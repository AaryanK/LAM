from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=150)
    barcode = models.CharField(max_length=50, unique=True,null=True, blank=True)
    count = models.IntegerField(default=0)       # Individual units
    case_count = models.IntegerField(default=0)  # Number of full cases
    # reorder_threshold = models.IntegerField(default=10)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # last_restocked = models.DateTimeField(auto_now=True)

    # def is_low_stock(self):
    #     return self.count <= self.reorder_threshold

    def __str__(self):
        return f"{self.name} - {self.count} units"
