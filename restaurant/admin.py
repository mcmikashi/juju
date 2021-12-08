from django.contrib import admin
from .models import Categorie,Nouriture,Commande,Pannier
admin.site.register(Nouriture)
admin.site.register(Categorie)
admin.site.register(Pannier)
admin.site.register(Commande)