from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
from store_front.models import Customer
from django.db.models.aggregates import Avg,Count,Sum,Min,Max
from django.db.models import Q,F,Value,  Func, ExpressionWrapper


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title', 'unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_per_page=10
    list_select_related=['collection']
    list_filter=['collection','last_update']
    def collection_title(self,product):
        return product.collection.title
    @admin.display()
    def inventory_status(self,product):
        if product.inventory<10:
            return 'low'
        return 'ok'
     
    
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    
    list_display=['first_name', 'last_name','membership','count_order']
    list_editable=['membership']
    list_per_page=10
    search_fields=['first_name__istartswith']
    @admin.display(ordering='count_order')
    def count_order(self,order):
        return order.count_order
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(count_order=Count(F('order')))
  
  
  
  
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['placed_at', 'payment_status','customer']
    list_editable=['payment_status']
    list_per_page=10 
    list_select_related=['customer']
    
    
    
           
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['id','title','product_count']
    
    @admin.display(ordering='product_count')
    def product_count(self,count):
        return count.product_count
    #get_queryset is builtin function in admin site options
    def get_queryset(self, request ):
        return super().get_queryset(request).annotate(product_count=Count(F('product')))

