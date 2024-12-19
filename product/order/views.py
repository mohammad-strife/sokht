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
def time(request, pk=None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if Order.objects.filter(user=request.user).exists():
                msg = "شما یک سفارش فعال دارید در صورت لغو ویا سفارش مجدد باید ابتدا از صفحه سفارشات , درخواست فعلی رو لغو کنید"
                button_text = "متوجه شدم"
                icon_type = "warning"
                return redirect(f"{reverse('moj')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")

            lat = request.POST.get('lat')
            lon = request.POST.get('lon')
            print(lat, lon)
            if not lat or not lon:
                msg = "لطفا لوکیشن را مجددا ثبت کنید"
                button_text = "باشه"
                icon_type = "warning"
                return redirect(f"{reverse('client:home')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")

            # current_time = datetime.now()
            #
            # # تنظیم منطقه زمانی به تهران
            # tehran_timezone = pytz.timezone('Asia/Tehran')
            # tehran_time = current_time.astimezone(tehran_timezone)
            #
            # # گرفتن ساعت محلی تهران
            # hour = tehran_time.hour
            #
            # selected_time = int(request.POST.get('time'))
            #
            # if selected_time <= hour:
            #     msg = "زمانیکه در نظر گرفتید برای دریافت سوخت از تایم های گذشته است لطفا تایم های پیش رو را انتخاب کنید\n سفارش های هرروز از ساعت ۰۰:۰۰ بازمیشوند  "
            #     return render(request, 'pay.html', {'msg': msg})
            # fullname = request.POST.get('fullname')

            product_id = request.POST.get('product_id')
            # quantity = request.POST.get('quantity')
            print(product_id)
            # product_price = Product.objects.get(product_id=product_id)

            # Ensure price and quantity are numeric
            # price = float(product_price.price)
            # quantity = int(quantity)

            # Calculate the amount
            # amount = price * quantity

            # Print the calculated amount

            # description = request.POST.get('description')

            api_url = f"https://api.neshan.org/v5/reverse?lat={lat}&lng={lon}"
            headers = {
                'Api-Key': settings.NESHAN_API_KEY
            }

            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                location_data = response.json()
                formatted_address = location_data.get('formatted_address', 'آدرسی یافت نشد')
            else:
                msg = 'خطای سمت سرور لطفا فیلتر شکن خود را خاموش کنید'
                button_text = "باشه"
                icon_type = "warning"
                return render(request, 'homepage.html',
                              {'msg': msg, 'button_text': button_text, 'icon_type': icon_type})

            # if Order.objects.filter(user_id=request.user).exists():
            #     return redirect('order')
            if product_id and lat and lon:
                product = Product.objects.get(product_id=product_id)
                order = Order.objects.create(
                    user=request.user,
                    product=product,
                    fullname='aaaa',

                    location=formatted_address,

                    status='uncompleted',
                    cart=False,

                    lat=lat,
                    lon=lon,
                )
                return redirect('update')
            msg = "لطفا مقادیر را با دقت پر کنید "
            return render(request, 'homepage.html', {'msg': msg})
    else:
        return redirect('client:auth')


def order(request):
    try:
        orders = Order.objects.get(user=request.user)
        return render(request, 'order1.html', {'orders': orders})
    except CustomUser.DoesNotExist:
        return redirect('client:auth')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def update(request):
    if request.method == 'POST':

        user = request.user
        try:
            order = Order.objects.get(user_id=user.id)
        except Order.DoesNotExist:
            return redirect('client:home')

        # گرفتن داده‌های ارسال شده از کاربر
        litre = request.POST.get('litre')
        saat = request.POST.get('saat')
        description = request.POST.get('description')
        print(litre, saat)

        # اعتبارسنجی داده‌ها
        if not litre or not litre.isdigit():
            msg = "لیتر باید عددی بین 10 الی 60 باشد"
            button_text = "باشه"
            icon_type = "warning"
            return redirect(f"{reverse('time')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")
        litre = int(litre)

        if not saat:
            msg = "شما باید یکی از ساعت هارو انتخاب کنید"
            button_text = "باشه"
            icon_type = "warning"
            return redirect(f"{reverse('time')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")
        if order.product_id == 1 or order.product_id == 2:
            if litre < 10:
                msg = "بنزین معمولی و سوپر حداقل سفارش 10 و حداکثر 60 لیتر میباشد"
                button_text = "متوجه شدم"
                icon_type = "warning"
                return redirect(f"{reverse('time')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")

        current_time = datetime.now()

        # تنظیم منطقه زمانی به تهران
        tehran_timezone = pytz.timezone('Asia/Tehran')
        tehran_time = current_time.astimezone(tehran_timezone)

        # گرفتن ساعت محلی تهران
        hour = tehran_time.hour
        saat = int(saat)
        selected_time = saat

        if selected_time <= hour:
            msg = "زمانیکه در نظر گرفتید برای دریافت سوخت از تایم های گذشته است لطفا تایم های پیش رو را انتخاب کنید\n سفارش های هرروز از ساعت ۰۰:۰۰ بازمیشوند  "
            button_text = "متوجه شدم"
            icon_type = "warning"
            return render(request, 'time.html', {'msg': msg, 'button_text': button_text, 'icon_type': icon_type})

        mahsol = order.product_id
        ords = Product.objects.get(product_id=mahsol)
        mm = ords.price
        mm = int(mm)
        ss = mm * litre
        # به‌روزرسانی اطلاعات سفارش
        order.amount = ss
        order.farsi = f"{ss:,}"  # ss عددی است که می‌خواهید فرمت کنید
        order.quantity = litre
        order.date = saat  # بهتر است فرمت تاریخ را بررسی کنید
        order.description = description
        order.status = "completed"
        order.save()
        msg = "تکمیل سفارش با موفقیت انجام شد"
        button_text = "بسیار عالی"
        icon_type = "success"
        return render(request, 'moj.html',
                      {'order': order, 'msg': msg, 'button_text': button_text, 'icon_type': icon_type})
    else:

        user = request.user
        try:
            order = Order.objects.get(user_id=user.id)
        except Order.DoesNotExist:
            return redirect('client:home')
        if order.status == "completed":
            msg = "شما یک سفارش فعال و تکمیل شده از پیش دارید برای لغو به سفارشات بروید"
            button_text = "متوجه شدم"
            icon_type = "warning"
            return redirect(f"{reverse('moj')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")
        return render(request, 'time.html')


def moj(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.get(user_id=user.id)

        # ابتدا بررسی می‌کنیم که پیام قبلاً در سشن ذخیره شده یا نه
        if 'msg' in request.session:
            session_msg = request.session.pop('msg')  # حذف پس از خواندن
            session_button_text = request.session.pop('button_text', None)
            session_icon_type = request.session.pop('icon_type', None)
        else:
            # در صورتی که پیام قبلاً ذخیره نشده باشد
            msg = request.GET.get('msg')
            button_text = request.GET.get('button_text')
            icon_type = request.GET.get('icon_type')

            # اگر پیام وجود داشت، آن را در سشن ذخیره کنید
            if msg and button_text and icon_type:
                request.session['msg'] = msg
                request.session['button_text'] = button_text
                request.session['icon_type'] = icon_type
                session_msg = msg
                session_button_text = button_text
                session_icon_type = icon_type
            else:
                session_msg = None
                session_button_text = None
                session_icon_type = None

        return render(request, 'moj.html', {
            'order': order,
            'msg': session_msg,
            'button_text': session_button_text,
            'icon_type': session_icon_type
        })

    else:
        msg = "ابتدا باید ثبت نام کنید و سپس یک سفارش ثبت کنید"
        button_text = "متوجه شدم"
        icon_type = "warning"
        return redirect(f"{reverse('client:auth')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")


def delete_order(request, order_id):
    # بررسی اینکه کاربر وارد شده باشد
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'لطفاً وارد شوید.'}, status=403)

    try:
        # دریافت سفارش
        order = get_object_or_404(Order, id=order_id, user=request.user)

        # حذف سفارش
        order.delete()

        msg = "سفارش شما با موفقیت لغو شد"
        button_text = "متوجه شدم"
        icon_type = "success"
        return redirect(f"{reverse('client:home')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")
    except:
        msg = "سفارش شما یافت نشد"
        button_text = "متوجه شدم"
        icon_type = "error"
        return redirect(f"{reverse('client:home')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")


def emergency(request):
    return render(request, "emergency.html")
