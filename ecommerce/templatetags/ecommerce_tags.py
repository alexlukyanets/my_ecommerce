from ecommerce.models import Category
from django import template
from django.db.models import Count

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    return categories
