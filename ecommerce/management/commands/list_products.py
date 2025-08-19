from django.core.management.base import BaseCommand
from django.db.models import Avg
from ecommerce.models import Product

"""
This command get and print all products with their related information.

with this way explained bellow we can prevent N+1 query problem (means hitting
database N more query for products or query with O(N) complexity):
- select_related("category") is used to fetch each product's category
  in the same query.
- prefetch_related("tags") fetches all tags for the selected products
  in a single additional query.
- annotate(Avg("reviews__rating")) computes the average rating for all
  products in the same query on database side (not python).

TOTAL QUERIES WILL BE: 1 (products + categories + avg rating) + 1 (tags) = 2 queries total.

"""


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        products = (
            Product.objects.select_related("category")
            .prefetch_related("tags")
            .annotate(avg_rating=Avg("reviews__rating"))
        )

        if products.count() == 0:
            self.stdout.write("no product found!")
            return

        for product in products:
            tags = ", ".join(tag.name for tag in product.tags.all()) or "no tag found"
            avg_rating = product.avg_rating if product.avg_rating else "no review found"
            self.stdout.write(
                f"Product: {product.name} | Price: ${product.price} | "
                f"Category: {product.category.name} | "
                f"Tags: {tags} | "
                f"Avg Rating: {avg_rating}"
            )
