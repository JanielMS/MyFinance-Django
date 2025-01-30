from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

class RegistrarView(CreateView):
    model = get_user_model()
    template_name = "registration/registrar.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

class LogoutView(LogoutView):
    next_page = '/'