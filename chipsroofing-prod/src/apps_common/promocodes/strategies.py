from decimal import Decimal, InvalidOperation
from django.utils.translation import ugettext_lazy as _
from libs.valute_field.valute import Valute


class BaseStrategy:
    name = ''
    description = ''

    @classmethod
    def short_description(cls, promo):
        raise NotImplementedError

    @classmethod
    def full_description(cls, promo):
        raise NotImplementedError

    @classmethod
    def validate_form(cls, form, cleaned_data):
        """
            Валидация формы админки при добавлении/редактировании промокода.
        """
        return cleaned_data

    @classmethod
    def validate(cls, *args, **kwargs):
        """
            Персональная для стратегии валидация, что промокод может быть использован.
            В случае ошибки следует вызвать исключение подкласса PromoCodeError
        """
        pass

    @classmethod
    def calculate(cls, promo, products_cost, **kwargs):
        raise NotImplementedError


class FixedAmountStrategy(BaseStrategy):
    """ Фиксированная скидка, например 100 рублей """
    name = 'fixed_amount'
    description = _('Fixed monetary amount')

    @classmethod
    def short_description(cls, promo):
        return '-%s' % Valute(promo.parameter)

    @classmethod
    def full_description(cls, promo):
        return _('Discount %s') % Valute(promo.parameter)

    @classmethod
    def validate_form(cls, form, cleaned_data):
        parameter = cleaned_data.get('parameter', '')
        if not parameter:
            form.add_error('parameter', _('This field cannot be blank.'))
            return

        try:
            amount = Valute(parameter)
        except (TypeError, ValueError, InvalidOperation):
            form.add_error('parameter', _('Invalid value'))
            return

        if not amount:
            form.add_error('parameter', _('Ensure this value is greater than 0'))
            return

        return cleaned_data

    @classmethod
    def calculate(cls, promo, products_cost, **kwargs):
        amount = min(products_cost, Valute(promo.parameter))
        return amount


class PercentageStrategy(BaseStrategy):
    """ Процентная скидка, например 10% """
    name = 'percent'
    description = _('Percentage discount')

    @classmethod
    def short_description(cls, promo):
        return '-%s%%' % Decimal(promo.parameter)

    @classmethod
    def full_description(cls, promo):
        return _('Discount %s%%') % Decimal(promo.parameter)

    @classmethod
    def validate_form(cls, form, cleaned_data):
        parameter = cleaned_data.get('parameter', '')
        if not parameter:
            form.add_error('parameter', _('This field cannot be blank.'))
            return

        try:
            percentage = Decimal(parameter)
        except (TypeError, ValueError, InvalidOperation):
            form.add_error('parameter', _('Invalid value'))
            return

        if not percentage:
            form.add_error('parameter', _('Ensure this value is greater than 0'))
            return

        return cleaned_data

    @classmethod
    def calculate(cls, promo, products_cost, **kwargs):
        percentage = Decimal(promo.parameter)
        return products_cost * percentage / 100


ALL_STRATEGIES = (FixedAmountStrategy, PercentageStrategy)
STRATEGIES = {
    strategy.name: strategy
    for strategy in ALL_STRATEGIES
}
STRATEGY_CHOICES = tuple(
    (strategy.name, strategy.description)
    for strategy in ALL_STRATEGIES
)
