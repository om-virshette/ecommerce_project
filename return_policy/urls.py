from django.urls import path
from . import views  # Import from your existing app

urlpatterns = [
    path('return-policy/', views.return_policy, name='return_policy'),
]