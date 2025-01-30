from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('registrar', RegistrarView.as_view(), name='registrar'),
    path('logout', LogoutView.as_view(), name='logout'),
]