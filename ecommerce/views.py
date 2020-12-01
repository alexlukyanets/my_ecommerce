from django.shortcuts import render, get_object_or_404, redirect
from django.utils.functional import SimpleLazyObject
from django.utils import timezone
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


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # chech if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.products.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_item)

    return redirect("product", slug=slug)

#48:53
def remove_from_card(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # chech if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_item)
        else:
            return redirect("product", slug=slug)


    else:
        # add a massage saying the user doesn't have an order
        return redirect("product", slug=slug)

    return redirect("product", slug=slug)
