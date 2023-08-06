import django.db.models
from django.conf import settings
from django.shortcuts import render as _render

from foledol.django.utils import paginate, get_param_from_get_or_request, new_context, get_action


class TableFilter:
    def __init__(self, key, label):
        self.key = key
        self.label = label


class TableButton:
    def __init__(self, label, action):
        self.label = label
        self.action = action


class TableButtonGroup:
    def __init__(self, label, items):
        self.label = label
        self.items = items


class TableButtonDivider:
    def __init__(self):
        None


class TableColumn:
    def __init__(self, key, name, type=None, value=None, method=None, link=None, sortable=False):
        self.key = key
        self.name = name
        self.type = type
        self.value = value
        self.method = method
        self.link = link
        self.sortable = sortable


class Table:
    def __init__(self, model, columns, rows=None, path=None, heading=None, create=None, update=None,
                 search=False, upload=False, filters=None, buttons=None, placeholder=None, sort='date_asc'):
        self.rows = rows
        self.count = rows.count if rows else 0
        self.model = model
        self.path = path
        self.sort = sort
        self.title = None
        self.columns = columns
        self.heading = heading
        self.create = create
        self.update = update
        self.search = search
        self.upload = upload
        self.filters = filters
        self.buttons = buttons
        self.template = 'table_view.html'
        self.placeholder = placeholder

    def sort(self, rows):
        pass

    def formatter(self, row):
        return ''


class TableView(Table):

    def select(self, rows, search, order_by):
        return rows

    def handle(self, request, context, action, rows):
        return False

    def get_space(self):
        segment = self.path.split(':')
        return segment[1] if len(segment) > 1 else segment[0]

    def get_rows(self, request, context):
        space = self.get_space()
        search = get_param_from_get_or_request(request, context, space, 'search', '').strip()
        order_by = get_param_from_get_or_request(request, context, space, 'sort', self.sort)
        filter_key = get_param_from_get_or_request(request, context, space, 'filter_key', None)
        rows = self.model.objects.all()
        if filter_key and filter_key in self.filters:
            rows = self.filters[filter_key].filter(rows)
        return self.select(rows, search, order_by)

    def render(self, request, context=new_context()):
        rows = self.get_rows(request, context)
        space = self.get_space()
        self.rows = paginate(request, context, rows, space=space)
        self.count = rows.count()
        context['base'] = settings.DEFAULT_SPACE + '/base.html'
        context['path'] = self.path
        context['sort'] = self.sort
        context['title'] = self.title
        context['table'] = self

        result = self.handle(request, context, get_action(request), rows)
        if result:
            return result

        return _render(request, self.template, context)
