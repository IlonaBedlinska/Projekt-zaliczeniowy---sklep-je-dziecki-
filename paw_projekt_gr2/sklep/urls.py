from django.urls import path
from . import views

urlpatterns = [
    path('produkty/', views.ProduktListCreateView.as_view(), name='produkt-list'),
    path('produkty/<int:pk>/', views.ProduktDetailView.as_view(), name='produkt-detail'),

    path('kategorie/', views.KategoriaListView.as_view(), name='kategoria-list'),
    path('kategorie/<int:pk>/', views.KategoriaDetailView.as_view(), name='kategoria-detail'),
    path('html/produkty/', views.produkt_list_html, name='produkt-list-html'),
    path('html/produkty/<int:id>/', views.produkt_detail_html, name='produkt-detail-html'),
    path('html/produkty/dodaj/', views.produkt_create_html, name='produkt-create-html'),
]