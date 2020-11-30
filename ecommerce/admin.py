from django.contrib import admin

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
    list_display = ('id', 'name', 'price', 'category', 'count', 'model', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ]
    readonly_fields = ('views', 'created_at', 'update_at')


admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Color)
admin.site.register(Brand)
