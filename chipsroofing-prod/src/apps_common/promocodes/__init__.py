"""
    Модуль промокодов для заказов.

    Зависит от:
        libs.valute_field

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'promocodes',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'promocodes',
                    'models': (
                        'PromoCode',
                    )
                },
                ...
            }

    Детали реализации:
        Промокод - текстовый код, вводимый заказчиком при оформлении заказа.
        У каждого промокода есть стратегия (паттерн), которая по объекту заказа
        вычисляет размер скидки.

        Промокод может быть ограничен по времени и/или по количеству использований.


        Перед привязкой промокода, нужно пройти проверку промокода на доступность:
            from promocodes.exceptions import PromoCodeError

            try:
                promocode.validate(order)
            except PromoCodeError as e:
                logger.error(e.message)

        P.S. Для потокобезопасности рекомендуется проводить валидацию с добавлением промокода
        внутри транзакции с эксклюзивным доступом.


        Для возможности крепления промокода к ещё не подтвержденному заказу,
        у PromoCodeReference есть поле applied, которое отделяет подтвержденные использования
        промокода от ещё не подтвержденных.

        При подтверждении (оплате) заказа необходимо подтвердить использованные промокоды:
            order.promocode_refs.update(applied=True)

        P.S. При этом не проверяются ограничения использования промокода, т.к. иначе
        пришлось бы сообщать клиенту, что его промокод некорректен уже после того, как клиент
        добавил промокод к своему заказу, что не совсем корректно. Поэтому, теоретически,
        использований промокода может быть больше, чем заявлено в ограничениях.

    Пример:
        # models.py:
            class Order(model.Model):
                ...
                promocode_refs = GenericRelation(PromoCodeReference, verbose_name=_('promo codes'))


        # views.py:
            class AddPromocodeView(View):
                ...
                cursor = connection.cursor()
                cursor.execute('BEGIN WORK')
                cursor.execute('LOCK TABLE %s IN ACCESS EXCLUSIVE MODE' % (PromoCodeReference._meta.db_table,))

                try:
                    promocode.validate()
                except PromoCodeError as e:
                    raise Http404
                else:
                    order.references.create(
                        promocode=promocode,
                    )
                finally:
                    cursor.execute('COMMIT')


            class ConfirmOrder(View):
                ...
                order.promocode_refs.update(applied=True)

"""

default_app_config = 'promocodes.apps.Config'
