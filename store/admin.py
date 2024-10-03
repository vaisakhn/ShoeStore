from django.contrib import admin

# Register your models here.

from store.models import Brand,Size,Category,Product,ProductVariant,ShippingAddress

admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ShippingAddress)