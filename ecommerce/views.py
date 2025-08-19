from django.db.models import Avg
from rest_framework import viewsets
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    BaseInFilter,
)

from config.permissions import IsAdminOrReadOnly
from ecommerce.models import Product
from ecommerce.serializers import ProductSerializer


# needed because in django-filter, CharFilter with lookup_expr="in" won’t 
# parse a list of values properly from query params
class CharInFilter(BaseInFilter, CharFilter):
    pass


class ProductFilter(FilterSet):
    category = CharFilter(field_name="category__name", lookup_expr="iexact")
    tags = CharInFilter(field_name="tags__name", lookup_expr="in")

    class Meta:
        model = Product
        fields = ["category", "tags"]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = (
            Product.objects.select_related("category")
            .prefetch_related("tags")
            .annotate(average_rating=Avg("reviews__rating"))
        )
        return queryset
