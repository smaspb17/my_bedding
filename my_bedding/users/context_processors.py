from django.conf import settings

from .forms import RegisterUserForm, LoginUserForm


def auth_forms(request):
    return {
        'reg_form': RegisterUserForm(),
        'login_form': LoginUserForm(),
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
    }
