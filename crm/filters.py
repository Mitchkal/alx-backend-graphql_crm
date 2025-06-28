import django_filters
from .models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    """
    filters customers
    """

    name = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    created_at__gte = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at__lte = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    phone_starts_with = django_filters.CharFilter(method="filter_phone_starts_with")

    def filter_phone_starts_with(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)

    class Meta:
        model = Customer
        fields = [
            "name",
            "email",
            "created_at__gte",
            "created_at__lte",
            "phone_starts_with",
        ]
        order_by = django_filters.OrderingFilter(fields=(("name", "name"),))


class ProductFilter(django_filters.FilterSet):
    """
    product filter
    """

    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    stock = django_filters.NumberFilter(field_name="stock", lookup_expr="exact")
    stock__lte = django_filters.RangeFilter(field_name="stock", lookup_expr="lte")
    stock__gte = django_filters.RangeFilter(field_name="stock", lookup_expr="gte")
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = [
            "price",
            "stock",
            "price__gte",
            "price__lte",
            "stock__lte",
            "stock__gte",
            "name",
        ]

    order_by = django_filters.OrderingFilter(
        fields=(
            (
                "price",
                "stock",
            ),
        )
    )


class OrderFilter(django_filters.FilterSet):
    """
    Order filter
    """

    total_amount__gte = django_filters.NumberFilter(
        field_name="total_amount", lookup_expr="gte"
    )
    total_amount__lte = django_filters.NumberFilter(
        field_name="total_amount", lookup_expr="lte"
    )
    order_date__gte = django_filters.DateFilter(
        field_name="order_date", lookup_expr="gte"
    )
    order_date__lte = django_filters.DateFilter(
        field_name="order_date", lookup_expr="lte"
    )
    customer_name = django_filters.CharFilter(
        field_name="customer__name", lookup_expr="icontains"
    )
    product_name = django_filters.CharFilter(
        field_name="products__name", lookup_expr="icontains"
    )
    product_id = django_filters.NumberFilter(
        field_name="products__id", lookup_expr="exact"
    )

    def filter_product_id(self, queryset, name, value):
        return queryset.filter(product_id=value).distinct()

    class Meta:
        model = Order
        fields = [
            "total_amount__gte",
            "total_amount__lte",
            "order_date__gte",
            "order_date__lte",
            "customer_name",
            "product_name",
            "product_id",
        ]

    order_by = django_filters.OrderingFilter(fields=(("order_date", "order_date"),))
