from django.contrib import admin
from .models import Kategoria, Produkt

class KategoriaAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'slug']
    prepopulated_fields = {'slug': ('nazwa',)} 

admin.site.register(Kategoria, KategoriaAdmin)

class ProduktAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'cena', 'stan_magazynowy', 'dostepny', 'kategoria', 'utworzono']

    list_filter = ['dostepny', 'kategoria', 'utworzono']

    list_editable = ['cena', 'stan_magazynowy', 'dostepny']

    search_fields = ['nazwa', 'opis']

    prepopulated_fields = {'slug': ('nazwa',)}

admin.site.register(Produkt, ProduktAdmin)