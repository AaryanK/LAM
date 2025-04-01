from django.db import models

class Aisle(models.Model):
    number = models.PositiveIntegerField(unique=True)
    description = models.TextField()

    def __str__(self):
        return f"Aisle {self.number}"
    
    def __int__(self):
        return self.number
    
    @staticmethod
    def as_int(self):
        return self.number


class Item(models.Model):
    name = models.CharField(max_length=100)
    aisle = models.ForeignKey(Aisle, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    case_quantity = models.PositiveIntegerField(default=1, help_text="Number of items per case")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_items_sold(self):
        return SaleData.objects.filter(item=self).aggregate(models.Sum('quantity_sold'))['quantity_sold__sum'] or 0

    @property
    def remaining_stock(self):
        total_sold = self.total_items_sold
        return self.count - total_sold


class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    items = models.ManyToManyField(Item, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


class OrderShipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])
    expected_delivery_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment for Order {self.order.order_number} - {self.shipment_status}"


class SaleData(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity_sold = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity_sold} of {self.item.name} sold on {self.sale_date}"
