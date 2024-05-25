from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImageListView.as_view(), name='index'),
    path('image/<int:pk>/', views.ImageDetailView.as_view(), name='image-detail'),
    path('about/', views.about, name='about'),
]
