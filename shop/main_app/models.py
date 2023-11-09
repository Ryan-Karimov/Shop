from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return super().__str__()
    

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Kategoriya", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Rasmi")
    description = models.TextField(verbose_name="Tavsifi", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Narxi")

    def __str__(self) -> str:
        return super().__str__()
    

class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Xaridor', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Savat', on_delete=models.CASCADE, related_name='related_products')  # Изменен related_name
    product = models.ForeignKey(Product, verbose_name='Mahsulot', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Narxi")

    def __str__(self) -> str:
        return "Mahsulot: {} (savat uchun)".format(self.product.title)

    
class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Egasi', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Narxi")

    def __str__(self) -> str:
        return str(self.id)
    

class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Foydalanuvchi', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Telefon raqami')
    address = models.CharField(max_length=255, verbose_name='Adres')

    def __str__(self) -> str:
        return "Xaridor: {} {}".format(self.user.first_name, self.user.last_name)


class Specification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, verbose_name='Xarakteristika uchun mahsulot nomi')

    def __str__(self) -> str:
        return "Mahsulot uchun xarakteristikalar: {} ".format(self.name)