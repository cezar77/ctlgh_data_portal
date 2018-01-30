from django.utils.html import format_html

import django_tables2 as tables
from django_tables2 import A

from .models import Animal


class AnimalTable(tables.Table):
    id = tables.LinkColumn(
        viewname='chickens:animal-detail',
        kwargs={'pk': A('pk')},
        accessor='animal_id',
        orderable=False
    )
    animal_sex = tables.Column()

    class Meta:
        model = Animal
        template = 'django_tables2/bootstrap.html'

    def render_animal_sex(self, value):
        html = '<i class="fa{fa}"></i>'
        if value == 'female':
            fa_class = ' fa-venus'
        elif value == 'male':
            fa_class = ' fa-mars'
        else:
            fa_class = ''
        return format_html(html, fa=fa_class)
