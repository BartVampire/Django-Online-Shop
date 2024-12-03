from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models.product import Product, ProductProxy
from .models.category import Category
from .models.brand import Brand


class ProductViewTest(TestCase):
    def test_get_products(self):
        def setUp(self):
            # Создаем тестовые данные
            self.category = Category.objects.create(
                name="Category 1", slug="category-1"
            )
            self.brand = Brand.objects.create(name="Brand 1", slug="brand-1")

            # Создаем несколько продуктов
            self.product1 = ProductProxy.objects.create(
                name="Product 1", category=self.category, brand=self.brand, price=100
            )
            self.product2 = ProductProxy.objects.create(
                name="Product 2", category=self.category, brand=self.brand, price=200
            )
            self.product3 = ProductProxy.objects.create(
                name="Product 3", category=self.category, brand=self.brand, price=300
            )

        def test_category_products_list_view(self):
            # Получаем URL для представления
            response = self.client.get(
                reverse(
                    "shop:category_products_list", kwargs={"slug": self.category.slug}
                )
            )

            # Проверяем статус ответа
            self.assertEqual(response.status_code, 200)

            # Проверяем, что контекст содержит ожидаемые данные
            self.assertIn("categories", response.context)
            self.assertIn("brands", response.context)
            self.assertIn("new_products", response.context)
            self.assertIn("all_products", response.context)

            # Проверяем, что в контексте есть правильные категории
            self.assertEqual(len(response.context["categories"]), 1)
            self.assertEqual(response.context["categories"][0], self.category)

            # Проверяем, что в контексте есть правильные бренды
            self.assertEqual(len(response.context["brands"]), 1)
            self.assertEqual(
                response.context["brands"][0][1], self.brand.name
            )  # Проверяем имя бренда

            # Проверяем, что в контексте есть все продукты
            self.assertEqual(len(response.context["all_products"]), 3)
            self.assertIn(self.product1, response.context["all_products"])
            self.assertIn(self.product2, response.context["all_products"])
            self.assertIn(self.product3, response.context["all_products"])

        def test_category_products_list_view_without_slug(self):
            # Проверяем, что происходит, если slug не передан
            response = self.client.get(reverse("shop:category_products_list"))

            # Проверяем статус ответа
            self.assertEqual(response.status_code, 200)

            # Проверяем, что контекст содержит все продукты
            self.assertIn("all_products", response.context)
            self.assertEqual(
                len(response.context["all_products"]), 3
            )  # Все продукты должны быть в контексте
