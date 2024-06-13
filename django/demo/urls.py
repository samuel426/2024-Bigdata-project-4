from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_data, name='input_data'),
#    path('demo/input', views.input_data, name='input_data'),
    path('demo/result', views.show_result, name='show_result'),
]
