from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class RatingFilter(SimpleListFilter):
    title = 'Рейтинг'
    parameter_name = 'rating_filter'

    def lookups(self, request, model_admin):
        return (
            ('good', _('good_film')),
            ('normal', _('normal_film')),
            ('bad', _('bad_film')),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'good':
            return queryset.filter(rating__gte=8.0)
        elif self.value().lower() == 'normal':
            return queryset.filter(rating__gte=6.0, rating__lt=8.0)
        elif self.value().lower() == 'bad':
            return queryset.filter(rating__lt=6.0)
