from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from cart.models import Cart
from order.models import Order, OrderItem
from user.forms import UserRegistrationForm, ProfileForm
from user.mixins.UserMixin import UserIsNotAuthenticated
from .services.tasks import send_activate_email_message_task


class UserLoginView(LoginView):
    template_name = "user/login.html"
    # form_class = UserLoginForm

    # success_url = reverse_lazy('main:home_page')

    def get_success_url(self):  # Перенаправление после успешного входа
        # Получаем параметр next (на какую страницу хотел зайти пользователь)
        redirect_page = self.request.GET.get("next", None)
        # Если параметр есть и страница "не выйти из аккаунта", то перенаправляем на запрашиваемую страницу
        if redirect_page and redirect_page != reverse("users:logout_page"):
            return redirect_page
        # Иначе перенаправляем на главную страницу
        return reverse_lazy("shop:main_page")

    def form_valid(
        self, form
    ):  # Проверка наличия сессионного ключа для неавторизованного пользователя
        # Получаем сессионный ключ
        session_key = self.request.session.session_key
        # Получаем пользователя
        user = form.get_user()
        # Если есть пользователь, то логиним его
        if user:
            auth.login(self.request, user)
            # Если есть сессионный ключ
            if session_key:
                # Присваиваем переменной forgot_carts значение корзин пользователя
                forgot_carts = Cart.objects.filter(user=user)
                # Если в корзине есть хотя бы одна корзина
                if forgot_carts.exists():
                    # Удаляем все корзины пользователя
                    forgot_carts.delete()
                # Обновляем значение сессионного ключа на авторизованного пользователя
                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
                return HttpResponseRedirect(self.get_success_url())


class UserRegistrationView(
    UserIsNotAuthenticated, CreateView
):  # Форма регистрации пользователя
    # Имя шаблона для отображения формы регистрации
    template_name = "user/registration.html"
    # Форма регистрации пользователя с моделью User (поля для регистрации)
    form_class = UserRegistrationForm
    # Указываем URL, на которую будет перенаправлен пользователь после успешной регистрации
    success_url = reverse_lazy("shop:main_page")

    def form_valid(self, form):
        # Получаем сессионный ключ
        session_key = self.request.session.session_key
        # Получаем пользователя из формы данных (данные которые пришли с формы регистрации)
        user = form.save(commit=False)
        # Делаем пользователя неактивным до подтверждения email
        user.is_active = False
        user.save()

        # Отправляем email для активации
        send_activate_email_message_task.delay(user.id)

        # Если есть сессионный ключ
        if session_key:
            # Обновляем значение сессионного ключа на авторизованного пользователя
            Cart.objects.filter(session_key=session_key).update(user=user)

        # Выводим сообщение о том, что необходимо подтвердить email
        messages.success(
            self.request,
            f"{user.username}, пожалуйста, подтвердите свой электронный адрес. Письмо отправлено на {user.email}",
        )

        # Перенаправляем пользователя на страницу подтверждения отправки email
        return redirect("user:email_confirmation_sent")


# Класс для обновления профиля пользователя (данных профиля), LoginRequiredMixin - проверяет, залогинен ли пользователь
class UserProfileView(LoginRequiredMixin, UpdateView):  # CacheMixin
    # Имя шаблона для отображения профиля пользователя
    template_name = "user/profile.html"
    # Форма для обновления профиля пользователя
    form_class = ProfileForm
    # URL, на которую будет перенаправлен пользователь после успешного обновления профиля
    success_url = reverse_lazy("user:profile_page")

    # Функция для получения объекта пользователя
    def get_object(self, queryset=None):
        # Получаем объект пользователя
        return self.request.user

    # Функция для проверки формы для обновления профиля пользователя
    def form_valid(self, form):
        # Выводим сообщение об успешном обновлении профиля
        messages.success(self.request, f"Профиль успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f"Произошла ошибка при обновлении профиля")
        return super().form_invalid(form)

    # Функция для получения контекста для шаблона профиля пользователя
    def get_context_data(self, **kwargs):
        # Получаем контекст для шаблона профиля пользователя
        context = super().get_context_data(**kwargs)
        orders = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product_variant"),
                )
            )
            .order_by("-created_timestamp")
        )

        context["orders"] = orders

        return context


class UserCartView(TemplateView):  # Класс для отображения корзины пользователя
    template_name = (
        "user/user-cart.html"  # Имя шаблона для отображения корзины пользователя
    )


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, f"{request.user.username}, Вы успешно вышли из аккаунта")
    return redirect(reverse("shop:main_page"))
