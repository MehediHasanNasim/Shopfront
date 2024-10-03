from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from .models import *
from django.db.models import Count


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']
    
    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''
     
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    autocomplete_fields = ['collection']
    search_fields = ['title']
    # inlines = [TagInline] 
    prepopulated_fields = {
        'slug': ['title']
    }
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update']
    list_per_page = 15
    list_select_related = ['collection']


    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 15000:
            return 'LOW'
        return 'Ok'
    
    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderItemInline(admin.TabularInline):

    model = OrderItem
    autocomplete_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']


    
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        return collection.products_count
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            products_count=Count('products')  # Note: Use 'products' instead of 'product'
        )
        return queryset
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         products_count=Count('product')
    #     )


admin.site.register(Promotion)
# admin.site.register(Collection)
# admin.site.register(Product)
# admin.site.register(Customer)
# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
