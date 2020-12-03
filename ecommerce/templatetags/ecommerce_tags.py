from ecommerce.models import Category, Order
from django import template
from django.db.models import Count

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    return categories


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].products.count()
    return 0


@register.filter
def cart_item_total (user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].get_total()
    return 0
