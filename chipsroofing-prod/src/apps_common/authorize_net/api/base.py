import json
import logging
import datetime
from decimal import Decimal
from django.utils.timezone import now
from django.utils.translation import ugettext
from authorizenet import apicontractsv1
from authorizenet.constants import constants
from authorizenet.apicontrollers import (
    getHostedPaymentPageController, getTransactionDetailsController,
    createTransactionController, ARBCreateSubscriptionController,
    ARBCancelSubscriptionController, ARBGetSubscriptionListController
)
from .. import conf

logger = logging.getLogger('django.authorize_net')


def _default_ref_id():
    return 'ref%d' % int(datetime.datetime.now().timestamp())


def create_auth(login_id=conf.LOGIN_ID, transaction_key=conf.TRANSACTION_KEY):
    auth = apicontractsv1.merchantAuthenticationType()
    auth.name = login_id
    auth.transactionKey = transaction_key
    return auth


def create_cc(card_number, card_expires, card_code):
    """
        Test:
            card_number:     4111111111111111
            card_expires:    2020-12
            card_code:       123
    """
    card = apicontractsv1.creditCardType()
    card.cardNumber = card_number
    if isinstance(card_expires, (datetime.datetime, datetime.date)):
        card.expirationDate = card_expires.strftime('%Y-%m')
    else:
        card.expirationDate = card_expires
    card.cardCode = card_code
    return card


def create_echeck(routing_number, account_number, name_on_account,
        bank_name=None, account_type=conf.ECHECK_ACCOUNT_CHECKING):
    """
        Test:
            routing_number:     121042882
            account_number:     123456789
            name_on_account:    John Doe
    """
    echeck = apicontractsv1.bankAccountType()

    account_type_enum = apicontractsv1.bankAccountTypeEnum
    if account_type == conf.ECHECK_ACCOUNT_SAVINGS:
        echeck.accountType = account_type_enum.savings
    else:
        echeck.accountType = account_type_enum.checking

    echeck.routingNumber = routing_number
    echeck.accountNumber = account_number
    echeck.nameOnAccount = name_on_account
    echeck.bankName = bank_name
    return echeck


def create_paypal(success_url=None, cancel_url=None):
    """
        Test:
            routing_number:     121042882
            account_number:     123456789
            name_on_account:    John Doe
    """
    paypal = apicontractsv1.payPalType()
    paypal.successUrl = success_url
    paypal.cancelUrl = cancel_url
    return paypal


