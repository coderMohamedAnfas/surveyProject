from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_input/', views.add_input, name='add_input'),
    path('edit_input/<int:input_id>/', views.edit_input, name='edit_input'),
    path('delete_input/<int:input_id>/', views.delete_input, name='delete_input'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('edit_input/<int:input_id>/', views.edit_input, name='edit_input'),
    path('edit_productive/<int:productive_id>/', views.edit_productive, name='edit_productive'),
    path('edit_employ_welfare/<int:employ_welfare_id>/', views.edit_employ_welfare, name='edit_employ_welfare'),
]
