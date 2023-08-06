from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from foledol.django.tools.table import TableColumn, TableView

from ..models import Column


class ColumnTable(TableView):
    def __init__(self, rows):
        super().__init__(rows, [
            TableColumn('label', "Libellé")
        ], path='django:columns', search=True)
        self.update = 'django:column_update'
        self.create = 'django:column_create'

    def select(self, search, order_by, filter_key):
        if len(search) > 0:
            return Column.objects.filter(label=search)
        return Column.objects.all()


@login_required
@staff_member_required
def column_list(request):
    return ColumnTable(None).render(request)
