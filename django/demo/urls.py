from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('demo/result', views.show_result, name='show_result'),
]