from django.urls import path, include


from . import views

urlpatterns = [
    path('cart_add/<str:slug>/', views.CartAdd.as_view(), name='cart-add'),
    path('cart_get/', views.CartGet.as_view(), name='cart-get'),
]
