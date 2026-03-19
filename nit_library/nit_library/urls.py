from django.contrib import admin
from django.urls import path
from portal import views

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Home Page - Iska name 'index' rakha hai kyunki login.html mein yahi use ho raha hai
    path('', views.index, name='index'), 
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login_url'),
    path('logout/', views.logout_view, name='logout'),
    
    # Portal Features
    path('dashboard/', views.dashboard, name='dashboard'),
 #   path('book-vault/', views.book_vault, name='book_vault'),
    path('rules/', views.rules_view, name='rules'),

    path('', views.index, name='index'),
    path('notices/', views.notice_view, name='notice_page'),
    path('download/', views.download_view, name='download_page'),
    # Isse urlpatterns list ke andar daal do
    path('contact/', views.contact_view, name='contact_page'),
]