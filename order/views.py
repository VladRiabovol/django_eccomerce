from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from . import models
from django.views import View
from django.urls import reverse
from product.models import Product
from .models import ShopCart, OrderProduct


# Create your views here.


class CartAdd(View):
    def get(self, request, *args, **kwargs):
        cart = request.session['cart']
        try:
            cart[self.kwargs['slug']] += 1
        except KeyError:
            cart[self.kwargs['slug']] = 1
        request.session.modified = True

        return redirect(reverse('product-list'))


class CartGet(View):
    def get(self, request, *args, **kwargs):
        try:
            cart = request.session['cart']
            print(cart)
        except KeyError:
            cart = request.session['cart'] = {}
        cart_products = [item['product_slug'] for item in cart]

        return JsonResponse(cart)
