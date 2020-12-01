from django.shortcuts import render
from django.utils.functional import SimpleLazyObject

from .models import *
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.contrib.auth.models import User


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

    def get_context_data(self, **kwargs):
        if str(self.request.user) != "AnonymousUser":
            view = View(views_by=self.request.user, product_id=self.object.id)
            view.save()

        context = super().get_context_data(**kwargs)

        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class Shop(ListView):
    model = Product
    template_name = 'ecommerce/shop.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        if self.kwargs:
            return Product.objects.filter(category__slug=self.kwargs['slug'])
        else:
            return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs:
            context['title_category'] = str(Category.objects.get(slug=self.kwargs['slug']))

        return context


def cart(request):
    return render(request, 'ecommerce/cart.html')
