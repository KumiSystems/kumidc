from django.template.loader import render_to_string

from authentication.mixins.timeout import TimeoutMixin

from oidc_provider.models import Client
from ajax_datatable.views import AjaxDatatableView


class ClientDataView(TimeoutMixin, AjaxDatatableView):
    model = Client
    title = "My Apps"
    initial_order = [["date_created", "asc"], ]

    column_defs = [
        {
            'name': '',
            'visible': True,
            'defaultContent': render_to_string('frontend/datatables/client_list.html'),
            "className": 'dataTables_row-tools',
            'width': 30,
        },
        {'name': 'id', "visible": False},
        {'name': 'name', 'visible': True, },
        {'name': 'client_id', 'visible': True, },
        {'name': 'date_created', 'visible': True, }
    ]

    def get_initial_queryset(self, request):
        queryset = self.model.objects.filter(owner=request.user)
        return queryset

    
