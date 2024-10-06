"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name='register'),
    path('',views.SignInView.as_view(),name='signin'),
    path('index/',views.IndexView.as_view(),name='index'),
    path('product/details/<int:pk>/',views.ProductDetailView.as_view(),name='product-details'),
    path('cart/add/<int:pk>/',views.AddToCartView.as_view(),name='add-to-cart'),
    path('mycart/',views.MyCartView.as_view(),name='mycart'),
    path('mycart/remove/<int:pk>/',views.CartItemDelete.as_view(),name='cartitem-remove'),
    path('shipping/',views.ShippingAddressView.as_view(),name='shipping-address'),
    path('checkout/',views.CheckOutView.as_view(),name='checkout'),
    path('orders/',views.OrderSummaryView.as_view(),name='orders'),
    path('payment/verification/',views.PaymentVerificationView.as_view(),name='payment-verify'),
    path('signout/',views.SignOutView.as_view(),name='signout'),
    path('review/<int:pk>/',views.ReviewAddView.as_view(),name='review-add'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
