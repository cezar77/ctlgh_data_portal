from django.contrib.gis import admin

from .models import Farm, Animal, Relatedness, Sampling


class FarmAdmin(admin.GeoModelAdmin):
    list_display = ['village', 'agroecology']
    num_zoom = 6
    modifiable = False

admin.site.register(Farm, FarmAdmin)
admin.site.register(Animal)
admin.site.register(Relatedness)
admin.site.register(Sampling)
