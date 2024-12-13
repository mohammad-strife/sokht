from django.urls import path

from product.order import views


urlpatterns = [
    path('time/', views.time, name='time'),
    path('order/', views.order, name='order'),
    path('update/', views.update, name='update'),
    path('moj/', views.moj, name='moj'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),

    path('emergency/', views.emergency, name='emergency'),

]
