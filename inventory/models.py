from django.db import models
from django.utils import timezone

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, default="General")
    quantity = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=10)
    max_stock = models.IntegerField(default=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} units)"

    def needs_restock(self):
        return self.quantity <= self.min_stock

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity_sold = models.IntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(default=timezone.now)
    customer_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_sold} units"

    def total_revenue(self):
        return self.quantity_sold * self.sale_price