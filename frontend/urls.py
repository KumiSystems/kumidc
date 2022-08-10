from django.urls import path

from .views.dashboard import IndexView, DashboardView
from .views.password import PasswordChangeView
from .views.otp import TOTPActivationView, TOTPDeactivationView, TOTPDispatcherView
from .views.log import AuthorizationLogView
from .views.datatables.log import AuthorizationLogDataView
from .views.clients import ClientView, ClientEditView, ClientCreateView
from .views.datatables.clients import ClientDataView
from .views.profile import OwnProfileView


urlpatterns = [
    path("", IndexView.as_view()),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/", OwnProfileView.as_view(), name="profile"),
    path("profile/change_password/", PasswordChangeView.as_view(), name="change_password"),
    path("profile/totp/", TOTPDispatcherView.as_view(), name="totp"),
    path("profile/totp/activate/", TOTPActivationView.as_view(), name="activate_totp"),
    path("profile/totp/deactivate/", TOTPDeactivationView.as_view(), name="deactivate_totp"),
    path("authorizations/", AuthorizationLogView.as_view(), name="authorization_log"),
    path("authorizations/data/", AuthorizationLogDataView.as_view(), name="authorization_log_data"),
    path("apps/", ClientView.as_view(), name="client_list"),
    path("apps/data/", ClientDataView.as_view(), name="client_list_data"),
    path("apps/<int:pk>/edit/", ClientEditView.as_view(), name="client_edit"),
    path("apps/new/", ClientCreateView.as_view(), name="client_create"),
]