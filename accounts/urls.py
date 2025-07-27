from django.urls import include, path
from django.contrib import admin  
from .import views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
     path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
]   