from django.urls import path
from .views import MainPageView, CategoryProductsListView, ProductDetailView

app_name = "shop"
urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("products/", CategoryProductsListView.as_view(), name="products_list"),
    path(
        "products/<slug:slug>/",
        CategoryProductsListView.as_view(),
        name="category_products",
    ),  # URL с slug
    path(
        "product/<slug:slug>/<str:article>",
        ProductDetailView.as_view(),
        name="product_details",
    ),
]
