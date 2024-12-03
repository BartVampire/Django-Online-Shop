import random
import string
import datetime
from django.db import models


class BaseModel(models.Model):

    class Meta:
        # Базовая модель не будет иметь метаданных и не будет создана в базе данных
        abstract = True

    @classmethod
    def random_slug(cls):
        """
        Эта функция генерирует случайную строку длиной 3 символа, состоящую из строчных букв и цифр для slug категории.
        """
        return "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(3)
        )

    @classmethod
    def generate_unique_article(cls):  # Генерация уникального артикула
        timestamp = datetime.datetime.now(datetime.UTC).strftime(
            "%y%m%d%H%M"
        )  # 10 цифр: ГГММДДЧЧММ
        random_digits = "".join(
            [str(random.randint(0, 9)) for _ in range(2)]
        )  # 2 случайные цифры
        return f"{timestamp}{random_digits}"  # Всего 12 цифр
