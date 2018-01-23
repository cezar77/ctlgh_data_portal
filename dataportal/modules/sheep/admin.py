from django.contrib.gis import admin

from .models import Population, Sampling, Animal


class SamplingAdmin(admin.GeoModelAdmin):
    list_display = ['date', 'population', 'locality']
    num_zoom = 6
    modifiable = False

admin.site.register(Population)
admin.site.register(Sampling, SamplingAdmin)
admin.site.register(Animal)
