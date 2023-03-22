from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tables/<str:table_name>/', views.index_show_table, name='index_show_table'),
    path('reports/<str:report_name>/', views.index_show_report, name='index_show_report'),
    path('reports/<str:report_name>/output/<str:output_type>/', views.reqort_output, name='reqort_output'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('add/<str:model_name>/', views.add_data_to_table, name='add'),
    path('edit/<str:model_name>/<int:_id>/', views.edit_data, name='edit'),
    path('delete/<str:model_name>/<int:_id>/', views.delete_data_view, name='delete'),
    path('profile/', views.profile, name='profile'),
    path('profile/basic/', views.profile_basic, name='profile_basic'),
    path('profile/password/', views.profile_password, name='profile_password'),
    path('profile/password/forget/', views.profile_password_forget, name='profile_password_forget'),
]
