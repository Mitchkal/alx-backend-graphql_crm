#!/bin/env python3
from django.db import models

# from datetime import datetime
import django.utils.timezone

# Create your models here.


class Customer(models.Model):
    """
    class definition for customer
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(null=True, blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Model for products
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    model for orders
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                       default=0.00)
