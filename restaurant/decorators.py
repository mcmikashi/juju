from .models import Nouriture,Pannier
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import  Sum,Count
def data_pannier(view_func):
    def wrap(request, *args, **kwargs):
        resultat = view_func(request, *args, **kwargs)
        if resultat:
            if isinstance(resultat,Nouriture):
                resultat = resultat.nom
            else:
                resultat = "Videz"
            totale_pannier = Pannier.objects.filter(utilisateur=request.user,commander=False).aggregate(totale_pannier=Sum(F('quantite') * F('nouriture__prix')),nombre_element=Count('id'))
            pannier_utilisateur = Pannier.objects.filter(utilisateur=request.user,commander=False).values("id","nouriture__nom","nouriture__prix","nouriture__image","quantite").order_by('nouriture__nom')
            data = {
                    'resultat':resultat,
                    'totale':totale_pannier.get("totale_pannier"),
                    'nombre':totale_pannier.get("nombre_element"),
                    'pannier': list(pannier_utilisateur)
            }
            return JsonResponse(data)
        else:
            return redirect("restaurant:index")
    return wrap