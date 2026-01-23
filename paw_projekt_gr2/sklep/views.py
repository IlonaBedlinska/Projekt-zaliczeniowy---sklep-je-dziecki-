from rest_framework import generics, permissions
from .models import Produkt, Kategoria, Zamowienie, PozycjaZamowienia
from .serializers import ProduktSerializer, KategoriaSerializer
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


class ProduktListCreateView(generics.ListCreateAPIView):
    queryset = Produkt.objects.all()
    serializer_class = ProduktSerializer


class ProduktDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produkt.objects.all()
    serializer_class = ProduktSerializer


class KategoriaListView(generics.ListCreateAPIView):
    queryset = Kategoria.objects.all()
    serializer_class = KategoriaSerializer

class KategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kategoria.objects.all()
    serializer_class = KategoriaSerializer

def produkt_list_html(request):
    produkty = Produkt.objects.all()
    return render(request, 
                  "sklep/produkt/list.html", 
                  {'produkty': produkty})

def produkt_detail_html(request, id):
    produkt = get_object_or_404(Produkt, id=id)
    if request.method == "POST":
        produkt.delete()
        return redirect('produkt-list-html')

    return render(request, 
                  "sklep/produkt/detail.html", 
                  {'produkt': produkt})

@staff_member_required
def produkt_create_html(request):
    kategorie = Kategoria.objects.all() 

    if request.method == "POST":
        serializer = ProduktSerializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()
            return redirect('produkt-list-html')
        else:
            return render(request, "sklep/produkt/create.html", {
                'kategorie': kategorie,
                'errors': serializer.errors,  
                'old_data': request.POST      
            })
    
    return render(request, "sklep/produkt/create.html", {'kategorie': kategorie})

class ProduktListCreateView(generics.ListCreateAPIView):
    queryset = Produkt.objects.all()
    serializer_class = ProduktSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProduktDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produkt.objects.all()
    serializer_class = ProduktSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class KategoriaListView(generics.ListCreateAPIView):
    queryset = Kategoria.objects.all()
    serializer_class = KategoriaSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class KategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kategoria.objects.all()
    serializer_class = KategoriaSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('produkt-list-html') 
        else:
            return render(request, 'sklep/login.html', {'error': 'Nieprawidłowe dane'})
    return render(request, 'sklep/login.html')

def user_logout(request):
    logout(request)
    return redirect('user-login')

def produkt_list_html(request):
    produkty = Produkt.objects.all()
    return render(request, "sklep/produkt/list.html", {'produkty': produkty})

def produkt_detail_html(request, id):
    produkt = get_object_or_404(Produkt, id=id)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('user-login') 
            
        produkt.delete()
        return redirect('produkt-list-html')

    return render(request, "sklep/produkt/detail.html", {'produkt': produkt})


@login_required(login_url='user-login') 
def produkt_create_html(request):
    kategorie = Kategoria.objects.all() 

    if request.method == "POST":
        serializer = ProduktSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('produkt-list-html')
        else:
            return render(request, "sklep/produkt/create.html", {
                'kategorie': kategorie,
                'errors': serializer.errors,
                'old_data': request.POST
            })
    
    return render(request, "sklep/produkt/create.html", {'kategorie': kategorie})



@login_required 
def dodaj_do_koszyka(request, id_produktu):
    produkt = get_object_or_404(Produkt, id=id_produktu)
    
    zamowienie, created = Zamowienie.objects.get_or_create(
        user=request.user, 
        status='nowe'
    )
    
    pozycja, created = PozycjaZamowienia.objects.get_or_create(
        zamowienie=zamowienie, 
        produkt=produkt
    )
    
    if not created:
        pozycja.ilosc += 1
        pozycja.save()
    
    return redirect('produkt-list-html')

@login_required
def pokaz_koszyk(request):
    try:
        zamowienie = Zamowienie.objects.get(user=request.user, status='nowe')
        pozycje = zamowienie.pozycje.all()
        
        suma_calkowita = sum(p.ilosc * p.cena_przy_zakupie for p in pozycje)
    except Zamowienie.DoesNotExist:
        zamowienie = None
        pozycje = []
        suma_calkowita = 0

    return render(request, 'sklep/koszyk.html', {
        'zamowienie': zamowienie,
        'pozycje': pozycje,
        'suma': suma_calkowita
    })