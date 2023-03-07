from django.shortcuts import render
from .models import Image
from django.views.generic import (
    ListView, DetailView
)


def about(request):
    return render(request, 'about.html')


class ImageListView(ListView):
    model = Image
    template_name = 'index.html'
    context_object_name = 'images'
    ordering = ['-created_at']
    #paginate_by = 2


class ImageDetailView(DetailView):
    model = Image
    template_name = 'image.html'
