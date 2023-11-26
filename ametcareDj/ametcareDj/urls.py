from django.contrib import admin
from django.urls import path
from firstapp import views


urlpatterns = [
    path('', views.start1),
    path('start2', views.start2),
    path('login', views.login),
    path('register', views.register),
    path('userinfo', views.userinfo),
    path('choose', views.choose),
    path('allergy', views.allergy),
    path('indpref', views.indpref),
    path('admin/', admin.site.urls),
]
