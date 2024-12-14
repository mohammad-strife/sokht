from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse

from client.models import CustomUser
from product.models import Product


def auth(request):
    if request.method == 'POST':

        username = request.POST.get('n_code')
        password = request.POST.get('phone')

        print(username, password)
        # بررسی طول کد ملی
        if not len(username) == 10:
            msg = "طول کد ملی باید 10 رقم باشد"
            return render(request, 'login.html', {'msg': msg})

        # بررسی فرمت شماره همراه
        if not password.startswith('09') or not len(password) == 11:
            msg = "شماره همراه باید با 09 شروع شده و 11 رقم باشد"
            return render(request, 'login.html', {'msg': msg})

        if CustomUser.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print(1111)
                # next_url = request.GET.get('next')
                # if next_url:
                #     return redirect(next_url)
                return redirect(reverse('client:home'))

            else:
                msg = "شماره همراه  یا کدملی اشتباه است"
                return render(request, 'login.html', {'msg': msg})
        else:
            user = CustomUser(username=username, n_code=username, phone=password)
            user.set_password(password)
            user.save()
            login(request, user)
            print(1111111111111111111)
            return redirect(reverse('client:home'))

    return render(request, 'login.html', {'user': request.user})


def home(request):
    if not request.session.get('seen_guide', False):
        return redirect('client:site_guide')
    products = Product.objects.all()
    return render(request, 'homepage.html', {'products': products, 'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('client:home')  # به صفحه خانه برمی‌گردد


def site_guide_view(request):
    # تنظیم مقدار 'seen_guide' به True برای علامت زدن نمایش صفحه راهنما
    request.session['seen_guide'] = True
    return render(request, 'site_guide.html')  # نمایش صفحه راهنما
