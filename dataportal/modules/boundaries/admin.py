from django.contrib.gis import admin

from .models import (
    Country,
    FirstAdministrativeLevel,
    SecondAdministrativeLevel,
    ThirdAdministrativeLevel,
    FourthAdministrativeLevel,
    FifthAdministrativeLevel,
    AdministrativeRouter
)

admin.site.register(Country, admin.GeoModelAdmin)
admin.site.register(FirstAdministrativeLevel, admin.GeoModelAdmin)
admin.site.register(SecondAdministrativeLevel, admin.GeoModelAdmin)
admin.site.register(ThirdAdministrativeLevel, admin.GeoModelAdmin)
admin.site.register(FourthAdministrativeLevel, admin.GeoModelAdmin)
admin.site.register(FifthAdministrativeLevel, admin.GeoModelAdmin)
admin.site.register(AdministrativeRouter)
