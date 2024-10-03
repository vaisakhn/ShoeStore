from django.contrib import admin

# Register your models here.

from store.models import Brand,Size,Category,Color,Product,ProductVariant

admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductVariant)
