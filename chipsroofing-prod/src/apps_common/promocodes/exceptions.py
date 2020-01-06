class PromoCodeError(Exception):
    """ Базовый класс исключений """
    def __init__(self, message, *args):
        self.message = message
        super().__init__(*args)


class PromoCodeValidationError(PromoCodeError):
    pass


class PromoCodeLimitReachedError(PromoCodeError):
    pass


class PromoCodeExpiredError(PromoCodeError):
    pass
