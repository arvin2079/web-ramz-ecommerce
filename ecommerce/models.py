from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ecommerce.validation import validate_half_or_whole


# Category model uses the adjacency list pattern
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    class Meta:
        # because in django might makes this plural in Categorys form which is incorect
        # so we fix it here
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField("Tag", blank=True, related_name="products")

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5), validate_half_or_whole]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # from new to old
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating} from 5 for {self.product.name}"
