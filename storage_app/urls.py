from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_file, name='upload'),
    path('files/', views.file_list, name='file_list'),
    path('share/<int:file_id>/', views.share_file, name='share_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('view/<int:file_id>/', views.view_file, name='view_file'),
]