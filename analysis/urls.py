from django.conf.urls import  url

from django.views.generic import TemplateView
from django.urls import path
from analysis import views

urlpatterns = [
    path('search_query/',views.search, name='search'),
    path('tweets/',views.search),
    path('predict/',views.predict,name='predict'),
    path('result/',views.model, name="lr"),
        ]



   