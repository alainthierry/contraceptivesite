from django.urls import re_path, path
from . import views

app_name = 'predictMethods'

urlpatterns = [
    path('', views.index, name='home'),
    path('predict_methods/result/', views.get_sent_data, name='predict'),
    path('predict_methods/login/', views.user_login, name='login'),
    path('predict_methods/about_cmc', views.about_cmc, name='about'),
]
