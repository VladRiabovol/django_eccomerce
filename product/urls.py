from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<str:category>/', views.CategoryListView.as_view(), name='category-list'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
]