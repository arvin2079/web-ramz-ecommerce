from django.contrib import admin

from ecommerce.models import Category, Tag, Product, Review


class SubCategoryInline(admin.TabularInline):
    """Inline editor to manage subcategories from parent category."""

    model = Category
    extra = 1
    fk_name = "parent"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_name")
    list_filter = ("parent",)
    search_fields = ("name",)
    inlines = [SubCategoryInline]

    def parent_name(self, obj):
        return obj.parent.name if obj.parent else "-"

    parent_name.short_description = "Parent"


class TagInline(admin.TabularInline):
    model = Product.tags.through
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock_quantity")
    list_filter = ("category", "tags")
    search_fields = ("name", "description")
    inlines = [TagInline]
    exclude = ("tags",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "rating", "short_comment", "created_at")
    list_filter = ("rating", "product")
    search_fields = ("comment", "product__name")
    ordering = ("-created_at",)

    def short_comment(self, obj):
        return (
            (obj.comment[:40] + "...")
            if obj.comment and len(obj.comment) > 40
            else obj.comment
        )

    short_comment.short_description = "Comment"
