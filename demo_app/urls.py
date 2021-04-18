from django.conf.urls import  url

from django.views.generic import TemplateView
from django.urls import path
from demo_app import views

urlpatterns = [
    path('',views.search, name='search'),
    path('tweets/',views.search),
    path('predict/',views.predict,name='predict'),
    path('result/',views.model, name="lr"),
    path("signup/",views.user_signup,name="signup")

    ]



   