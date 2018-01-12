from django.contrib import admin

from .models import Species, Image


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'binomial_name')
    readonly_fields = (
        'slug', 'binomial_name', 'ncbi_taxonomy_html', 'display_image'
    )
    fieldsets = [
        (u'Main', {'fields': (
            'common_name', 'binomial_name', 'slug', 'image', 'display_image'
        )}),
        (u'Taxonomy', {'fields':  (
            'species', 'genus', 'subfamily', 'family', 'order', 'class_name',
            'phylum',
        )}),
        (u'NCBI', {'fields': ('ncbi_id', 'ncbi_taxonomy_html')})
    ]


class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ('display_image',)
    fields = ('page_url', 'file_url', 'attribution', 'display_image')


admin.site.register(Species, SpeciesAdmin)
admin.site.register(Image, ImageAdmin)
