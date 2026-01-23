from rest_framework import serializers
from .models import Kategoria, Produkt
from django.contrib.auth.models import User

def sprawdz_opis(value):
    if len(value) < 10:
        raise serializers.ValidationError("Opis jest za krótki! Musi mieć min. 10 znaków.")

class KategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategoria
        fields = ['id', 'nazwa', 'slug']

class ProduktSerializer(serializers.ModelSerializer):
    opis = serializers.CharField(validators=[sprawdz_opis], required=False)
    

    class Meta:
        model = Produkt
        fields = '__all__' 
        read_only_fields = ['id', 'slug', 'utworzono'] 

    def validate_nazwa(self, value):
        if not value[0].isupper():
            raise serializers.ValidationError("Nazwa produktu musi zaczynać się z wielkiej litery!")
        return value

    def validate(self, data):
        cena = data.get('cena')
        stan = data.get('stan_magazynowy')
        dostepny = data.get('dostepny')

        if dostepny and stan == 0:
            raise serializers.ValidationError({
                "stan_magazynowy": "Produkt oznaczony jako dostępny nie może mieć zerowego stanu magazynowego."
            })
            

        if cena and cena > 5000 and not data.get('opis'):
             raise serializers.ValidationError({
                "opis": "Dla produktów luksusowych (powyżej 5000 PLN) opis jest wymagany."
            })

        return data
    