def get_form_token(amount, email=None, invoice=None, description=None, **kwargs):
    # Merchant Name
    merchant_option = apicontractsv1.settingType()
    merchant_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentOrderOptions
    merchant_name = kwargs.get('merchantName', '')
    merchant_option.settingValue = json.dumps({
        'show': True,
        'merchantName': merchant_name,
    })

    # Return
    return_option = apicontractsv1.settingType()
    return_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentReturnOptions
    return_option.settingValue = json.dumps({
        'showReceipt': True,
        'url': kwargs.get('return_url', ''),
        'urlText': kwargs.get('return_text', ''),
        'cancelUrl': kwargs.get('cancel_url', ''),
        'cancelUrlText': kwargs.get('cancel_text', ''),
    })

    # Pay button
    button_option = apicontractsv1.settingType()
    button_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentButtonOptions
    button_option.settingValue = json.dumps({
        'text': ugettext('Pay'),
    })

    # Style
    style_option = apicontractsv1.settingType()
    style_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentStyleOptions
    style_option.settingValue = json.dumps({
        'bgColor': kwargs.get('color', '#3F8FCD'),
    })

    # CVV
    cvv_option = apicontractsv1.settingType()
    cvv_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentPaymentOptions
    cvv_option.settingValue = json.dumps({
        'cardCodeRequired': True,
    })

    # Captcha
    captcha_option = apicontractsv1.settingType()
    captcha_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentSecurityOptions
    captcha_option.settingValue = json.dumps({
        'captcha': kwargs.get('captcha', False),
    })

    # Shipping Form
    shipping_option = apicontractsv1.settingType()
    shipping_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentShippingAddressOptions
    shipping_option.settingValue = json.dumps({
        'show': kwargs.get('shippingForm', False),
        'required': kwargs.get('shippingRequired', False),
    })

    # Billing Form
    billing_option = apicontractsv1.settingType()
    billing_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentBillingAddressOptions
    billing_option.settingValue = json.dumps({
        'show': kwargs.get('billingForm', False),
        'required': kwargs.get('billingRequired', False),
    })

    # Email Field
    email_option = apicontractsv1.settingType()
    email_option.settingName = apicontractsv1.settingNameEnum.hostedPaymentCustomerOptions
    email_option.settingValue = json.dumps({
        'showEmail': kwargs.get('emailField', False),
        'requiredEmail': kwargs.get('emailRequired', False),
    })

    options = apicontractsv1.ArrayOfSetting()
    options.setting.append(merchant_option)
    options.setting.append(return_option)
    options.setting.append(button_option)
    options.setting.append(style_option)
    options.setting.append(cvv_option)
    options.setting.append(captcha_option)
    options.setting.append(shipping_option)
    options.setting.append(billing_option)
    options.setting.append(email_option)

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount

    transactionrequest.customer = apicontractsv1.customerDataType()
    transactionrequest.customer.email = email

    transactionrequest.billTo = apicontractsv1.customerAddressType()
    transactionrequest.billTo.firstName = kwargs.get('billing_firstname')
    transactionrequest.billTo.lastName = kwargs.get('billing_lastname')
    transactionrequest.billTo.company = kwargs.get('billing_company')
    transactionrequest.billTo.address = kwargs.get('billing_address')
    transactionrequest.billTo.city = kwargs.get('billing_city')
    transactionrequest.billTo.state = kwargs.get('billing_state')
    transactionrequest.billTo.zip = kwargs.get('billing_zipcode')
    transactionrequest.billTo.country = kwargs.get('billing_country')
    transactionrequest.billTo.phoneNumber = kwargs.get('billing_phone')

    transactionrequest.shipTo = apicontractsv1.nameAndAddressType()
    transactionrequest.shipTo.firstName = kwargs.get('shipping_firstname')
    transactionrequest.shipTo.lastName = kwargs.get('shipping_lastname')
    transactionrequest.shipTo.company = kwargs.get('shipping_company')
    transactionrequest.shipTo.address = kwargs.get('shipping_address')
    transactionrequest.shipTo.city = kwargs.get('shipping_city')
    transactionrequest.shipTo.state = kwargs.get('shipping_state')
    transactionrequest.shipTo.zip = kwargs.get('shipping_zipcode')
    transactionrequest.shipTo.country = kwargs.get('shipping_country')

    transactionrequest.order = apicontractsv1.orderType()
    transactionrequest.order.invoiceNumber = str(invoice) if invoice else None
    transactionrequest.order.description = description

    request = apicontractsv1.getHostedPaymentPageRequest()
    request.merchantAuthentication = kwargs.get('auth') or create_auth()
    request.transactionRequest = transactionrequest
    request.hostedPaymentSettings = options
    request.refId = str(kwargs.get('refId', '') or _default_ref_id())

    controller = getHostedPaymentPageController(request)
    if not conf.TEST_MODE:
        controller.setenvironment(constants.PRODUCTION)
    controller.execute()
    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            return response.token

        code = ''
        text = ''
        if response.messages is not None:
            code = response.messages.message[0]['code'].text
            text = response.messages.message[0]['text'].text

        logger.error('Error on get_form_token(): {0} ({1})'.format(code, text))


def get_transaction(trans_id, **kwargs):
    request = apicontractsv1.getTransactionDetailsRequest()
    request.merchantAuthentication = kwargs.get('auth') or create_auth()
    request.transId = str(trans_id)

    controller = getTransactionDetailsController(request)
    if not conf.TEST_MODE:
        controller.setenvironment(constants.PRODUCTION)
    controller.execute()
    response = controller.getresponse()
    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            return response.transaction

        code = ''
        text = ''
        if response.messages is not None:
            code = response.messages.message[0]['code'].text
            text = response.messages.message[0]['text'].text

        logger.error('Error on get_transaction(): {0} ({1})'.format(code, text))


