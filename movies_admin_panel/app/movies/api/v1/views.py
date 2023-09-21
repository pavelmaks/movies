from typing import Any
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView


from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_person_via_role(self, role: str) -> ArrayAgg:
        return ArrayAgg('person__full_name', filter=Q(personfilmwork__role=role))

    def get_queryset(self):
        queryset = Filmwork.objects.prefetch_related('genres', 'person').values(
            'id', 'title', 'description', 'creation_date', 'rating', type=F('film_type')
        ).annotate(genres=ArrayAgg('genres__name', distinct=True))
        queryset = queryset.annotate(actors=self.get_person_via_role('actor'))
        queryset = queryset.annotate(directors=self.get_person_via_role('director'))
        queryset = queryset.annotate(writers=self.get_person_via_role('writer'))
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, Any]:
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return kwargs['object']
