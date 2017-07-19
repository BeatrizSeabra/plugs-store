from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from plugs_store import models


class ItemCategorySerializer(serializers.ModelSerializer):
     """
     Item Category Serializer
     """

     # pylint: disable=R0903
     class Meta:
          """
          Metaclass definition
          """
          model = models.ItemCategory
          fields = ('id', 'name', 'is_hidden', 'created', 'updated')


class ItemSerializer(serializers.ModelSerializer):
     """
     Item Serializer
     """

     # pylint: disable=R0903
     class Meta:
          """
          Metaclass definition
          """
          model = models.Item
          fields = ('id', 'name', 'description', 'price', 'avatar', 'item_category', 'created', 'updated')


class OrderSerializer(serializers.ModelSerializer):
    """
    Order Serializer
    """
    def __init__(self, *args, **kwargs):
        """
        Dealing with extra read_only_fields
        """
        super(OrderSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method in ['POST']:
            self.fields['state'].read_only = True
        if self.context['request'].user.is_staff:
            self.fields['user'].read_only = False
            self.fields['total'].read_only = False
            self.fields['payment_id'].read_only = False
            self.fields['state'].read_only = False

    def validate(self, data):
        if 'user' not in data:
            data['user'] = self.context['request'].user
        if self.instance is None:
            items = models.OrderItem.objects.filter(user=data['user'], order=None)
            if not items.exists():
                if not self.fields['user'].read_only:
                    raise serializers.ValidationError({'user': [_('You have no items to checkout.')]})
                else:
                    raise serializers.ValidationError({'name': [_('Order cannot be created if user has no items to checkout.')]})
            if 'payment_type' not in data:
                raise serializers.ValidationError({'payment_type': [_('Order cannot be created without choosing a payment type.')]})
        elif not self.context['request'].user.is_staff and 'state' in data and data['state'] != 'CANCELED':
            raise serializers.ValidationError({'state': [_('You can only change order state to canceled.')]})
        return data


    class Meta:
        """
        Metaclass definition
        """
        model = models.Order
        fields = ('id', 'name', 'user', 'total', 'state', 'payment_type', 'payment_id', 'shipping', 'created', 'updated')
        read_only_fields = ('user', 'total', 'payment_id')


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Order Item Serializer
    """
    def __init__(self, *args, **kwargs):
        """
        Dealing with extra read_only_fields
        """
        super(OrderItemSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].user.is_staff:
            self.fields['user'].read_only = False
            self.fields['order'].read_only = False
            self.fields['price'].read_only = False

    def validate(self, data):
        if self.instance is None and 'user' not in data:
            data['user'] = self.context['request'].user
        return data

    class Meta:
        """
        Metaclass definition
        """
        model = models.OrderItem
        fields = ('id', 'order', 'item', 'quantity', 'price', 'user', 'created', 'updated')
        read_only_fields = ('order', 'price', 'user')


class PaymentTypeSerializer(serializers.ModelSerializer):
    """
    Payment Type Serializer
    """

    class Meta:
        """
        Metaclass definition
        """
        model = models.PaymentType
        fields = ('id', 'name', 'description', 'avatar', 'app', 'model', 'created', 'updated')


class ShippingSerializer(serializers.ModelSerializer):
    """
    Shipping Serializer
    """
    def __init__(self, *args, **kwargs):
        """
        Dealing with extra read_only_fields
        """
        super(ShippingSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].user.is_staff:
            self.fields['date'].read_only = False
            self.fields['fee'].read_only = False

    # pylint: disable=R0903
    class Meta:
        """
        Metaclass definition
        """
        model = models.Shipping
        fields = ('id', 'address', 'date', 'fee', 'created', 'updated')
        read_only_fields = ('date', 'fee')
