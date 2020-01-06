import logging
from pytz import timezone
from datetime import datetime
from itertools import chain, islice
from concurrent.futures import ThreadPoolExecutor
from django.utils.timezone import now
from django.db import models, transaction
from django.core.management import BaseCommand
from ...models import MailerConfig, Group, RegularCampaign, Subscriber
from ... import conf
from ... import api

logger = logging.getLogger('mailerlite')
THREADS = 2

# TODO: если был импортирован черновик рассылки, а потом запущен через админку - отправится пустое письмо
# TODO: при большом кол-ве подписчиков импорт будет долгим


class Command(BaseCommand):
    """
        Синхронизация данных
    """
    tz = None

    def add_arguments(self, parser):
        parser.add_argument('-eg', '--export-groups',
            action='store_true',
            dest='export_groups',
            help='Export groups'
        )
        parser.add_argument('-ig', '--import-groups',
            action='store_true',
            dest='import_groups',
            help='Import groups'
        )

        parser.add_argument('-ec', '--export-campaigns',
            action='store_true',
            dest='export_campaigns',
            help='Export campaigns'
        )
        parser.add_argument('-ic', '--import-campaigns',
            action='store_true',
            dest='import_campaigns',
            help='Import campaigns'
        )

        parser.add_argument('-is', '--import-subscribers',
            action='store_true',
            dest='import_subscribers',
            help='Import subscribers'
        )
        parser.add_argument('-es', '--export-subscribers',
            action='store_true',
            dest='export_subscribers',
            help='Export subscribers'
        )

    @staticmethod
    def all_pages(import_func, *args, per_page=100, **kwargs):
        page = 0
        kwargs['limit'] = per_page
        while True:
            kwargs['offset'] = page * per_page

            try:
                items = import_func(*args, **kwargs)
            except api.SubscribeAPIError as e:
                logger.error(e.message)
                return

            for item in items:
                yield item

            if len(items) < per_page:
                break
            else:
                page += 1

    def to_datetime(self, date_str):
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return self.tz.localize(date)

    def export_groups(self):
        """
            Многопоточная отправка групп в MailerLite.
        """
        logger.info("Export groups...")
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            for group in Group.objects.filter(need_export=True):
                executor.submit(self._export_group, group)

    @staticmethod
    def _export_group(group):
        if group.remote_id == 0:
            # создание
            try:
                response = api.groups.create(
                    name=group.name,
                )
            except api.SubscribeAPIError as e:
                logger.error(e.message)
            else:
                group.remote_id = response['id']
                group.save(need_export=False)
        else:
            # обновление
            try:
                api.groups.update(
                    group.remote_id,
                    name=group.name,
                )
            except api.SubscribeAPIError as e:
                logger.error(e.message)
            else:
                group.save(need_export=False)

    def import_groups(self):
        """
            Загрузка групп
        """
        logger.info('Import groups...')
        group_iter = self.all_pages(api.groups.get_all)
        while True:
            pack = list(islice(group_iter, 25))
            if not pack:
                break

            with transaction.atomic():
                for remote_group in pack:
                    self._import_group(remote_group)

    def _import_group(self, data):
        group, created = Group.objects.get_or_create(
            remote_id=data['id']
        )
        if created:
            logger.info("Group '%s' created." % data['name'])

        group.name = data['name']
        group.total = data['total']
        group.active = data['active']
        group.bounced = data['bounced']
        group.unsubscribed = data['unsubscribed']
        group.sent = data['sent']
        group.opened = data['opened']
        group.clicked = data['clicked']
        group.date_created = self.to_datetime(data['date_created'])
        group.date_updated = self.to_datetime(data['date_updated'])
        group.save(need_export=False)

    def export_campaigns(self):
        """
            Многопоточная отправка рассылок в MailerLite.
        """
        logger.info("Export campaigns...")
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            campaigns = RegularCampaign.objects.filter(
                export_allowed=True,
                status=api.campaings.STATUS_DRAFT
            ).prefetch_related('groups')
            for campaign in campaigns:
                executor.submit(self._export_campaign, campaign)

    @staticmethod
    def _export_campaign(campaign):
        if campaign.remote_id == 0:
            # рассылка ещё не существует
            try:
                response = api.campaings.create(
                    subject=campaign.subject,
                    from_name=campaign.from_name,
                    from_email=campaign.from_email,
                    groups=[group.remote_id for group in campaign.groups.all()],
                )
            except api.SubscribeAPIError as e:
                logger.error(e.message)
                return
            else:
                campaign.remote_id = response['id']
                campaign.save()
                logger.info("Published campaign '%s'" % campaign.subject)

        # установка содержимого
        try:
            api.campaings.content(
                campaign.remote_id,
                html=campaign.final_html(scheme='https://' if conf.HTTPS_ALLOWED else 'http://'),
                plain=campaign.final_plain(),
            )
        except api.SubscribeAPIError as e:
            # отмена рассылки
            campaign.export_allowed = False
            campaign.save()
            logger.error(e.message)
            return
        else:
            logger.info("Setted content for campaign '%s'" % campaign.subject)

        # запуск
        try:
            api.campaings.action(
                campaign.remote_id,
                action_type=api.campaings.ACTION_SEND
            )
        except api.SubscribeAPIError as e:
            logger.error(e.message)
        else:
            campaign.status = api.campaings.STATUS_OUTBOX
            campaign.save()
            logger.info("Started campaign '%s'" % campaign.subject)

    def import_campaigns(self, status=api.campaings.STATUS_SENT):
        """ Загрузка рассылок """
        logger.info("Import campaigns with status '%s'..." % status)
        campaign_iter = self.all_pages(api.campaings.get_all, status)
        while True:
            pack = list(islice(campaign_iter, 25))
            if not pack:
                break

            with transaction.atomic():
                for campaign in pack:
                    self._import_campaign(campaign)

    def _import_campaign(self, data):
        campaign, created = RegularCampaign.objects.get_or_create(
            remote_id=data['id']
        )
        if created:
            logger.info("Campaign '%s' created." % data['name'])

        campaign.subject = data['name']
        campaign.status = data['status']
        campaign.total_recipients = data['total_recipients']
        campaign.opened = data['opened']['count']
        campaign.clicked = data['clicked']['count']
        campaign.date_created = self.to_datetime(data['date_created'])

        if campaign.status == api.campaings.STATUS_DRAFT:
            campaign.export_allowed = False
            campaign.date_send = None
        else:
            campaign.export_allowed = True
            campaign.date_send = self.to_datetime(data['date_send'])

        campaign.save()

    @staticmethod
    def export_subscribers():
        """
            Отправка подписчиков в MailerLite
        """
        logger.info("Export subscribers...")
        subscribers = Subscriber.objects.filter(
            need_export=True,
            status__in=[api.subscribers.STATUS_ACTIVE, api.subscribers.STATUS_UNSUBSCRIBED]
        ).only(
            'email', 'status', 'name', 'last_name', 'company',
        ).prefetch_related('groups')

        subscriber_iter = iter(subscribers)
        while True:
            pack = list(islice(subscriber_iter, 250))
            if not pack:
                break

            bulk_groups = {}
            for subscriber in pack:
                if subscriber.remote_id:
                    try:
                        api.subscribers.update(
                            subscriber.email,
                            status=subscriber.status,
                            name=subscriber.name,
                            last_name=subscriber.last_name,
                            company=subscriber.company,
                        )
                    except api.SubscribeAPIError as e:
                        logger.error(e.message)
                else:
                    try:
                        api.subscribers.create(
                            subscriber.email,
                            status=subscriber.status,
                            name=subscriber.name,
                            last_name=subscriber.last_name,
                            company=subscriber.company,
                        )
                    except api.SubscribeAPIError as e:
                        logger.error(e.message)

                for group_id in subscriber.groups.values_list('remote_id', flat=True):
                    bulk_groups.setdefault(group_id, []).append(
                        {
                            'email': subscriber.email,
                            'type': subscriber.status,
                        }
                    )

            for group_id, records in bulk_groups.items():
                logger.info('Adding to group #%s %d items...' % (group_id, len(records)))

                try:
                    response = api.subscribers.bulk_subscribe(group_id, records)
                except api.SubscribeAPIError as e:
                    logger.error(e.message)
                    continue
                else:
                    logger.info('  Imported: %s' % len(response['imported']))
                    logger.info('  Updated: %s' % len(response['updated']))
                    logger.info('  Unchanged: %s' % len(response['unchanged']))
                    logger.info('  Errors: %s' % len(response['errors']))

                    with transaction.atomic():
                        for row in chain(response['imported'], response['updated'], response['unchanged']):
                            Subscriber.objects.filter(email=row['email']).update(
                                need_export=False,
                                remote_id=row['id'],
                            )

                    for row in response['errors']:
                        logger.error('%r' % row)

    def import_subscribers(self):
        """
            Загрузка подписчиков
        """
        logger.info("Import subscribers...")
        for group in Group.objects.all():
            subscriber_iter = self.all_pages(api.subscribers.get_all, group.remote_id)
            while True:
                pack = list(islice(subscriber_iter, 50))
                if not pack:
                    break

                with transaction.atomic():
                    for subscriber in pack:
                        self._import_subscriber(group, subscriber)

    def _import_subscriber(self, group, data):
        try:
            subscriber = Subscriber.objects.get(
                models.Q(remote_id=data['id']) |
                models.Q(email=data['email'], remote_id=0)
            )
        except Subscriber.MultipleObjectsReturned:
            logger.warning("MultipleObjectsReturned for ({0[id]}, {0[email]}).".format(data))
            return
        except Subscriber.DoesNotExist:
            subscriber = Subscriber()
            logger.info("Subscriber '{0[email]}' created.".format(data))
        else:
            # Если ожидает экспорта - пропускаем, пока не экспортируется
            if subscriber.need_export:
                return

        subscriber_fields = {
            field['key']: field['value']
            for field in data['fields']
        }

        subscriber.email = data['email']
        subscriber.name = subscriber_fields['name'] or ''
        subscriber.last_name = subscriber_fields['last_name'] or ''
        subscriber.company = subscriber_fields['company'] or ''
        subscriber.status = data['type']
        subscriber.remote_id = data['id']
        subscriber.sent = data['sent']
        subscriber.opened = data['opened']
        subscriber.clicked = data['clicked']
        subscriber.date_created = self.to_datetime(data['date_created'])

        if data['date_subscribe']:
            subscriber.date_subscribe = self.to_datetime(data['date_subscribe'])
        else:
            subscriber.date_subscribe = None

        if data['date_updated']:
            subscriber.date_updated = self.to_datetime(data['date_updated'])
        else:
            subscriber.date_updated = None

        if data['date_unsubscribe']:
            subscriber.date_unsubscribe = self.to_datetime(data['date_unsubscribe'])
        else:
            subscriber.date_unsubscribe = None

        subscriber.save(need_export=False)
        if not subscriber.groups.filter(pk=group.pk).exists():
            subscriber.groups.add(group)

    def handle(self, *args, **options):
        config = MailerConfig.get_solo()

        try:
            tz_name = api.request('me')
        except api.SubscribeAPIError as e:
            logger.error(e.message)
        else:
            self.tz = timezone(tz_name['account']['timezone']['timezone'])

        # Groups
        if options['export_groups']:
            self.export_groups()
            config.export_groups_date = now()

        if options['import_groups']:
            self.import_groups()
            config.import_groups_date = now()

        # Subscribers
        if options['export_subscribers']:
            self.export_subscribers()
            config.export_subscribers_date = now()

        if options['import_subscribers']:
            try:
                self.import_subscribers()
            except api.SubscribeAPIError as e:
                logger.error(e.message)
            else:
                config.import_subscribers_date = now()

        # Campaigns
        if options['export_campaigns']:
            self.export_campaigns()
            config.export_campaigns_date = now()

        if options['import_campaigns']:
            for status in api.campaings.STATUSES:
                self.import_campaigns(status)
            config.import_campaigns_date = now()

        config.save()
