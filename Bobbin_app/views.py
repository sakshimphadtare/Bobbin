from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, WishlistItem, Review
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError, models
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
import json
from django.views.decorators.csrf import csrf_exempt

# ------------------ General Views -------------------

def test_base_template(request):
    return render(request, 'base.html')

def home_view(request):
    return render(request, "Bobbin_app/home.html")
# ------------------ Search -------------------

def search_suggestions(request):
    query = request.GET.get('term', '') or request.GET.get('q', '')
    suggestions = []

    if query:
        matches = Product.objects.filter(
            Q(name__istartswith=query) |
            Q(brand__istartswith=query) |
            Q(color__istartswith=query)
        ).values_list('name', flat=True).distinct()[:10]
        suggestions = list(matches)

    return JsonResponse({'suggestions': suggestions})

def search_page_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(brand__icontains=query) |
        Q(material__icontains=query) |
        Q(color__icontains=query) |
        Q(category__icontains=query)
    ) if query else []

    wishlist_products = []
    if request.user.is_authenticated:
        wishlist_products = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'Bobbin_app/search_results.html', {
        'products': products,
        'query': query,
        'wishlist_products': wishlist_products,
    })

# ------------------ Product List -------------------

def product_list_view(request):
    products = Product.objects.all()
    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__icontains=query)
        ).distinct()

    wishlist_products = []
    if request.user.is_authenticated:
        wishlist_products = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    materials = ['Cotton', 'Linen', 'Denim', 'Flannel', 'Silk', 'Polyester', 'Rayon / Viscose', 'Blends']
    sizes = ['S', 'M', 'L', 'XL', 'XXL']
    colors = ['Black', 'White', 'Blue', 'Grey', 'Beige', 'Green', 'Brown', 'Red', 'Yellow', 'Pink']
    styles = ['Casual', 'Formal', 'Streetwear', 'Traditional', 'Partywear', 'Oversized']

    carousel_images = ['hero_image.jpg', 'hero_image2.jpg', 'hero_image3.jpg']

    context = {
        'products': products,
        'page_title': 'All Men\'s Tops' if not query else f'Search Results for "{query}"',
        'query': query,
        'wishlist_products': wishlist_products,
        'materials': materials,
        'sizes': sizes,
        'colors': colors,
        'styles': styles,
        'carousel_images': carousel_images,
    }
    return render(request, 'Bobbin_app/product_list.html', context)

# ------------------ Product Detail -------------------

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Images for carousel
    images = []
    for i in range(1, 4):
        img = getattr(product, f'image{i}', None)
        if img:
            images.append(img.url)

    # Safe handling of size options
    size_options = []
    if hasattr(product, "size_options") and product.size_options:
        size_options = [s.strip() for s in product.size_options.split(",") if s.strip()]
    else:
        size_options = ['S', 'M', 'L', 'XL']

    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'images': images,
        'sizes': size_options,
        'page_title': product.name,
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'Bobbin_app/product_detail.html', context)

# ------------------ Registration / Login / Logout -------------------

def user_registration_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Account created for {user.email}! You are now logged in.')
                return redirect('home')
            except IntegrityError:
                form.add_error('email', 'This email is already registered. Try logging in.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Bobbin_app/register.html', {'form': form, 'page_title': 'Register'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged in successfully!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'Bobbin_app/login.html', {'form': form, 'page_title': 'Login'})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# ------------------ Cart -------------------

@login_required
@require_POST
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    selected_size = request.POST.get('selected_size', '').strip()

    if not selected_size:
        return JsonResponse({'success': False, 'message': 'Please select a size before adding to cart.'})

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        size=selected_size,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'success': True, 'message': f'Added "{product.name}" (Size: {selected_size}) to your cart.'})

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'Bobbin_app/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'page_title': 'Your Cart'})

@login_required
@require_POST
def remove_from_cart_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return JsonResponse({'success': True, 'message': f'Removed "{cart_item.product.name}" from your cart.'})

@login_required
@require_POST
def increase_quantity_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({'success': True})

@login_required
@require_POST
def decrease_quantity_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return JsonResponse({'success': True})

def cart_item_count_context_processor(request):
    count = CartItem.objects.filter(user=request.user).aggregate(total=models.Sum('quantity'))['total'] or 0 if request.user.is_authenticated else 0
    return {'cart_count': count}

# ------------------ Wishlist -------------------

@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

    if created:
        return JsonResponse({
            'status': 'added',
            'success': True,
            'message': f'Added "{product.name}" to your wishlist.'
        })
    else:
        wishlist_item.delete()
        return JsonResponse({
            'status': 'removed',
            'success': True,
            'message': f'Removed "{product.name}" from your wishlist.'
        })

@login_required
def view_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'Bobbin_app/wishlist.html', {'wishlist_items': wishlist_items, 'page_title': 'Your Wishlist'})

# ------------------ Buy Now -------------------

@login_required
def buy_now_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    selected_size = request.GET.get('size', '').strip()
    if not selected_size:
        messages.error(request, 'Please select a size before purchasing.')
        return redirect('product_detail', pk=product.id)

    CartItem.objects.filter(user=request.user).delete()
    CartItem.objects.create(user=request.user, product=product, quantity=1, size=selected_size)
    messages.success(request, f'"{product.name}" (Size: {selected_size}) added to cart. Proceeding to checkout...')
    return redirect('view_cart')

# ------------------ Style Filter -------------------

def products_by_style(request, style_name):
    products = Product.objects.filter(category__iexact=style_name)
    wishlist_products = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []

    return render(request, 'Bobbin_app/products_by_style.html', {
        'products': products,
        'wishlist_products': wishlist_products,
        'style_name': style_name,
        'page_title': f'{style_name} Styles',
    })

# ------------------ Pincode Save API -------------------

@csrf_exempt
@login_required
def save_pincode(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request.session["saved_pincode"] = data.get("pincode")
        request.session["saved_address"] = data.get("address")
        return JsonResponse({"success": True, "message": "Pincode and address saved."})
    return JsonResponse({"error": "Invalid request"}, status=400)

# ------------------ Add Review -------------------

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        if comment:
            Review.objects.create(product=product, user=request.user, comment=comment)
            messages.success(request, "Your review has been submitted.")
    return redirect('product_detail', pk=product.id)
