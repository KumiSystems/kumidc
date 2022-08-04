from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages


class PasswordChangeView(DjangoPasswordChangeView):
    success_url = reverse_lazy("frontend:dashboard")
    template_name = "frontend/change_password.html"

    def form_valid(self, form):
        messages.success(self.request, "Your password was changed successfully.")
        return super().form_valid(form)