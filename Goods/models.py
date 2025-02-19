from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class Banner(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    title = models.TextField()
    img = models.ImageField(upload_to='category_img')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def is_like(self, user):
        object = WishList.objects.filter(product = self, user = user)
        return object
        

class ProductImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to='product-img')

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='carts')
    is_active = models.BooleanField(default=True)
    shopping_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.author.username if self.author else "Anonymous"


class CartProduct(models.Model):
    productImg = models.ForeignKey(ProductImg, on_delete=models.SET_NULL, null=True, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.product.product.name


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, related_name='orders')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    status = models.SmallIntegerField(
        choices=(
            (1, 'Tayyorlanmoqda'),
            (2, 'Yo`lda'),
            (3, 'Yetib borgan'),
            (4, 'Qabul qilingan'),
            (5, 'Qaytarilgan'),
        )
    )

    def __str__(self):
        return self.full_name


class ProductEnter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='entries')
    quantity = models.IntegerField()
    old_quantity = models.IntegerField(blank=True, null=True)  # Allow null for new instances
    date = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.id:
                self.old_quantity = self.product.quantity
                self.product.quantity += int(self.quantity)
            else:
                try:
                    previous_entry = ProductEnter.objects.get(id=self.id)
                    quantity_diff = int(self.quantity) - previous_entry.quantity
                    self.product.quantity += quantity_diff
                    self.old_quantity = previous_entry.quantity
                except ObjectDoesNotExist:
                    # Handle case where the entry doesn't exist
                    pass
            self.product.save()
            super().save(*args, **kwargs)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}, {self.product.name}"
     
    
class Info(models.Model):
    email = models.EmailField()
    number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)


class Contact (models.Model):
    whatsapp = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    telegram = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)