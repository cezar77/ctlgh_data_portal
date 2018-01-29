from django.contrib import admin

from .models import Study, Person


class StudyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Study, StudyAdmin)
admin.site.register(Person)
