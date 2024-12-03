from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View, TemplateView
from user.models import User


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()  # Декодирование байт в строку
            user = User.objects.get(pk=uid)  # Получаем пользователя по его id
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("user:email_confirmed")
        else:
            return redirect("user:email_confirmation_failed")


class EmailConfirmationSentView(TemplateView):
    template_name = "email/email_confirmation_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено."
        return context


class EmailConfirmedView(TemplateView):
    template_name = "email/email_confirmed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес активирован."
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = "email/email_confirmation_failed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес не активирован."
        return context
