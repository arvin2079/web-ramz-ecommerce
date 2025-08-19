from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError
from ecommerce.models import Product


@transaction.atomic
def process_order(order_items):
    product_ids = [item["product_id"] for item in order_items]
    products = Product.objects.select_for_update().filter(id__in=product_ids)

    # maping id to product objects for easier comparing
    product_map = {p.id: p for p in products}
    for item in order_items:
        product = product_map.get(item["product_id"])
        if not product:
            raise ValidationError(f"product with id {item['product_id']} not exists.")
        if product.stock_quantity < item["quantity"]:
            raise ValidationError(f"stock quantity not enouph for {product.name}.")

    # using F function to update stock quantity directly in the database.
    for item in order_items:
        Product.objects.filter(id=item["product_id"]).update(
            stock_quantity=F("stock_quantity") - item["quantity"]
        )
