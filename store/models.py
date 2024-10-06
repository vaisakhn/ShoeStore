from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.db.models.signals import pre_save



# request.user
# UserProfile.objects.get(user_object=request.user)
# USer=>userProfile
# request.user.profile

class UserProfile(models.Model):

    profile_pic=models.ImageField(upload_to="profile_pictures",default="/profile_pictures/default.png")

    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


    def __str__(self) -> str:

        return self.user_object.username
    


class Brand(models.Model):

    title=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    



class Size(models.Model):

    number=models.PositiveIntegerField(unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    

    


class Category(models.Model):

    title=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title



class Product(models.Model):

    title=models.CharField(max_length=200)

    description=models.TextField()

    brand_object=models.ForeignKey(Brand,on_delete=models.CASCADE)

    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="projects")

    thumbnail=models.ImageField(upload_to="product_pictures",default="/product_pictures/default.png")

    size_objects=models.ManyToManyField(Size)

    price=models.PositiveIntegerField()
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.title
    



class ProductVariant(models.Model):

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_variant')
    
    color_variant=models.CharField(max_length=100,null=True)

    variant_img=models.ImageField(upload_to="variant_pictures",default="/product_pictures/default.png")

    price_variant=models.PositiveIntegerField()

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    


class Cart(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


# request.user.cart.cart_items.all()
class CartItems(models.Model):

    wishlist_object=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")

    product_variant_object=models.ForeignKey(ProductVariant,on_delete=models.CASCADE)

    size_variant=models.PositiveIntegerField(null=True)

    quantity=models.PositiveIntegerField(null=True)

    total=models.PositiveIntegerField(null=True)

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class ShippingAddress(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)

    street_address = models.CharField(max_length=1000)

    address_line_2 = models.CharField(max_length=255, blank=True, null=True)

    city = models.CharField(max_length=200)

    state = models.CharField(max_length=200)

    postal_code = models.CharField(max_length=20)

    country =models.CharField(max_length=200)

    phone_number = models.CharField(max_length=20)

    email = models.EmailField()

    created_date=models.DateTimeField(auto_now_add=True,null=True)

    updated_date=models.DateTimeField(auto_now=True,null=True)

    is_active=models.BooleanField(default=True)



class OrderSummary(models.Model):

    STATUS_PENDING = 'Pending'
    STATUS_SHIPPED = 'Shipped'
    STATUS_DELIVERED = 'Delivered'
    STATUS_CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]




    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    cart_items_object=models.ManyToManyField(CartItems)

    shipping_address=models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)

    order_id=models.CharField(max_length=200,null=True,unique=True)

    payment_method=models.CharField(max_length=200,null=True)

    delivery_status=models.CharField(
        max_length=200,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    is_paid=models.BooleanField(default=False)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    total=models.FloatField(null=True)




def create_profile(sender,instance,created,*args,**kwargs):
    if created:
        UserProfile.objects.create(user_object=instance)

post_save.connect(sender=User,receiver=create_profile)


def create_cart(sender,instance,created,*args,**kwargs):
    if created:
        Cart.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_cart)


from django.core.validators import MaxValueValidator,MinValueValidator

class Reviews(models.Model):

    product_variant_object=models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name='product_reviews')

    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    comment=models.TextField()

    rating=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


