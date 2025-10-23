from django.contrib import admin
from .models import Region, Country, State, City
from listings.models import Listing


class CityInline(admin.TabularInline):
    model = City
    extra = 0
    show_change_link = True


class StateInline(admin.TabularInline):
    model = State
    extra = 0
    show_change_link = True


class CountryInline(admin.TabularInline):
    model = Country
    extra = 0
    show_change_link = True


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [CountryInline]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    list_filter = ("region",)
    inlines = [StateInline]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)
    inlines = [CityInline]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "get_state", "get_country", "get_region", "listings_count")
    list_filter = ("state__country__region",)
    search_fields = ("name", "state__name", "state__country__name")

    def get_state(self, obj):
        return obj.state.name
    get_state.short_description = "Штат / Земля"

    def get_country(self, obj):
        return obj.state.country.name
    get_country.short_description = "Страна"

    def get_region(self, obj):
        return obj.state.country.region.name
    get_region.short_description = "Регион"

    def listings_count(self, obj):
        return Listing.objects.filter(city=obj).count()
    listings_count.short_description = "Объявлений"
