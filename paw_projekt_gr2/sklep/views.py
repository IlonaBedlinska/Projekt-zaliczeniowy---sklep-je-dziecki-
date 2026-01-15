from rest_framework import generics
from .models import Produkt, Kategoria
from .serializers import ProduktSerializer, KategoriaSerializer
from django.shortcuts import render, redirect, get_object_or_404

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




def produkt_create_html(request):
    kategorie = Kategoria.objects.all() 

    if request.method == "POST":
        nazwa = request.POST.get('nazwa')
        opis = request.POST.get('opis')
        cena = int(request.POST.get('cena'))
        ilosc_z_formularza = request.POST.get('ilosc')
        kategoria_id = request.POST.get('kategoria')
        

        if nazwa and cena and kategoria_id:
            kat = Kategoria.objects.get(id=kategoria_id)
            Produkt.objects.create(
                nazwa=nazwa,
                opis=opis,
                cena=cena,
                stan_magazynowy=ilosc_z_formularza,
                kategoria=kat
            )
            return redirect('produkt-list-html')
    
    return render(request, "sklep/produkt/create.html", {'kategorie': kategorie})