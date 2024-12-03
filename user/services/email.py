from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404

User = get_user_model()


def send_contact_email_message(subject, email, content, ip, user_id):
    """
    Функция отправки письма из формы обратной связи
    """
    # Получаем пользователя по его id
    user = User.objects.get(id=user_id) if user_id else None
    print(f"Пользователь {user}")
    # Отправляем письмо на почту
    message = render_to_string(
        "system/email/feedback_email_send.html",
        {
            "email": email,
            "content": content,
            "ip": ip,
            "user": user,
        },
    )
    email = EmailMessage(subject, message, settings.EMAIL_SERVER, settings.EMAIL_ADMIN)
    print(f"Отправляем письмо на почту {email}")
    email.send(fail_silently=False)


def send_activate_email_message(user_id):
    """
    Функция отправки письма с подтверждением для аккаунта
    """
    # Получаем пользователя по его id
    user = get_object_or_404(User, id=user_id)
    print(f"Пользователь {user}")
    # Получаем текущий сайт
    current_site = Site.objects.get_current().domain
    print(f"Текущий сайт {current_site}")
    # Генерируем токен активации пользователя
    token = default_token_generator.make_token(user)
    # Генерируем uidb64 для хранения в базе данных
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    # Генерируем ссылку для активации пользователя в письме
    activation_url = reverse_lazy(
        "user:confirm_email", kwargs={"uidb64": uid, "token": token}
    )
    # Объект с данными для отправки письма
    subject = f"Активируйте свой аккаунт, {user.username}!"
    # Сообщение с данными для отправки письма
    message = render_to_string(
        "email/activate_email_send.html",
        {
            "user": user,
            "activation_url": f"https://{current_site}{activation_url}",
        },
    )
    # Возвращаем функции отправки письма
    return user.email_user(subject, message)
