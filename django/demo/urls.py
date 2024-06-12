from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('demo/input', views.input_data, name='input_data'),
    path('demo/result', views.show_result, name='show_result'),
]