from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class UserIsNotAuthenticated(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(
                self.request, "Вы уже авторизованы. Вы не можете посетить эту страницу."
            )
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect("shop:main_page")
