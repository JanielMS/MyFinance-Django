from django.views.generic import TemplateView, FormView
from django.http import JsonResponse
from django.template.loader import render_to_string

class Home(TemplateView):
    template_name = "home.html"