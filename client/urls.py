from django.urls import path
from client import views,carwash


app_name = 'client'  # Replace with your app's actual name

urlpatterns = [
    path("auth/", views.auth, name="auth"),
    path("", views.home, name="home"),
    path('logout/', views.logout_view, name='logout'),  # URL خروج
    path('site-guide/', views.site_guide_view, name='site_guide'),  # ویوی راهنما
    path('carwash/', carwash.carwash, name='carwash'),  # ویوی راهنما
]
