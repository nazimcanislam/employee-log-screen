from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('add/<str:model_name>/', views.add_data_to_table, name='add'),
    path('edit/<str:model_name>/<int:_id>/', views.edit_data, name='edit'),
    path('delete/<str:model_name>/<int:_id>/', views.delete_data, name='delete'),
]
