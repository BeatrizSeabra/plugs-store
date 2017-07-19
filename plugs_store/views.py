from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ModelViewSet

from plugs_filter.decorators import auto_filters
from plugs_store import permissions as api_permissions
from plugs_store.pagination import ClientRequestedPagination
from plugs_store import serializers, models


@auto_filters
class ItemCategoryViewSet(ModelViewSet):
    """
    Item Category ViewSet
    """
    queryset = models.ItemCategory.objects.all()
    serializer_class = serializers.ItemCategorySerializer
    permission_classes = [api_permissions.StaffOrReadOnly]
    pagination_class = ClientRequestedPagination
    auto_filters_fields = ('is_hidden', 'name')
    ordering_fields = ('id', 'name', 'created', 'updated')


@auto_filters
class ItemViewSet(ModelViewSet):
    """
    Item ViewSet
    """
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    permission_classes = [api_permissions.StaffOrReadOnly]
    pagination_class = ClientRequestedPagination
    auto_filters_fields = ('name', 'price', 'item_category', 'item_category__is_hidden')
    ordering_fields = ('id', 'name', 'price', 'item_category', 'created', 'updated')


@auto_filters
class OrderViewSet(ModelViewSet):
    """
    Order Viewset
    """
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Order.objects.all()
    auto_filters_fields = ('name', 'user', 'state', 'total', 'payment_type', 'payment_id')
    ordering_fields = ('id', 'name', 'user', 'state', 'total', 'payment_id', 'created', 'updated')

    def get_queryset(self):
        """
        View should return a list of orders for the current
        authenticated user
        """
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset


@auto_filters
class OrderItemViewSet(ModelViewSet):
    """
    Order Items Viewset
    """
    serializer_class = serializers.OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.OrderItem.objects.all()
    auto_filters_fields = ('order', 'item', 'item__item_category', 'price', 'user', 'quantity')
    ordering_fields = ('id', 'order', 'user', 'item', 'price', 'quantity', 'created', 'updated')

    def get_queryset(self):
        """
        View should return list of user's order items
        """
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset


class PaymentTypeViewSet(ModelViewSet):
    """
    Payment Type ViewSet
    """
    queryset = models.PaymentType.objects.all()
    serializer_class = serializers.PaymentTypeSerializer
    permission_classes = [api_permissions.AdminOrReadOnly]
    pagination_class = ClientRequestedPagination


class ShippingViewSet(ModelViewSet):
    """
    Shipping ViewSet
    """
    queryset = models.Shipping.objects.all()
    serializer_class = serializers.ShippingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ClientRequestedPagination
