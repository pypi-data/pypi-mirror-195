from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from foledol.django.tools.table import TableColumn, TableView

from ..models import Condition


class ConditionTables(TableView):
    def __init__(self, rows):
        super().__init__(rows, [
            TableColumn('label', "Libellé"),
            TableColumn('criteria', "Critère"),
            TableColumn('value', "Valeur")
        ], path='django:conditions', search=True)
        self.update = 'django:condition_update'
        self.create = 'django:condition_create'

    def select(self, search, order_by, filter_key):
        if len(search) > 0:
            return Condition.objects.filter(label=search)
        return Condition.objects.all()


@login_required
@staff_member_required
def condition_list(request):
    return ConditionTables(None).render(request)
