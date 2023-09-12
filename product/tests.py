from django.test import TestCase
from faker import Faker
from .models import Product
# Create your tests here.
fake = Faker()
record_count = 50

def generate_fake_data(count):
    for _ in range(count):  # Generate 10 fake records (you can change the number)
        # Create a new instance of your model with fake data
        Product.objects.create(
            name=fake.name(),
            price=fake.random_int(min=100, max=1000),
            stock=fake.random_int(min=1, max=100),
            description=fake.text())

generate_fake_data(record_count)
    