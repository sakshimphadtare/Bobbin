from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('casual', 'Casual'),
        ('denim', 'Denim'),
        ('formal', 'Formal'),
        ('oversized', 'Oversized'),
        ('printed', 'Printed'),
        ('checked', 'Checked'),
        ('striped', 'Striped'),
        ('solid', 'Solid'),
        ('cuban', 'Cuban'),
        ('half sleeve', 'Half Sleeve'),
        ('full sleeve', 'Full Sleeve'),
    ]

    MATERIAL_CHOICES = [
        ('cotton', 'Cotton'),
        ('linen', 'Linen'),
        ('denim', 'Denim'),
        ('flannel', 'Flannel'),
        ('polyester', 'Polyester'),
        ('rayon', 'Rayon / Viscose'),
        ('blends', 'Blends'),
        ('silk', 'Silk'),
    ]

    COLOR_CHOICES = [
        ('white', 'White'),
        ('black', 'Black'),
        ('blue', 'Blue'),
        ('red', 'Red'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('beige', 'Beige'),
        ('grey', 'Grey'),
        ('brown', 'Brown'),
        ('pink', 'Pink'),
    ]

    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    image1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)

    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=True, null=True)
    material = models.CharField(max_length=30, choices=MATERIAL_CHOICES, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
        help_text="Category of the shirt (Casual, Denim, Formal, Printed, etc.)"
    )

    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ✅ Added/Adjusted for Carousel Image Setup
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='products/slides/')
    alt_text = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class UserPincode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.pincode} ({self.address})"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.name}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity}) - Size: {self.size or 'N/A'}"

    class Meta:
        ordering = ['product__name']
        verbose_name_plural = 'Cart Items'


# ✨ Review model
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.comment[:20]}"
