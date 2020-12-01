from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created_at')
    list_display_links = ('id', 'image')
    search_fields = ('image',)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    max_num = 10
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'price', 'category', 'count', 'model', 'created_at', 'get_photo', 'views')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ]
    readonly_fields = ('views', 'created_at', 'update_at')

    def get_photo(self, obj):
        if obj.head_images:
            return mark_safe(f'<img src = "{obj.head_images.url}" width="50">')
        return '-'

    get_photo.short_description = 'Миниатюра'


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(View)
