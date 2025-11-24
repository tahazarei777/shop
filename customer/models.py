from turtle import Turtle
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    created_at = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="transactions")
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_addition = models.BooleanField(default=False)  # True = اضافه شده، False = کم شده

    def __str__(self):
        return f"{self.customer} - {self.amount} - {'+' if self.is_addition else '-'}"