from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse

from client.models import CustomUser
from product.models import Product


def auth(request):
    if request.method == 'POST':

        username = request.POST.get('n_code')
        password = request.POST.get('phone')

        # بررسی طول کد ملی
        if not len(username) == 10:
            msg = "طول کد ملی باید 10 رقم باشد"
            button_text = "باشد"
            icon_type = "error"
            return render(request, 'login.html', {'msg': msg, 'button_text': button_text, 'icon_type': icon_type})

        # بررسی فرمت شماره همراه
        if not password.startswith('09') or not len(password) == 11:
            msg = "شماره همراه باید با 09 شروع شده و 11 رقم باشد"
            button_text = "باشد"
            icon_type = "error"
            return render(request, 'login.html', {'msg': msg, 'button_text': button_text, 'icon_type': icon_type})

        if CustomUser.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                # next_url = request.GET.get('next')
                # if next_url:
                #     return redirect(next_url)
                msg = "شما از قبل حساب داشتید و با موفقیت لاگین شدید"
                button_text = "بسیار عالی"
                icon_type = "success"
                return redirect(f"{reverse('client:home')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")
            else:
                msg = "شماره همراه  یا کدملی اشتباه است"
                button_text = "درستش میکنم"
                icon_type = "error"
                return render(request, 'login.html', {'msg': msg, 'button_text': button_text, 'icon_type': icon_type})
        else:
            user = CustomUser(username=username, n_code=username, phone=password)
            user.set_password(password)
            user.save()
            login(request, user)
            msg = "ثبت نام شما با موفقیت انجام شد"
            button_text = "بسیار عالی"
            icon_type = "success"
            return redirect(f"{reverse('client:home')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")
    return render(request, 'login.html', {'user': request.user})


def home(request):
    if not request.session.get('seen_guide', False):
        return redirect('client:site_guide')
    products = Product.objects.all()
    msg = request.GET.get('msg')
    button_text = request.GET.get('button_text')
    icon_type = request.GET.get('icon_type')
    return render(request, 'homepage.html', {
        'products': products,
        'user': request.user,
        'msg': msg,
        'button_text': button_text,
        'icon_type': icon_type
    })


def logout_view(request):
    logout(request)
    msg = "شما از حساب کاربری خارج شدید"
    button_text = "فهمیدم"
    icon_type = "info"
    return redirect(f"{reverse('client:home')}?msg={msg}&button_text={button_text}&icon_type={icon_type}")


def site_guide_view(request):
    # تنظیم مقدار 'seen_guide' به True برای علامت زدن نمایش صفحه راهنما
    request.session['seen_guide'] = True
    return render(request, 'site_guide.html')  # نمایش صفحه راهنما
