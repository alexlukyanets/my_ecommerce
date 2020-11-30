from django.conf import settings
from django.db import models
from colorfield.fields import ColorField
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True, blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    model = models.CharField(max_length=50, verbose_name='Модель', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    count = models.IntegerField(verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    colors = models.ManyToManyField('Color', blank=True)
    head_images = models.ImageField(upload_to='product_images/%Y/%m/%d/%H/%M/%S/', verbose_name='Фото', blank=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категории')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

class ProductImage(models.Model):
    def __str__(self):
        return self.image.name

    image = models.ImageField(max_length=300,
                              upload_to='product_images/%Y/%m/%d/%H/%M/%S/')
    product = models.ForeignKey(Product, related_name="images", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления', null=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'фото Товара'


class Color(models.Model):
    title = models.CharField(max_length=50)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['title']


class Brand(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бернды'
        ordering = ['title']