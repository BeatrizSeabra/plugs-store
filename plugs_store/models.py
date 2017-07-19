# -*- coding: utf-8 -*-
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMField, transition, TransitionNotAllowed

from plugs_core.mixins import Timestampable
from plugs_media.fields import MediaField

#region Store
class ItemCategory(Timestampable):
    """
    Item Category Model
    """
    name = models.CharField(max_length=30, verbose_name=_('name'))
    is_hidden = models.BooleanField(default=False, blank=True)

    def __str__(self):
        """
        Python3 string representation
        """
        return self.name

    class Meta:
        verbose_name = _('item category')
        verbose_name_plural = _('item categories')


class Item(Timestampable):
    """
    Item Model
    """
    name = models.CharField(max_length=50, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('price'))
    avatar = MediaField(null=True, blank=True, verbose_name=_('avatar'))
    item_category = models.ForeignKey('ItemCategory', null=True, blank=True)

    def __str__(self):
        """
        Python3 string representation
        """
        return self.name

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')


class PaymentType(Timestampable):
    """
    Type of Payment Model
    """
    id = models.CharField(max_length=10, primary_key=True, unique=True, verbose_name=_('name'))
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True, verbose_name=_('description'))
    avatar = MediaField(null=True, blank=True, verbose_name=_('avatar'))

    def __str__(self):
        """
        Python3 string representation
        """
        return self.name

    class Meta:
        verbose_name = _('payment type')
        verbose_name_plural = _('payment types')


class Shipping(Timestampable):
    """
    Shipping Model
    """
    address = models.TextField(verbose_name=_('address'))
    date = models.DateTimeField(null=True, blank=True, verbose_name=_('date'))
    fee = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('fee'))

    def __str__(self):
        """
        Python3 string representation
        """
        return self.address

    class Meta:
        verbose_name = _('shipping')
        verbose_name_plural = _('shipping')


class Order(Timestampable):
    """
    Order Model
    """
    #region states
    CREATED = 'CREATED'
    IN_PAYMENT = 'IN_PAYMENT'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    CANCELED = 'CANCELED'
    INVALID = 'INVALID'

    STATES = [
        (CREATED, _('Created')),
        (IN_PAYMENT, _('In Payment')),
        (PAID, _('Paid')),
        (SHIPPED, _('Shipped')),
        (CANCELED, _('Canceled')),
        (INVALID, _('Invalid')),
    ]
    #endregion

    name = models.CharField(max_length=50, blank=True, verbose_name=_('name'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    total = models.DecimalField(default=0, max_digits=25, decimal_places=2, verbose_name=_('total'))
    payment_type = models.ForeignKey('PaymentType')
    payment_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('payment_id'))
    state = FSMField(null=False, blank=True, default=CREATED, choices=STATES, verbose_name=_('state'))
    shipping = models.ForeignKey('Shipping', null=True, blank=True)

    #region transitions
    @transition(field=state, source=[CREATED, IN_PAYMENT], target=INVALID)
    def to_invalid(self):
        pass

    @transition(field=state, source=[CREATED, IN_PAYMENT, PAID], target=CANCELED)
    def to_canceled(self):
        pass

    @transition(field=state, source=PAID, target=SHIPPED)
    def to_shipped(self, data):
        if data is not None:
            self.shipping.date = data
        else:
            self.shipping.date = timezone.now()
        self.shipping.save()

    @transition(field=state, source=[CREATED, IN_PAYMENT], target=PAID)
    def to_paid(self):
        pass

    @transition(field=state, source=CREATED, target=IN_PAYMENT)
    def to_in_payment(self):
        pass
    #endregion

    def get_total(self):
        return self.total

    def checkout_items(self):
        """
        Fetch order item with order null and update it with order id
        """
        order_items = OrderItem.objects.filter(user=self.user, order=None)
        for item in order_items:
            item.order = self
            item.save()

    def compute_total(self):
        self.total = OrderItem.objects.filter(order=self).aggregate(models.Sum('price'))['price__sum']

    def create_payment(self):
        # generate payment instead of payment=None
        payment = None
        if payment is not None:
            self.payment_id = payment.pk
            self.to_in_payment()

    def save(self, *args, **kwargs):
        """
        Overrides save method
        """
        if not self.pk:
            super(Order, self).save(*args, **kwargs)
            self.checkout_items()
            self.compute_total()
            self.create_payment()
            self.save()
        else:
            super(Order, self).save(*args, **kwargs)

    def __str__(self):
        """
        Python3 string representation
        """
        return self.name

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderItem(Timestampable):
    """
    Order Item Model
    """
    order = models.ForeignKey('Order', null=True, blank=True, verbose_name=_('order'))
    item = models.ForeignKey('Item', verbose_name=_('item'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    quantity = models.PositiveIntegerField(default=1, blank=True, verbose_name=_('quantity'))
    price = models.DecimalField(blank=True, max_digits=22, decimal_places=2, verbose_name=_('price'))

    def __str__(self):
        """
        Python3 string representation
        """
        return '{0} ordered'.format(self.item)

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
#endregion


@receiver(pre_save, sender=OrderItem)
def calculate_order_item_price(instance, sender, **kwargs):
    instance.price = instance.quantity * instance.item.price
