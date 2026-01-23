from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q, CheckConstraint
from django.contrib.auth.models import User

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ['nazwa']  

    def __str__(self):
        return self.nazwa

class Produkt(models.Model):
    kategoria = models.ForeignKey(Kategoria, related_name='produkty', on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True) 
    
    opis = models.TextField(blank=True, null=True)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    
    stan_magazynowy = models.PositiveIntegerField(default=0)
    dostepny = models.BooleanField(default=True)
    
    utworzono = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"
        ordering = ['-utworzono'] 
        constraints = [
           CheckConstraint(condition=Q(cena__gte=0), name='cena_nieujemna'),
           CheckConstraint(condition=Q(stan_magazynowy__gte=0), name='stan_nieujemny'),
        ]

    def __str__(self):
        return f"{self.nazwa} ({self.cena} PLN)"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nazwa)
        
        if self.cena < 0:
             raise ValueError("Cena nie może być ujemna!")
             
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print(f"UWAGA: Usuwam produkt {self.nazwa} z bazy!")
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('produkt_detail', args=[self.slug])
    

class Zamowienie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zamowienia')
    data_zamowienia = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('nowe', 'Nowe'), ('oplacone', 'Opłacone'), ('wyslane', 'Wysłane')],
        default='nowe'
    )

    def __str__(self):
        return f"Zamówienie {self.id} - {self.user.username}"
    
class PozycjaZamowienia(models.Model):
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.CASCADE, related_name='pozycje')
    produkt = models.ForeignKey('Produkt', on_delete=models.CASCADE)
    ilosc = models.PositiveIntegerField(default=1) 
    
    cena_przy_zakupie = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.cena_przy_zakupie:
            self.cena_przy_zakupie = self.produkt.cena
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produkt.nazwa} x {self.ilosc}"