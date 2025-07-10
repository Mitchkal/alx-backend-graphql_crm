from django.core.management.base import BaseCommand
from crm.models import Customer, Product, Order
from django.db import transaction
import random
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with initial Customers, Products, and Orders"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))
        self.clear_data()
        self.create_customers()
        self.create_products()
        self.create_orders()
        self.stdout.write(self.style.SUCCESS("Database successfully seeded."))

    def clear_data(self):
        Order.objects.all().delete()
        Customer.objects.all().delete()
        Product.objects.all().delete()

    def create_customers(self, count=10):
        self.customers = []
        for _ in range(count):
            customer = Customer.objects.create(
                name=fake.name(), email=fake.unique.email(), phone=fake.phone_number()
            )
            self.customers.append(customer)

    def create_products(self, count=10):
        self.products = []
        for _ in range(count):
            product = Product.objects.create(
                name=fake.unique.word().capitalize(),
                price=round(random.uniform(10.0, 500.0), 2),
                stock=random.randint(1, 100),
            )
            self.products.append(product)

    def create_orders(self, count=5):
        for _ in range(count):
            customer = random.choice(self.customers)
            selected_products = random.sample(self.products, k=random.randint(1, 3))
            total_price = sum(p.price for p in selected_products)
            order = Order.objects.create(customer=customer, total_amount=total_price)
            order.product.set(selected_products)
