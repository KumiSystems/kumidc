from django.views.generic import UpdateView

from core.models.profile import Profile


class ProfileUpdateView(UpdateView):
    model = Profile

    fields = [
        "first_name",
        "middle_name",
        "last_name",
        "nickname",
        "preferred_username",
        "website",
        "zoneinfo",
        "phone_number",
    ]


class OwnProfileView(ProfileUpdateView):
    template_name = "frontend/my_profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile