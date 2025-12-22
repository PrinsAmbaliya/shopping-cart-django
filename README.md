# Shopping Cart Django Project

## Overview

This is a fully functional e-commerce shopping cart application built using the Django web framework. The project allows users to browse products, add them to a cart, manage cart items, and proceed through a simple checkout process. It also includes a separate blog application for posting articles (e.g., product reviews or news).

The application demonstrates core Django concepts including models, views, templates, forms, authentication, session-based cart management, and admin customization.

Key features:
- Product catalog with categories
- Session-based shopping cart (works for both anonymous and authenticated users)
- Basic checkout simulation
- User authentication (register, login, logout)
- Blog section
- Responsive UI using Bootstrap

## Features

- Browse products by category or search
- View detailed product information with images
- Add/remove/update items in the shopping cart
- Persistent cart using Django sessions
- Simple checkout form (order creation, no payment gateway)
- User registration and authentication
- Blog posts with create/read functionality
- Fully functional Django admin for managing products, categories, orders, and blog posts
- Responsive design with Bootstrap 5

## Technology Stack

- **Framework**: Django (Python)
- **Database**: SQLite (development), easily switchable to PostgreSQL/MySQL
- **Frontend**: HTML, CSS, Bootstrap 5, vanilla JavaScript
- **Image Handling**: Pillow
- **Authentication**: Django's built-in auth system

## Project Structure
```base
shopping-cart-django/
├── Ecommerce/                  # Project settings and configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/                       # Main e-commerce app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Product, Category, Order, etc.
│   ├── tests.py
│   ├── views.py                # Product list, detail, cart, checkout
│   ├── urls.py
│   ├── migrations/             # Database migration files
│   ├── static/shop/            # CSS, JS, images for shop app
│   └── templates/shop/         # Shop-specific templates
├── blog/                       # Blog application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Post model
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   ├── migrations/             # Database migration files
│   └── templates/blog/         # Blog-specific templates
├── media/                      # Uploaded product images
├── static/                     # Global static files (CSS, JS, images)
├── templates/                  # Base and global templates
├── manage.py                   # Django management script
├── db.sqlite3                  # Development database
└── README.md                   # This file
