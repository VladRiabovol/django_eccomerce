from django.shortcuts import render
from django.contrib import messages
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect

from product.models import Product, Category

# Create your views here.


def index(request):
    return HttpResponse("My Product Page")


class CategoryListView(ListView):
    template_name = 'category_product_list.html'
    paginate_by = 3

    def get_queryset(self):
        products = Product.objects.filter(category__slug=self.kwargs['category'])
        self.kwargs['count'] = products.count()
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['category'])
        context['categories_list'] = Category.objects.all().exclude(slug=context['category'].slug)
        context['product_count'] = self.kwargs['count']
        return context


class ProductListView(ListView):
    template_name = 'all_product_list.html'
    model = Product
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context
