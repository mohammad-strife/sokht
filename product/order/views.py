from django.shortcuts import redirect, render
from urllib.parse import urlencode
from django.urls import reverse
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from client.models import CustomUser
from product.models import Product
from product.models import Order
import pytz
from datetime import datetime
from sokht import settings


@csrf_exempt
def pay(request, pk=None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if Order.objects.filter(user=request.user).exists():
                msg = "شما یک سفارش فعال دارید!!!"
                query_string = urlencode({'msg': msg})
                url = f"{reverse('pay')}?{query_string}"
                return redirect(url)

            lat = request.POST.get('lat')
            lon = request.POST.get('lon')

            if not lat or not lon:
                msg = 'لطفا لوکیشن را با دابل کلیک مشخص کنید'
                query_string = urlencode({'msg': msg})
                url = f"{reverse('pay')}?{query_string}"
                return redirect(url)

            current_time = datetime.now()

            # تنظیم منطقه زمانی به تهران
            tehran_timezone = pytz.timezone('Asia/Tehran')
            tehran_time = current_time.astimezone(tehran_timezone)

            # گرفتن ساعت محلی تهران
            hour = tehran_time.hour

            selected_time = int(request.POST.get('time'))

            if selected_time <= hour:
                msg = "زمانیکه در نظر گرفتید برای دریافت سوخت از تایم های گذشته است لطفا تایم های پیش رو را انتخاب کنید\n سفارش های هرروز از ساعت ۰۰:۰۰ بازمیشوند  "
                return render(request, 'pay.html', {'msg': msg})
            fullname = request.POST.get('fullname')

            product_id = request.POST.get('product')
            quantity = request.POST.get('quantity')

            product_price = Product.objects.get(product_id=product_id)

            # Ensure price and quantity are numeric
            price = float(product_price.price)
            quantity = int(quantity)

            # Calculate the amount
            amount = price * quantity

            # Print the calculated amount

            description = request.POST.get('description')

            api_url = f"https://api.neshan.org/v5/reverse?lat={lat}&lng={lon}"
            headers = {
                'Api-Key': settings.NESHAN_API_KEY
            }

            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                location_data = response.json()
                formatted_address = location_data.get('formatted_address', 'آدرسی یافت نشد')
            else:
                error_message = "خطا در دریافت اطلاعات از سرور "
                return render(request, 'pay.html', {'error_message': error_message})

            if Order.objects.filter(user_id=request.user).exists():
                return redirect('order')
            if product_id and quantity and lat and lon and selected_time and fullname:
                product = Product.objects.get(product_id=product_id)
                order = Order.objects.create(
                    user=request.user,
                    product=product,
                    description=description,
                    location=formatted_address,
                    date=selected_time,
                    status='pending',
                    cart=False,
                    quantity=quantity,
                    amount=amount,
                    lat=lat,
                    lon=lon,
                    fullname=fullname,
                )
                return redirect('order')
            msg = "مقادیر را با دقت پر کنید لطفا"
            return render(request, 'pay.html', {'msg': msg})

        products = Product.objects.all()
        if pk:
            if products.filter(product_id=pk).exists():
                pk = pk
            else:
                pk = 0
        else:
            pk = 0
        return render(request, 'pay.html', {'products': products, 'pk': pk})
    else:
        return redirect('client:auth')


def order(request):
    try:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'order.html', {'orders': orders})
    except CustomUser.DoesNotExist:
        return redirect('client:auth')
