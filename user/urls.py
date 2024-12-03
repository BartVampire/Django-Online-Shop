from django.urls import path
from .views import (
    logout,
    UserLoginView,
    UserRegistrationView,
    UserProfileView,
    UserCartView,
)
from .view.email_views import (
    EmailConfirmationSentView,
    EmailConfirmedView,
    EmailConfirmationFailedView,
    UserConfirmEmailView,
)
from .view.user_password_views import (
    UserForgotPasswordView,
    UserPasswordResetConfirmView,
)

app_name = "user"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login_page"),
    path("registration/", UserRegistrationView.as_view(), name="registration_page"),
    path("profile/", UserProfileView.as_view(), name="profile_page"),
    path("user-cart/", UserCartView.as_view(), name="user_cart_page"),
    path("logout/", logout, name="logout_page"),
    path(
        "email-confirmation-sent/",
        EmailConfirmationSentView.as_view(),
        name="email_confirmation_sent",
    ),
    path(
        "confirm-email/<str:uidb64>/<str:token>/",
        UserConfirmEmailView.as_view(),
        name="confirm_email",
    ),
    path("email-confirmed/", EmailConfirmedView.as_view(), name="email_confirmed"),
    path(
        "confirm-email-failed/",
        EmailConfirmationFailedView.as_view(),
        name="email_confirmation_failed",
    ),
    path("password-reset/", UserForgotPasswordView.as_view(), name="password_reset"),
    path(
        "set-new-password/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