def create_transaction(amount, credit_card=None, echeck=None, paypal=None,
        email=None, invoice=None, description=None, **kwargs):
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount

    transactionrequest.payment = apicontractsv1.paymentType()
    if credit_card is not None:
        transactionrequest.payment.creditCard = credit_card
    elif echeck is not None:
        transactionrequest.payment.bankAccount = echeck
    elif paypal is not None:
        transactionrequest.payment.payPal = paypal

    transactionrequest.customer = apicontractsv1.customerDataType()
    transactionrequest.customer.email = email

    transactionrequest.billTo = apicontractsv1.customerAddressType()
    transactionrequest.billTo.firstName = kwargs.get('billing_firstname')
    transactionrequest.billTo.lastName = kwargs.get('billing_lastname')
    transactionrequest.billTo.company = kwargs.get('billing_company')
    transactionrequest.billTo.address = kwargs.get('billing_address')
    transactionrequest.billTo.city = kwargs.get('billing_city')
    transactionrequest.billTo.state = kwargs.get('billing_state')
    transactionrequest.billTo.zip = kwargs.get('billing_zipcode')
    transactionrequest.billTo.country = kwargs.get('billing_country')
    transactionrequest.billTo.phoneNumber = kwargs.get('billing_phone')

    transactionrequest.shipTo = apicontractsv1.nameAndAddressType()
    transactionrequest.shipTo.firstName = kwargs.get('shipping_firstname')
    transactionrequest.shipTo.lastName = kwargs.get('shipping_lastname')
    transactionrequest.shipTo.company = kwargs.get('shipping_company')
    transactionrequest.shipTo.address = kwargs.get('shipping_address')
    transactionrequest.shipTo.city = kwargs.get('shipping_city')
    transactionrequest.shipTo.state = kwargs.get('shipping_state')
    transactionrequest.shipTo.zip = kwargs.get('shipping_zipcode')
    transactionrequest.shipTo.country = kwargs.get('shipping_country')

    transactionrequest.order = apicontractsv1.orderType()
    transactionrequest.order.invoiceNumber = str(invoice) if invoice else None
    transactionrequest.order.description = description

    request = apicontractsv1.createTransactionRequest()
    request.merchantAuthentication = kwargs.get('auth') or create_auth()
    request.transactionRequest = transactionrequest
    request.refId = str(kwargs.get('refId', '') or _default_ref_id())

    controller = createTransactionController(request)
    if not conf.TEST_MODE:
        controller.setenvironment(constants.PRODUCTION)
    controller.execute()
    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            return response

        code = ''
        text = ''
        if response.messages is not None:
            code = response.messages.message[0]['code'].text
            text = response.messages.message[0]['text'].text

        logger.error('Error on create_transaction(): {0} ({1})'.format(code, text))


def void_transaction(trans_id, **kwargs):
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "voidTransaction"
    transactionrequest.refTransId = str(trans_id)

    request = apicontractsv1.createTransactionRequest()
    request.merchantAuthentication = kwargs.get('auth') or create_auth()
    request.transactionRequest = transactionrequest
    request.refId = str(kwargs.get('refId', '') or _default_ref_id())

    controller = createTransactionController(request)
    if not conf.TEST_MODE:
        controller.setenvironment(constants.PRODUCTION)
    controller.execute()
    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            return True

        code = ''
        text = ''
        if response.messages is not None:
            code = response.messages.message[0]['code'].text
            text = response.messages.message[0]['text'].text

        logger.error('Error on void_transaction(): {0} ({1})'.format(code, text))


