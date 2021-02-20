from django.shortcuts import render

# Create your views here.


def index(req, *args, **kwargs):
    """Render our index template"""
    return render(req, 'frontend/index.html')
