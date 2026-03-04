from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import save_pincode

urlpatterns = [
    # 🏠 Homepage
    path('', views.home_view, name='home'),

    # 🔍 Search
    path('search/', views.search_page_view, name='search_page'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),

    # 🛍️ Product Listing and Detail Pages
    path('products/', views.product_list_view, name='product_list'),
    path('products/all/', views.product_list_view, name='all_products'),
    path('products/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('style/<str:style_name>/', views.products_by_style, name='products_by_style'),

    # 📍 Pincode Save
    path('save-pincode/', save_pincode, name='save_pincode'),

    # 🧾 Authentication
    path('register/', views.user_registration_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),

    # 💖 Wishlist
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('toggle-wishlist/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # 🛒 Cart System
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now_view, name='buy_now'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('increase-quantity/<int:item_id>/', views.increase_quantity_view, name='increase_quantity'),
    path('decrease-quantity/<int:item_id>/', views.decrease_quantity_view, name='decrease_quantity'),

    # ✨ Review System
    path('products/<int:product_id>/add-review/', views.add_review, name='add_review'),
]