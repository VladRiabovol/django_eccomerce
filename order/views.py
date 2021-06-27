from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from . import models
from django.views import View
from django.urls import reverse
from product.models import Product


# Create your views here.


class CartAdd(View):
    def get(self, request, *args, **kwargs):
        cart = request.session['cart']
        try:
            cart[self.kwargs['slug']] += self.kwargs['quantity']
        except KeyError:
            cart[self.kwargs['slug']] = 1
        request.session.modified = True

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class CartRemove(View):
    def get(self, request, *args, **kwargs):
        cart = request.session['cart']
        if self.kwargs['quantity'] < cart[self.kwargs['slug']]:
            cart[self.kwargs['slug']] -= self.kwargs['quantity']
        else:
            del cart[self.kwargs['slug']]
        request.session.modified = True

        return redirect(reverse('cart-view'))


class CartGet(View):
    def get(self, request, *args, **kwargs):
        try:
            cart = request.session['cart']
            print(cart)
        except KeyError:
            cart = request.session['cart'] = {}
        cart_products = [item['product_slug'] for item in cart]

        return JsonResponse(cart)


class CartView(ListView):
    template_name = 'shopping_cart.html'

    def get_queryset(self):
        cart = self.request.session['cart']
        products = Product.objects.filter(slug__in=cart.keys())
        order_list = [{'product': product, 'quantity': cart[product.slug],
                       'total_price': product.price * cart[product.slug]}
                      for product in products]
        self.kwargs['order_list'] = order_list
        return order_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        price_list = [product['quantity'] * product['product'].price for product in self.kwargs['order_list']]
        context['price_list'] = price_list
        context['total_price'] = sum([item['total_price'] for item in self.kwargs['order_list']])
        return context


