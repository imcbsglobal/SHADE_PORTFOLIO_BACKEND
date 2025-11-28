from django.urls import path
from . import views

urlpatterns = [
    # Visitor Registration
    path('register/', views.register_visitor, name='register_visitor'),
    
    # Admin Login
    path('admin-login/', views.admin_login, name='admin_login'),


    path('user-login/', views.user_login, name='user_login'),
    
    # Smiles
    path('smiles/', views.smile_list, name='smile_list'),
    path('smiles/<int:pk>/', views.smile_detail, name='smile_detail'),
    
    # Our Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    
    # Ceremonial
    path('ceremonials/', views.ceremonial_list, name='ceremonial_list'),
    path('ceremonials/<int:pk>/', views.ceremonial_detail, name='ceremonial_detail'),
    
    # Demonstrations
    path('demonstrations/', views.demonstration_list, name='demonstration_list'),
    path('demonstrations/<int:pk>/', views.demonstration_detail, name='demonstration_detail'),
    
    # Dashboard
    path('dashboard/', views.dashboard_data, name='dashboard_data'),
]