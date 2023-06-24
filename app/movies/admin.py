from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from .custom_filters import RatingFilter
from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        'title',
        'film_type',
        'creation_date',
        'rating',
    )
    list_filter = (
        'film_type',
        ('creation_date', DateRangeFilter),
        RatingFilter,
    )
    search_fields = ('title', 'description', 'id')
