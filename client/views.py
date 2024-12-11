from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse

from client.models import CustomUser
from product.models import Product


def auth(request):
    if request.user.is_authenticated:
        return redirect('client:home')

    if request.method == 'POST':

        username = request.POST.get('n_code')
        password = request.POST.get('phone')
        print(username, password)
        # بررسی طول کد ملی
        if not len(username) == 10:
            msg = "طول کد ملی باید 10 رقم باشد"
            return render(request, 'auth.html', {'msg': msg})

        # بررسی فرمت شماره همراه
        if not password.startswith('09') or not len(password) == 11:
            msg = "شماره همراه باید با 09 شروع شده و 11 رقم باشد"
            return render(request, 'auth.html', {'msg': msg})

        if CustomUser.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # next_url = request.GET.get('next')
                # if next_url:
                #     return redirect(next_url)
                return redirect(reverse('client:home'))

            else:
                msg = "شماره همراه  یا کدملی اشتباه است"
                return render(request, 'auth.html', {'msg': msg})
        else:
            user = CustomUser(username=username, n_code=username, phone=password)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect(reverse('client:home'))

    return render(request, 'auth.html')


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products, 'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('client:home')  # به صفحه خانه برمی‌گردد
