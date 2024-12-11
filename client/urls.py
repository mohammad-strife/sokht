from django.urls import path

from client import views

app_name = 'client'  # Replace with your app's actual name

urlpatterns = [
    path("auth/", views.auth, name="auth"),
    path("", views.home, name="home"),
    path('logout/', views.logout_view, name='logout'),  # URL خروج

]
