from django.contrib import admin

from .models import Farm, Animal, Relatedness

# Register your models here.
admin.site.register(Farm)
admin.site.register(Animal)
admin.site.register(Relatedness)
