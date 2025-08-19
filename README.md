# WebRamzEcommerce

A simple Django project to manage a product catalog with categories, tags, and reviews, exposed via a RESTful API using Django REST Framework (DRF).  

---

## Features

- **Categories**: Supports hierarchical categories with parent-child relationships.  
- **Products**: Each product belongs to a category and can have multiple tags.  
- **Tags**: Organize products using tags like `new-arrival` or `on-sale`.  
- **Reviews**: Customers can leave ratings (1-5) and comments for products.  
- **Optimized API**: Prevents N+1 query problems using `select_related`, `prefetch_related`, and `annotate`.  
- **Filtering**: Filter products by category and tags using DRF `DjangoFilterBackend`.  
- **Permissions**: Read-only access for regular users, full access for admins (`IsAdminOrReadOnly`).  
- **Transaction-safe orders**: Stock updates are atomic and roll back on insufficient stock.  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/arvin2079/web-ramz-ecommerce.git
cd WebRamzEcommerce