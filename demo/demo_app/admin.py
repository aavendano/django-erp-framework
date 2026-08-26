from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from erp_framework.admin.admin import EntityAdmin, TransactionAdmin, TransactionItemAdmin
from erp_framework.sites import erp_admin_site
from .models import Client, Product, Sale, SaleItem


class SaleItemInline(TransactionItemAdmin):
    model = SaleItem
    extra = 1
    fields = ('product', 'quantity', 'price', 'discount', 'value')
    readonly_fields = ('value',)


class ClientAdmin(EntityAdmin):
    list_display = ('name', 'slug', 'email', 'phone', 'owner', 'creation_date')
    search_fields = ('name', 'email', 'phone', 'slug')


class ProductAdmin(EntityAdmin):
    list_display = ('name', 'code', 'price', 'stock', 'category', 'owner')
    search_fields = ('name', 'code', 'category', 'slug')


class SaleAdmin(TransactionAdmin):
    list_display = ('slug', 'date', 'client', 'value', 'owner')
    search_fields = ('slug', 'client__name')
    inlines = [SaleItemInline]


class SaleItemAdmin(EntityAdmin):
    list_display = ('sale', 'product', 'quantity', 'price', 'discount', 'value')
    search_fields = ('sale__slug', 'product__name', 'product__code')
    readonly_fields = ('value',)


# Register models with ERP admin site at the bottom of the file
# This avoids issues with lazy object initialization during module import
erp_admin_site.register(Client, ClientAdmin)
erp_admin_site.register(Product, ProductAdmin)
erp_admin_site.register(Sale, SaleAdmin)
erp_admin_site.register(SaleItem, SaleItemAdmin)
