from django.urls import path

from product.order import views


urlpatterns = [
    path('time/', views.time, name='time'),
    path('order/', views.order, name='order'),
    path('update/', views.update, name='update'),
    path('moj/', views.moj, name='moj'),
]
