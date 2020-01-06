from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist

UserModel = get_user_model()


class EmailModelBackend(ModelBackend):
    """
        Авторизация по паре email-пароль
    """
    def authenticate(self, email=None, password=None, **kwargs):
        if isinstance(email, str):
            email = email.lower()

        try:
            user = UserModel._default_manager.get(email__iexact=email)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
