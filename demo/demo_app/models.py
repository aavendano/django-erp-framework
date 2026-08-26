"""Demo App Models.

This module contains demo models that inherit from ERP Framework base models
to demonstrate the framework's capabilities.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from erp_framework.base.models import EntityModel, TransactionModel, QuantitativeTransactionItemModel


class Client(EntityModel):
    """
    Client model - inherits from EntityModel.
    Represents a customer/client in the system.
    """
    email = models.EmailField(
        _("Email"),
        unique=True,
        help_text=_("Client's email address")
    )
    phone = models.CharField(
        _("Phone"),
        max_length=20,
        blank=True,
        help_text=_("Client's phone number")
    )
    address = models.TextField(
        _("Address"),
        blank=True,
        help_text=_("Client's physical address")
    )
    
    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class Product(EntityModel):
    """
    Product model - inherits from EntityModel.
    Represents a product/item that can be sold.
    """
    code = models.CharField(
        _("Code"),
        max_length=50,
        unique=True,
        help_text=_("Unique product code")
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Product unit price")
    )
    stock = models.PositiveIntegerField(
        _("Stock"),
        default=0,
        help_text=_("Current stock quantity")
    )
    category = models.CharField(
        _("Category"),
        max_length=100,
        help_text=_("Product category")
    )
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code}) - ${self.price}"


class Sale(TransactionModel):
    """
    Sale model - inherits from TransactionModel.
    Represents a sales transaction.
    """
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name=_("Client"),
        related_name='sales',
        help_text=_("Client who made the purchase")
    )
    
    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")
        ordering = ['-date']
    
    def __str__(self):
        return f"Sale #{self.slug} - {self.client.name} - ${self.value}"


class SaleItem(QuantitativeTransactionItemModel):
    """
    Sale Item model - inherits from QuantitativeTransactionItemModel.
    Represents an item/line in a sale.
    Automatically calculates value based on quantity * price - discount.
    """
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        verbose_name=_("Sale"),
        related_name='items',
        help_text=_("Parent sale")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name='sale_items',
        help_text=_("Product being sold")
    )
    
    class Meta:
        verbose_name = _("Sale Item")
        verbose_name_plural = _("Sale Items")
        ordering = ['-sale__date']
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity} @ ${self.price} = ${self.value}"
    
    def save(self, *args, **kwargs):
        """Override save to set the product price as the item price."""
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
