from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from django.db.models import F


def item_list(request):
    # context = {
    #     "items": Item.objects.all()
    # }
    # print(context)
    return render(request, 'ecommerce/index.html')


class GetProduct(DetailView):
    model = Product
    template_name = 'ecommerce/product.html'
    context_object_name = 'product'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


def shop(request):
    return render(request, 'ecommerce/shop.html')


def cart(request):
    return render(request, 'ecommerce/cart.html')
