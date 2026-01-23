from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('api/produkty/', views.ProduktListCreateView.as_view(), name='produkt-list'),
    path('api/produkty/<int:pk>/', views.ProduktDetailView.as_view(), name='produkt-detail'),
    path('api/kategorie/', views.KategoriaListView.as_view(), name='kategoria-list'),
    path('api/kategorie/<int:pk>/', views.KategoriaDetailView.as_view(), name='kategoria-detail'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('html/produkty/', views.produkt_list_html, name='produkt-list-html'),
    path('html/produkty/<int:id>/', views.produkt_detail_html, name='produkt-detail-html'),
    path('html/produkty/dodaj/', views.produkt_create_html, name='produkt-create-html'),
    path('html/login/', views.user_login, name='user-login'),
    path('html/logout/', views.user_logout, name='user-logout'),
    path('html/koszyk/dodaj/<int:id_produktu>/', views.dodaj_do_koszyka, name='dodaj-do-koszyka'),
    path('html/koszyk/', views.pokaz_koszyk, name='pokaz-koszyk'),
]