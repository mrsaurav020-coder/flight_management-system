from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:id>/', views.book_flight, name='book_flight'),
    path('login/', views.user_login, name='login'),
    path('history/', views.history, name='history'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('success/<int:id>/', views.success, name='success'),
    path('download-ticket/<int:id>/', views.download_ticket, name='download_ticket'),
]