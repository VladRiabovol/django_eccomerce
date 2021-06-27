from django.urls import path, include


from . import views

urlpatterns = [
    path('cart_add/<str:slug>/<int:quantity>/', views.CartAdd.as_view(), name='cart-add'),
    path('cart_delete/<str:slug>/<int:quantity>', views.CartRemove.as_view(), name='cart-remove'),
    path('cart_get/', views.CartGet.as_view(), name='cart-get'),
    path('cart/', views.CartView.as_view(), name='cart-view')
]
