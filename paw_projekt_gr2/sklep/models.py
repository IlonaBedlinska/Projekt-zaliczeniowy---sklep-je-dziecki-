from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q, CheckConstraint

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