def create_subscription(name, amount, credit_card=None, echeck=None,
        email=None, phone=None, invoice=None, description=None,
        interval_length=1, interval_unit=conf.RECURRING_UNITS_MONTHS,
        total_occurrences=12, trial_occurrences=0, trial_amount=None,
        start_date=None, **kwargs):
    subscription = apicontractsv1.ARBSubscriptionType()
    subscription.name = name
    subscription.amount = amount
    subscription.trialAmount = trial_amount or Decimal('0.00')

    subscription.payment = apicontractsv1.paymentType()
    if credit_card is not None:
        subscription.payment.creditCard = credit_card
    elif echeck is not None:
        subscription.payment.bankAccount = echeck

    subscription.paymentSchedule = apicontractsv1.paymentScheduleType()
    subscription.paymentSchedule.interval = apicontractsv1.paymentScheduleTypeInterval()
    subscription.paymentSchedule.interval.length = interval_length

    if interval_unit == conf.RECURRING_UNITS_DAYS:
        subscription.paymentSchedule.interval.unit = apicontractsv1.ARBSubscriptionUnitEnum.days
    elif interval_unit == conf.RECURRING_UNITS_MONTHS:
        subscription.paymentSchedule.interval.unit = apicontractsv1.ARBSubscriptionUnitEnum.months

    subscription.paymentSchedule.startDate = start_date or now().date()
    subscription.paymentSchedule.totalOccurrences = total_occurrences
    subscription.paymentSchedule.trialOccurrences = trial_occurrences

    subscription.customer = apicontractsv1.customerType()
    subscription.customer.email = email
    subscription.customer.phoneNumber = phone

    subscription.billTo = apicontractsv1.nameAndAddressType()
    subscription.billTo.firstName = kwargs.get('billing_firstname')
    subscription.billTo.lastName = kwargs.get('billing_lastname')
    subscription.billTo.company = kwargs.get('billing_company')
    subscription.billTo.address = kwargs.get('billing_address')
    subscription.billTo.city = kwargs.get('billing_city')
    subscription.billTo.state = kwargs.get('billing_state')
    subscription.billTo.zip = kwargs.get('billing_zipcode')
    subscription.billTo.country = kwargs.get('billing_country')

    subscription.shipTo = apicontractsv1.nameAndAddressType()
    subscription.shipTo.firstName = kwargs.get('shipping_firstname')
    subscription.shipTo.lastName = kwargs.get('shipping_lastname')
    subscription.shipTo.company = kwargs.get('shipping_company')
    subscription.shipTo.address = kwargs.get('shipping_address')
    subscription.shipTo.city = kwargs.get('shipping_city')
    subscription.shipTo.state = kwargs.get('shipping_state')
    subscription.shipTo.zip = kwargs.get('shipping_zipcode')
    subscription.shipTo.country = kwargs.get('shipping_country')

    subscription.order = apicontractsv1.orderType()
    subscription.order.invoiceNumber = str(invoice) if invoice else None
    subscription.order.description = description

    request = apicontractsv1.ARBCreateSubscriptionRequest()
    request.merchantAuthentication = kwargs.get('auth') or create_auth()
    request.subscription = subscription
    request.refId = str(kwargs.get('refId', '') or _default_ref_id())

    controller = ARBCreateSubscriptionController(request)
    if not conf.TEST_MODE:
        controller.setenvironment(constants.PRODUCTION)
    controller.execute()
    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            return response

        code = ''
        text = ''
        if response.messages is not None:
            code = response.messages.message[0]['code'].text
            text = response.messages.message[0]['text'].text

        logger.error('Error on create_subscription(): {0} ({1})'.format(code, text))


def cancel_subscription(subscription_id, **kwargs):
    request = apicontractsv1.ARBCancelSubscriptionRequest()
    request.merchantAuthentication = kwargs.get('auth') or create_auth()
    request.subscriptionId = str(subscription_id)
    request.refId = str(kwargs.get('refId', '') or _default_ref_id())

    controller = ARBCancelSubscriptionController(request)
    if not conf.TEST_MODE:
        controller.setenvironment(constants.PRODUCTION)
    controller.execute()
    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            return True

        code = ''
        text = ''
        if response.messages is not None:
            code = response.messages.message[0]['code'].text
            text = response.messages.message[0]['text'].text

        logger.error('Error on cancel_subscription(): {0} ({1})'.format(code, text))


def get_subscriptions(**kwargs):
    request = apicontractsv1.ARBGetSubscriptionListRequest()
    request.merchantAuthentication = kwargs.get('auth') or create_auth()
    request.searchType = apicontractsv1.ARBGetSubscriptionListSearchTypeEnum.subscriptionInactive
    request.refId = str(kwargs.get('refId', '') or _default_ref_id())

    request.sorting = apicontractsv1.ARBGetSubscriptionListSorting()
    request.sorting.orderBy = apicontractsv1.ARBGetSubscriptionListOrderFieldEnum.id
    request.sorting.orderDescending = "false"

    request.paging = apicontractsv1.Paging()
    request.paging.limit = kwargs.get('limit', 100)
    request.paging.offset = kwargs.get('offset', 1)

    controller = ARBGetSubscriptionListController(request)
    if not conf.TEST_MODE:
        controller.setenvironment(constants.PRODUCTION)
    controller.execute()
    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            return [
                item.subscriptionDetail
                for item in response.subscriptionDetails
            ]

        code = ''
        text = ''
        if response.messages is not None:
            code = response.messages.message[0]['code'].text
            text = response.messages.message[0]['text'].text

        logger.error('Error on cancel_subscription(): {0} ({1})'.format(code, text))
