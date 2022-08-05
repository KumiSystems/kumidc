from authentication.mixins.timeout import TimeoutMixin
from core.models import AuthorizationLog

from ajax_datatable.views import AjaxDatatableView


class AuthorizationLogDataView(TimeoutMixin, AjaxDatatableView):
    model = AuthorizationLog
    title = "Authorizations"
    initial_order = [["timestamp", "desc"], ]

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'client', 'visible': True, 'foreign_field': 'client__name' },
        {'name': 'timestamp', 'visible': True, },
        {'name': 'granted', 'visible': True, }
    ]

    def get_initial_queryset(self, request):
        queryset = self.model.objects.filter(user=request.user)
        return queryset