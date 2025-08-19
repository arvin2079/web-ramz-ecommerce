from django.test import TestCase
from django.core.exceptions import ValidationError

from ecommerce.models import Category, Product
from ecommerce.services import process_order


class ProcessOrderTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="category 1")
        self.product1 = Product.objects.create(
            name="product 1", price=10.0, stock_quantity=5, category_id=category.pk
        )
        self.product2 = Product.objects.create(
            name="product 2", price=20.0, stock_quantity=2, category_id=category.pk
        )

    def test_order_rolls_back_when_not_enough_stock(self):
        order_items = [
            {"product_id": self.product1.id, "quantity": 3},
            {"product_id": self.product2.id, "quantity": 5},
        ]

        # should raise django validation error here
        with self.assertRaises(ValidationError):
            process_order(order_items)

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock_quantity, 5)
        self.assertEqual(self.product2.stock_quantity, 2)

    def test_order_is_processed_ok(self):
        order_items = [
            {"product_id": self.product1.id, "quantity": 3},
            {"product_id": self.product2.id, "quantity": 1},
        ]

        process_order(order_items)

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock_quantity, 2)
        self.assertEqual(self.product2.stock_quantity, 1)