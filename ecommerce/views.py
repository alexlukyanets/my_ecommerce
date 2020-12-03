from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.functional import SimpleLazyObject
from django.utils import timezone
from .models import *
from django.views.generic import ListView, DetailView, View as Views
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *


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


class OrderSummaryView(LoginRequiredMixin, Views):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order
            }
            return render(self.request, 'ecommerce/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect('/')


def cart(request):
    return render(request, 'ecommerce/cart.html')


@login_required
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
            messages.info(request, "This item quantity was updated")
            return redirect("cart")
        else:
            order.products.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect("cart")

    else:
        ordered_date = timezone.now()

        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_item)
        messages.info(request, "This was added to your cart")

    return redirect("cart")


class CheckoutView(Views):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "ecommerce/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")


@login_required
def remove_from_card(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    for i in order_qs:
        print(i.products)
    if order_qs.exists():
        order = order_qs[0]
        # print(order.products)
        # chech if the order item is in the order
        # print(order.products.all())
        # print(order.products.filter(product__slug=product.slug))
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            print(order_item)
            order.products.remove(order_item)
            messages.info(request, "This was removed to your cart")
        else:
            messages.error(request, "This item was not in your cart")
            return redirect("product", slug=slug)


    else:
        messages.error(request, "You don't have an active order")
        return redirect("product", slug=slug)

    return redirect("product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.products.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)


def register(request):
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)

        if form.is_valid():
            messages.success(request, 'Вы успешно заригестрированы!')
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterFrom()

    return render(request, 'ecommerce/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginFrom(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginFrom()
    return render(request, 'ecommerce/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
