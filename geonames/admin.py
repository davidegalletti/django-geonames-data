# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (
   Country,
   GeonamesAdm1,
   GeonamesAdm2,
   GeonamesAdm3,
   GeonamesAdm4,
   GeonamesAdm5,
   PopulatedPlace,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(GeonamesAdm1)
class GeonamesAdm1Admin(admin.ModelAdmin):
    pass


@admin.register(GeonamesAdm2)
class GeonamesAdm2Admin(admin.ModelAdmin):
    pass


@admin.register(GeonamesAdm3)
class GeonamesAdm3Admin(admin.ModelAdmin):
    pass


@admin.register(GeonamesAdm4)
class GeonamesAdm4Admin(admin.ModelAdmin):
    pass


@admin.register(GeonamesAdm5)
class GeonamesAdm5Admin(admin.ModelAdmin):
    pass


@admin.register(PopulatedPlace)
class PopulatedPlaceAdmin(admin.ModelAdmin):
    pass



