from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.shortcuts import  redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .forms import PerfilUsuarioForm, User


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


class PerfilUsuarioDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "usuarios/perfil_detail.html"

    def get_object(self):
        return self.request.user

class PerfilUsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = PerfilUsuarioForm
    template_name = "usuarios/perfil_form.html"
    success_url = reverse_lazy("perfil-usuario")

    def get_object(self):
        return self.request.user  # Permite apenas editar o próprio perfil

    def form_invalid(self, form):
        messages.success(self.request, "Perfil atualizado com sucesso!")
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest': 
            html = render_to_string(self.template_name, {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user 
        self.object = form.save()
        
       
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = form.save()
            return JsonResponse({'success': True, 'redirect_url': self.success_url})
        
        return redirect(self.success_url)

class PerfilUsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "usuarios/perfil_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user  # Permite excluir apenas o próprio perfil

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Perfil excluído com sucesso!")

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({'success': True, 'redirect_url': self.success_url})
        
        return redirect(self.success_url)
        