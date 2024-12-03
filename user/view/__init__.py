__all__ = [
    "EmailConfirmedView",
    "EmailConfirmationSentView",
    "EmailConfirmationFailedView",
]

from .email_views import (
    EmailConfirmationSentView,
    EmailConfirmationFailedView,
    EmailConfirmedView,
)
from .user_password_views import UserForgotPasswordView, UserPasswordResetConfirmView
