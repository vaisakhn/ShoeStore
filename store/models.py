from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save



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

    

    
    


class Color(models.Model):

    title=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    


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





class OrderSummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    product_object=models.ManyToManyField(Product)

    order_id=models.CharField(max_length=200,null=True)

    is_paid=models.BooleanField(default=False)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)



def create_profile(sender,instance,created,*args,**kwargs):
    if created:
        UserProfile.objects.create(user_object=instance)

post_save.connect(sender=User,receiver=create_profile)


def create_cart(sender,instance,created,*args,**kwargs):
    if created:
        Cart.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_cart)



class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=1000)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    country =models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    