from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
class Categorie(models.Model):
    nom = models.CharField(max_length=150)
    def __str__(self):
        return self.nom
    def get_absolute_url(self):
        return reverse("Categorie_detail", kwargs={"pk": self.pk})

class Nouriture(models.Model):
    categorie = models.ForeignKey("Categorie",on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    prix = models.FloatField()
    image = models.ImageField(upload_to="upload/image_nouriture/",default="pexels-maarten-van-den-heuvel-2284166.jpg")
    def __str__(self):
        return self.nom
    def get_absolute_url(self):
        return reverse("Nouriture_detail", kwargs={"pk": self.pk})
    def get_ajouter_pannier(self):
        return reverse("restaurant:ajouter-pannier", kwargs={"pk": self.pk})
class Pannier(models.Model):
    utilisateur = models.ForeignKey(User,on_delete=models.CASCADE)
    nouriture = models.ForeignKey(Nouriture,on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    commander =  models.BooleanField(default="False")
    def __str__(self):
        return self.nouriture.nom
    def get_absolute_url(self):
        return reverse("NouriturePannier_detail", kwargs={"pk": self.pk})
        
class Commande(models.Model):
    utilisateur = models.ForeignKey(User,on_delete=models.CASCADE)
    nouritures = models.ManyToManyField(Pannier)
    adresse = models.CharField(max_length=500,default="8 rue des flamboyant")
    code_postale = models.CharField(max_length=20,default="97300")
    ville = models.CharField(max_length=40,default="Cayenne")
    date_debut = models.DateField(auto_now=True)
    commander = models.BooleanField()
    def __str__(self):
        return self.utilisateur.username
    def get_absolute_url(self):
        return reverse("Categorie_detail", kwargs={"pk": self.pk})


