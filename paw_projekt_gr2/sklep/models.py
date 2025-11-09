from django.db import models

from django.db import models

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.nazwa

class Produkt(models.Model):
    kategoria = models.ForeignKey(Kategoria, related_name='produkty', on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    opis = models.TextField(blank=True, null=True)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    
    stan_magazynowy = models.PositiveIntegerField(default=0)
    dostepny = models.BooleanField(default=True)
    
    utworzono = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

    def __str__(self):
        return self.nazwa