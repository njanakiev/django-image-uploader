from django.shortcuts import render
from .models import Image

# Create your views here.
def index(request):
    images = Image.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'images': images})

def about(request):
    return render(request, 'about.html')
