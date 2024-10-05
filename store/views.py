from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.db.models import Sum

# Create your views here.

from store.forms import SignUpForm,SignInForm,ShippingAddressForm
from store.models import Product,ProductVariant,Cart,CartItems,ShippingAddress,OrderSummary


# aliasing decouple as dc
import decouple as dc

import uuid

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

KEY_SECRET=dc.config('KEY_SECRET')
KEY_ID=dc.config('KEY_ID')




class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form_instance=SignUpForm()

        return render(request,'store/reg_form.html',{'form':form_instance})
    
    
    def post(self,request,*args,**kwargs):
        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():
            form_instance.save()

            return redirect('signin')
        
        return render(request,'store/reg_form.html',{'form':form_instance})
    



class SignInView(View):
    def get(self,request,*args,**kwargs):
        form_instance=SignInForm()

        return render(request,'store/login.html',{'form':form_instance})
    

    def post(self,request,*args,**kwargs):
        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():
            data=form_instance.cleaned_data
            user_obj=authenticate(request,**data)

            if user_obj:
                login(request,user_obj)

                return redirect('index')
            
            return render(request,'store/login.html',{'form':form_instance})
        


class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()

        return render(request,'store/index.html',{'product':qs})
    

class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Product.objects.get(id=id)
        qty=[1,2,3,4,5,6,7,8,9,10]
        
        color=ProductVariant.objects.filter(product_object=id).values("color_variant")
        if request.GET.get('color'):
            selected_color=request.GET.get('color')
            variant_obj=ProductVariant.objects.filter(color_variant=selected_color)

            return render(request,'store/product_details.html',{'product':qs,'color':color,'variant':variant_obj,'selected_color':selected_color,'quantity':qty})

        return render(request,'store/product_details.html',{'product':qs,'color':color,'quantity':qty})



class AddToCartView(View):
    def post(self,request,*args,**kwargs):
        color=request.POST.get('color')
        product_variant_obj=ProductVariant.objects.get(color_variant=color)
        size=request.POST.get('size')
        quantity=int(request.POST.get('quantity'))
        price=int(request.POST.get('price'))
        total=quantity*price
        
        CartItems.objects.create(
            wishlist_object=request.user.cart,
            product_variant_object=product_variant_obj,
            size_variant=size,
            quantity=quantity,
            total=total
        )

        return redirect("index")


class MyCartView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cart_items.filter(is_order_placed=False)
        total=0
        for p in qs:
            total+=p.total


        return render(request,'store/my_cart.html',{'products':qs,"total":total})



class CartItemDelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')

        CartItems.objects.get(id=id).delete()

        return redirect('mycart')
    

class ShippingAddressView(View):
    def get(self,request,*args,**kwargs):
        form_instance=ShippingAddressForm()

        return render(request,'store/shipping_address.html',{'form':form_instance})
    
    
    def post(self,request,*args,**kwargs):
        form_instance=ShippingAddressForm(request.POST)

        if form_instance.is_valid():
            data=form_instance.cleaned_data
            ShippingAddress.objects.create(**data,user_object=self.request.user)

            return redirect('checkout')
        
        return render(request,'store/shipping_address.html',{'form':form_instance})
    

import razorpay

class CheckOutView(View):
    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cart_items.filter(is_order_placed=False)

        shipping_address=ShippingAddress.objects.filter(user_object=request.user).order_by('created_date').first()


        return render(request,'store/checkout.html',{'products':qs,"shipping":shipping_address})
    

    def post(self,request,*args,**kwargs):

        payment_method=request.POST.get('payment-method')

        if payment_method == 'cod':
            def generate_order_id():
                
                return str(uuid.uuid4())

            order_id = generate_order_id()

            qs=request.user.cart.cart_items.filter(is_order_placed=False)
            total=0
            for p in qs:
                total+=p.total

            cart_items=qs
            order_summery_obj=OrderSummary.objects.create(
                user_object=request.user,
                order_id=order_id,
                shipping_address=ShippingAddress.objects.filter(user_object=request.user).order_by('created_date').first(),
                total=total
                )
            for ci in cart_items:
                order_summery_obj.cart_items_object.add(ci)
                order_summery_obj.payment_method='cash on delivery'
                order_summery_obj.save()
       


            for ci in cart_items:
                ci.is_order_placed=True
                ci.save()

        else:

            qs=request.user.cart.cart_items.filter(is_order_placed=False)
            total=0
            for p in qs:
                total+=p.total

            client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))
            amount=total * 100
            data={"amount":amount,"currency":"INR","receipt":"order_rcptid_11"}
            payment=client.order.create(data=data)
            

            # create order_object
            cart_items=request.user.cart.cart_items.filter(is_order_placed=False)
            order_summery_obj=OrderSummary.objects.create(
                user_object=request.user,
                order_id=payment.get('id'),
                shipping_address=ShippingAddress.objects.filter(user_object=request.user).order_by('created_date').first(),
                total=total
                )

            for ci in cart_items:
                order_summery_obj.cart_items_object.add(ci)
                order_summery_obj.payment_method='online'
                order_summery_obj.save()

            context={
                'key':KEY_ID,
                'amount':data.get('amount'),
                'currency':data.get('currency'),
                'order_id':payment.get('id')
                }
            

        return render(request,'store/payment.html',context)



@method_decorator(csrf_exempt,name='dispatch')
class PaymentVerificationView(View):
    def post(self,request,*args,**kwargs):
        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))
        ordersummery_obj=OrderSummary.objects.get(order_id=request.POST.get('razorpay_order_id'))
        login(request,ordersummery_obj.user_object)
        try:
            # doubtfull code
            client.utility.verify_payment_signature(request.POST)
            print('payment succes')
            order_id=request.POST.get('razorpay_order_id')
            OrderSummary.objects.filter(order_id=order_id).update(is_paid=True)
            cart_items=request.user.cart.cart_items.filter(is_order_placed=False)
            for ci in cart_items:
                ci.is_order_placed=True
                ci.save()
                
        except:
            # handling code
            print('payment failed ')

        return redirect('index')


class OrderSummaryView(View):
    def get(self,request,*args,**kwargs):
        orders=OrderSummary.objects.filter(user_object=request.user).order_by('-created_date')

        return render(request,'store/order_summary.html',{'orders':orders})
    
