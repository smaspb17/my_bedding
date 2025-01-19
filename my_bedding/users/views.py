import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.middleware.csrf import get_token
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.http import require_POST, require_GET

from .context_processors import auth_forms
from .forms import RegisterUserForm, LoginUserForm, UserEditForm, ProfileEditForm, UserPasswordResetForm, \
    UserPasswordChangeForm
from .models import Profile
from .tasks import user_registered


User = get_user_model()


def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        secret_key = settings.RECAPTCHA_SECRET_KEY
        payload = {'secret': secret_key, 'response': recaptcha_response}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        result = response.json()
        print(f"reCAPTCHA результат верификации: {result}")
        if not result.get('success'):
            form.add_error('captcha', "Не пройдена captcha.")
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data['password']  # Получаем пароль до хэширования
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            user_registered.delay(user.id, raw_password)
            if user is not None:
                login(request, user)
            return JsonResponse({'success': True, 'redirect_url': reverse('users:view_account')},
                                status=201)
        else:
            # Возвращаем ошибки в виде JSON
            errors = {field: errors for field, errors in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user and user.is_active:
                login(request, user)
                response = JsonResponse({'success': True, 'message': 'Вход успешно выполнен'}, status=200)
            else:
                response = JsonResponse({'success': False, 'errors': {'password': ['Неверный логин или пароль']}},
                                        status=401)
        else:
            response = JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return response

def logout_user(request):
    logout(request)
    return redirect('shop:product_list')


@require_GET
@login_required(login_url='/')
def view_account(request):
    user = request.user
    profile = user.profile
    user_edit_form = UserEditForm(instance=user)
    profile_edit_form = ProfileEditForm(instance=profile)
    change_password_form = UserPasswordChangeForm(user=user)
    return render(request, 'users/personal_account.html',
                  {'user': user, 'profile': profile, 'user_edit_form': user_edit_form,
                   'profile_edit_form': profile_edit_form, 'change_password_form': change_password_form})


@require_POST
@login_required(login_url='/')
def edit_account(request):
    user = request.user
    profile = user.profile

    user_edit_form = UserEditForm(request.POST, instance=user)
    profile_edit_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
    change_password_form = UserPasswordChangeForm(data=request.POST, user=user)

    # Проверяем, есть ли данные для изменения пароля
    password_fields_filled = all(
        request.POST.get(field) for field in ['old_password', 'new_password1', 'new_password2']
    )

    if user_edit_form.is_valid() and profile_edit_form.is_valid() and change_password_form.is_valid():
        user_edit_form.save()
        profile_edit_form.save()

        # Сохраняем форму изменения пароля, только если были введены данные
        if password_fields_filled:
            change_password_form.save()
            update_session_auth_hash(request, user)  # Оставляем пользователя авторизованным

        return JsonResponse({'success': True}, status=200)

    else:
        # Если форма не валидна, отправляем ошибки
        errors = {}
        if not user_edit_form.is_valid():
            errors.update(user_edit_form.errors)
        if not profile_edit_form.is_valid():
            errors.update(profile_edit_form.errors)
        if not change_password_form.is_valid():
            errors.update(change_password_form.errors)
        return JsonResponse({'success': False, 'errors': errors}, status=400)


class PasswordResetAjaxView(View):
    def get(self, request, *args, **kwargs):
        form = UserPasswordResetForm()
        html_form = render_to_string('users/password_reset_form.html',
                                     {'form': form}, request=request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, *args, **kwargs):
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='users/password_reset_email.html',
                subject_template_name='users/password_reset_subject.txt',
                from_email=settings.DEFAULT_FROM_EMAIL,
            )
            html_reset_done = render_to_string('users/password_reset_done.html', request=request)
            return JsonResponse({'success': True, 'html_reset_done': html_reset_done},
                                status=200)
        else:
            errors = {field: error.get_json_data for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)


class PasswordResetConfirmAjaxView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Если пользователь найден, создаем форму для смены пароля
        form = SetPasswordForm(user) if user else None

        # Рендерим форму на страницу
        return render(request, 'users/password_reset_confirm.html', {'form': form})

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))  # Используем force_str вместо force_text
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Создаем форму с новыми данными из POST
        form = SetPasswordForm(user, request.POST)

        if form.is_valid():
            form.save()  # Сохраняем новый пароль
            login(request, user)
            return render(request, 'users/password_reset_complete.html', status=200)
        else:
            return render(request, 'users/password_reset_confirm.html', {'form': form},
                          status=400)


@login_required
def update_photo(request):
    if request.method == "POST" and request.FILES.get("photo"):
        profile = request.user.profile
        profile.photo = request.FILES["photo"]
        profile.save()
        return JsonResponse({"success": True, "photo_url": profile.photo['avatar'].url})
    return JsonResponse({"success": False})


@login_required
def delete_photo(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.photo.delete()  # Удаление файла из БД и системы
        profile.photo = None
        profile.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})