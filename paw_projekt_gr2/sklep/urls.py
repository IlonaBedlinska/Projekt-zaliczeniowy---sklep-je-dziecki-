from django.urls import path
from . import views

urlpatterns = [
    path('produkty/', views.ProduktListCreateView.as_view(), name='produkt-list'),
    path('produkty/<int:pk>/', views.ProduktDetailView.as_view(), name='produkt-detail'),

    path('kategorie/', views.KategoriaListView.as_view(), name='kategoria-list'),
    path('kategorie/<int:pk>/', views.KategoriaDetailView.as_view(), name='kategoria-detail'),
]