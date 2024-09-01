from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_input/', views.add_input, name='add_input'),
    path('delete_input/<int:input_id>/', views.delete_input, name='delete_input'),
    path('edit_input/<int:input_id>/', views.edit_input, name='edit_input'),
    path('edit_productive/', views.edit_productive, name='edit_productive'),
    path('edit_welfare/', views.edit_welfare, name='edit_welfare'),
    # path('apply_changes/', views.update_selection, name='apply_changes'),
]
