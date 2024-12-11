from django.urls import path

from blog.views import contact

urlpatterns = [
    path ('contact/', contact, name='contact')
]