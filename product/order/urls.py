from django.urls import path

from product.order import views


urlpatterns = [
    path('pay/<int:pk>/', views.pay, name='pay_with_pk'),
    path('pay/', views.pay, name='pay'),
    path('order/', views.order, name='order'),
]
