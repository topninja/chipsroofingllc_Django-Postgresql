from django.conf import settings
from django.http.response import Http404
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, FormView, TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import redirect, resolve_url, get_object_or_404
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.views import password_reset, password_reset_confirm
from seo.seo import Seo
from .forms import LoginForm, RegisterForm, PasswordResetForm, SetPasswordForm

UserModel = get_user_model()


def get_redirect_url(request, default=settings.LOGIN_REDIRECT_URL):
    """
        Получение адреса для редиректа из POST, GET или settings
    """
    redirect_to = request.POST.get(
        REDIRECT_FIELD_NAME,
        request.GET.get(REDIRECT_FIELD_NAME, '')
    )
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(default)
    return redirect_to


class LoginView(FormView):
    """ Страница авторизации """
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(get_redirect_url(request))

        # Seo
        seo = Seo()
        seo.title = _('Authorization')
        seo.save(request)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect(get_redirect_url(self.request))


class LogoutView(View):
    """ Выход из профиля """
    def get(self, request):
        raise Http404

    @staticmethod
    def post(request, next_page=None):
        auth_logout(request)

        if next_page:
            next_page = resolve_url(next_page)
        else:
            next_page = get_redirect_url(request, default=settings.LOGOUT_URL)

        return redirect(next_page)


class RegisterView(FormView):
    """ Страница регистрации """
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(get_redirect_url(request))

        # Seo
        seo = Seo()
        seo.title = _('Registration')
        seo.save(request)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(get_redirect_url(request))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user = authenticate(
            username=user.username,
            password=form.cleaned_data.get('password1')
        )
        auth_login(self.request, user)
        return redirect(get_redirect_url(self.request))


class PasswordResetView(TemplateView):
    """
        Страница с формой ввода email для сброса пароля, если
        текущий пользователь не авторизован.

        Если пользователь авторизован, сразу будет показана форма
        установки нового пароля.
    """
    template_name = 'users/reset_confirm.html'

    def get(self, request, *args, **kwargs):
        # Seo
        seo = Seo()
        seo.title = _('Password reset')
        seo.save(request)

        if request.user.is_authenticated():
            # Смена своего пароля, если авторизованы
            form = SetPasswordForm(request.user)
            return self.render_to_response({
                'form': form,
                'target': resolve_url('users:reset_self'),
            })
        else:
            return password_reset(request,
                template_name='users/reset.html',
                password_reset_form=PasswordResetForm,
            )

    @staticmethod
    def post(request):
        email = request.POST.get('email', '')
        request.session['reset_email'] = email

        # Seo
        seo = Seo()
        seo.title = _('Password reset')
        seo.save(request)

        return password_reset(request,
            template_name='users/reset.html',
            password_reset_form=PasswordResetForm,
            post_reset_redirect='users:reset_done',
            email_template_name='users/emails/reset_email.html',
            html_email_template_name='users/emails/reset_email.html',
            subject_template_name='users/emails/reset_subject.html',
        )


class ResetDoneView(TemplateView):
    """ Страница с сообщением о том, что инструкции для сброса пароля отправлены на почту """
    template_name = 'users/reset_done.html'

    def get(self, request, *args, **kwargs):
        email = request.session.get('reset_email')
        if not email:
            return redirect(resolve_url(settings.RESET_PASSWORD_REDIRECT_URL))

        # Seo
        seo = Seo()
        seo.title = _('Password reset')
        seo.save(request)

        return self.render_to_response({
            'email': email,
        })

    @staticmethod
    def post(request):
        return redirect(request.build_absolute_uri(request.path_info))


class ResetConfirmView(TemplateView):
    """
        Страница с формой ввода нового пароля
        для неавторизованного пользователя.
    """
    template_name = 'users/reset_confirm.html'

    def get(self, request, uidb64=None, token=None):
        if request.user.is_authenticated():
            return redirect(get_redirect_url(request))

        # Seo
        seo = Seo()
        seo.title = _('Password reset')
        seo.save(request)

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, token):
            return redirect(resolve_url(settings.RESET_PASSWORD_REDIRECT_URL))

        return password_reset_confirm(request,
            uidb64=uidb64,
            token=token,
            template_name='users/reset_confirm.html',
            set_password_form=SetPasswordForm,
            post_reset_redirect='users:reset_complete',
        )

    def post(self, request, uidb64=None, token=None):
        # Seo
        seo = Seo()
        seo.title = _('Password reset')
        seo.save(request)

        if request.user.is_authenticated():
            # Смена своего пароля, если авторизованы
            form = SetPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                return redirect(get_redirect_url(request, 'users:reset_complete'))
            else:
                return self.render_to_response({
                    'form': form,
                })
        else:
            if uidb64 is None or token is None:
                return redirect(resolve_url(settings.RESET_PASSWORD_REDIRECT_URL))

            return password_reset_confirm(request,
                uidb64=uidb64,
                token=token,
                template_name='users/reset_confirm.html',
                set_password_form=SetPasswordForm,
                post_reset_redirect='users:reset_complete',
            )


class ResetCompleteView(TemplateView):
    """ Страница с сообщением о успешной смене пароля """
    template_name = 'users/reset_complete.html'

    def get(self, request, *args, **kwargs):
        # Seo
        seo = Seo()
        seo.title = _('Password reset')
        seo.save(request)

        if request.user.is_authenticated():
            return redirect(get_redirect_url(request))
        else:
            email = request.session.pop('reset_email', '')
            if not email:
                return redirect(resolve_url(settings.RESET_PASSWORD_REDIRECT_URL))

            return self.render_to_response({
                'redirect': resolve_url(settings.RESET_PASSWORD_REDIRECT_URL),
            })


class ProfileView(TemplateView):
    """ Страница профиля """
    template_name = 'users/profile.html'

    def get(self, request, *args, username=None, **kwargs):
        if not username and not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL)

        request.js_storage.update(
            avatar_upload=resolve_url('users:avatar_upload'),
            avatar_crop=resolve_url('users:avatar_crop'),
            avatar_delete=resolve_url('users:avatar_delete'),
        )

        if username:
            user = get_object_or_404(UserModel, username=username)
        elif not request.user.is_authenticated():
            raise Http404
        else:
            user = request.user

        # Seo
        seo = Seo()
        seo.title = _('Profile of «%(username)s»') % {'username': user.username}
        seo.save(request)

        return self.render_to_response({
            'profile_user': user,
        })
