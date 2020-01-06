from .models import Subscriber
from . import api


def make_subscriber(email, name=None, last_name=None, company=None, resubscribe=False, save=True):
    """
        Получение или создание подписчика.

        Параметры:
            resubscribe - подписать заново, если пользователь ранее отписался.
            save        - сохранить в БД
    """
    email = email.lower().strip()

    try:
        subscriber = Subscriber.objects.get(email=email)
    except Subscriber.DoesNotExist:
        subscriber = Subscriber(
            email=email,
        )

    if name is not None:
        subscriber.name = name
    if last_name is not None:
        subscriber.last_name = last_name
    if company is not None:
        subscriber.company = company

    if resubscribe and subscriber.status == api.subscribers.STATUS_UNSUBSCRIBED:
        subscriber.status = api.subscribers.STATUS_ACTIVE

    if save:
        subscriber.save()

    return subscriber


def fill_demo(content):
    """
        Вставка тестовых данных в тело письма
    """
    content = content.replace('{$url}', '#')
    content = content.replace('{$unsubscribe}', '#')
    content = content.replace('{$email}', 'john@smithmail.com')
    content = content.replace('{$name}', 'John')
    content = content.replace('{$last_name}', 'Smith')
    content = content.replace('{$company}', 'Microsoft')
    return content
