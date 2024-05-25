from django.shortcuts import render
from .models import Image
from django.db.models import Q
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
    paginate_by = 16

    def get(self, request, *args, **kwargs):
        print(request.GET.get('query'))
        print(request.GET)
        query = request.GET.get('query', '')
        self.object_list = self.get_queryset()
        if query:
            self.object_list = self.object_list.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        context = self.get_context_data()
        context['query'] = query

        return self.render_to_response(context)


class ImageDetailView(DetailView):
    model = Image
    template_name = 'image.html'
