from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string

class Home(LoginRequiredMixin, TemplateView):
    template_name = "home.html"