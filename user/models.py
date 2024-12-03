from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from shop.mixins.id_primary_key import IdPrimaryKeyMixin


class User(
    IdPrimaryKeyMixin, AbstractUser
):  # Класс для регистрации новых пользователей
    # Проверка номера телефона с помощью регулярного выражения
    phone_regex = RegexValidator(
        regex=r"^(\+7|7|8)?9\d{9}$",
        message="Номер телефона должен быть в формате: '+79XXXXXXXXX' или '89XXXXXXXXX'.",
    )
    # Поле для ввода номера телефона
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Номер телефона",
    )

    class Meta:
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def clean(self):  # Метод для проверки уникальности номера телефона
        if self.phone_number:  # Если поле не пустое
            # Нормализация номера телефона с помощью метода normalize_phone_number
            normalized_number = self.normalize_phone_number(self.phone_number)

            # Проверка уникальности номера телефона по его нормализованному значению в базе данных User
            if (
                User.objects.filter(phone_number__endswith=normalized_number[-10:])
                .exclude(pk=self.pk)
                .exists()
            ):
                # Если такой номер телефона уже зарегистрирован, выбрасывается исключение ValidationError
                raise ValidationError(
                    {"phone_number": "Этот номер телефона уже зарегистрирован."}
                )
            # Если номер телефона корректен, то сохраняется его в поле phone_number
            self.phone_number = "+7" + normalized_number[-10:]

    # Метод для сохранения нормализованного номера телефона в базе данных
    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов метода full_clean, для того чтобы убедиться, что все проверки выполнены
        super().save(
            *args, **kwargs
        )  # Сохранение нормализованного номера телефона в базе данных

    @staticmethod  # Метод для нормализации номера телефона
    def normalize_phone_number(phone):
        phone = "".join(
            char for char in phone if char.isdigit()
        )  # Удаляет все символы, кроме цифр
        if len(phone) == 10 and phone.startswith(
            "9"
        ):  # Если длина номера 10 цифр и начинается с 9
            return "7" + phone  # Добавляет 7 в начало
        elif len(phone) == 11 and phone.startswith(
            "8"
        ):  # Если длина номера 11 цифр и начинается с 8
            return "7" + phone[1:]  # Удаляет первую цифру и добавляет 7 в начало
        return phone  # Возвращает нормализованный номер
