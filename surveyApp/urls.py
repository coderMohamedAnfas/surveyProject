from django.urls import path
from .views import index, data_management_view, add_input_category, add_input

urlpatterns = [
    path('', index, name='index'),
    path('manage/', data_management_view, name='data_management_view'),
    path('add-category/', add_input_category, name='add_input_category'),
    path('add-input/', add_input, name='add_input'),
]
