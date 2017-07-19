=====
Usage
=====

To use Plugs Store in a project, install it via pip and add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'plugs_store',
        ...
    )

Add Plugs Store's Views to ROUTER:

.. code-block:: python

    from plugs_store import views as store_views

    ROUTER.register(r'items', store_views.ItemViewSet)
    ROUTER.register(r'item-categories', store_views.ItemCategoryViewSet)
    ROUTER.register(r'orders', views.OrderViewSet)
    ROUTER.register(r'order-items', views.OrderItemViewSet)
    ROUTER.register(r'payment-types', views.PaymentTypeViewSet)
    ROUTER.register(r'shipping', views.ShippingViewSet)
    


    urlpatterns = [
        url(r'^', include(ROUTER.urls)),
        ...
    ]
