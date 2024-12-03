from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from user.forms import UserForgotPasswordForm, UserSetNewPasswordForm


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """

    # Класс формы сброса пароля
    form_class = UserForgotPasswordForm
    template_name = "password/user_password_reset.html"
    success_url = reverse_lazy("shop:main_page")
    success_message = (
        "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    )
    subject_template_name = "password/password_subject_reset_mail.txt"
    email_template_name = "password/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """

    form_class = UserSetNewPasswordForm
    template_name = "password/user_password_set_new.html"
    success_url = reverse_lazy("shop:main_page")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context
