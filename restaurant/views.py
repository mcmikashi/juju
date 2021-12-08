from django.db.models.expressions import Exists
from django.shortcuts import get_object_or_404,redirect
from django.views.generic import ListView,CreateView,FormView,TemplateView
from .models import Nouriture,Commande,Pannier,Categorie
from django.db.models import  Sum,Count,F
from django.urls import reverse_lazy
from .decorators import data_pannier
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import  UserLoginForm,InscriptionForm,ContactForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView

class NouritureListView(LoginRequiredMixin,ListView):
    login_url = 'compte/login'
    model = Nouriture
    template_name = "restaurant/nouriture_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pannier"] = Pannier.objects.filter(utilisateur=self.request.user,commander=False).order_by('nouriture__nom')
        context["categorie"] = Categorie.objects.all()
        context["pannier_tc"] = Pannier.objects.filter(utilisateur=self.request.user,commander=False).aggregate(totale_pannier=Sum(F('quantite') * F('nouriture__prix')),nombre_element=Count('id'))
        return context
class LoginFormView(FormView):
    template_name = 'compte/login.html'
    form_class = UserLoginForm
    success_url = '/'
    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if user is not None:
            login(self.request, user)
        else:
            redirect("restaurant:login")
        return super().form_valid(form)

class ContactFormViews(FormView):
    template_name = 'restaurant/contact.html'
    form_class = ContactForm
    success_url = 'contact' 
    def form_valid(self, form):
        message = f"{form.cleaned_data.get('nom')} \n {form.cleaned_data.get('email')} \n {form.cleaned_data.get('message')}"
        send_mail(subject={form.cleaned_data.get('sujet')},message=message,from_email="guyanebbc@gmail.com",recipient_list=["mickaelanicette@gmail.com"])
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pannier"] = Pannier.objects.filter(utilisateur=self.request.user,commander=False).order_by('nouriture__nom')
        context["pannier_tc"] = Pannier.objects.filter(utilisateur=self.request.user,commander=False).aggregate(totale_pannier=Sum(F('quantite') * F('nouriture__prix')),nombre_element=Count('id'))
        return context
class InscriptionFormView(FormView):
    template_name = 'compte/inscription.html'
    form_class = InscriptionForm
    success_url = 'login' 
    def form_valid(self, form):
        user = User.objects.create_user(username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password1'),email=form.cleaned_data.get('email'),first_name=form.cleaned_data.get('prenom'),last_name=form.cleaned_data.get('nom'))
        return super().form_valid(form)
def logout_view(request):
    logout(request)
    return redirect("restaurant:login")
@login_required
def rechercheCarte(request,recherche):
    carte_recherche = Nouriture.objects.filter(nom__icontains=recherche).values()
    data = {
            'carte': list(carte_recherche),
    }
    return JsonResponse(data)
@login_required
def categorieCarte(request,id):
    if id ==0:
        carte_recherche = Nouriture.objects.all().values()
    else:
        categorie = get_object_or_404(Categorie,id=id)
        carte_recherche = Nouriture.objects.filter(categorie=categorie).values()
    data = {
            'carte': list(carte_recherche),
    }
    return JsonResponse(data)
@login_required
@data_pannier
def ajouterNourriture(request,id):
    nouriture = get_object_or_404(Nouriture,id=id)
    nouriture_pannier_rc = Pannier.objects.filter(nouriture=nouriture,utilisateur=request.user,commander=False)
    if nouriture_pannier_rc.exists():
        nouriture_select_pannier = nouriture_pannier_rc[0]
        nouriture_select_pannier.quantite += 1 
        nouriture_select_pannier.save()
    else:
        nouvelle_item_pannier = Pannier.objects.create(nouriture=nouriture,utilisateur=request.user,quantite=1)
        nouvelle_item_pannier.save()
    return nouriture

@login_required
@data_pannier
def viderPannier(request):
    pannier_rc = Pannier.objects.filter(utilisateur=request.user,commander=False)
    if pannier_rc.exists():
        pannier_rc.delete()
    return True
@login_required
@data_pannier
def effacerPannier(request,id):
    ligne_pannier_rc = Pannier.objects.filter(id=id,utilisateur=request.user,commander=False)
    nouriture = get_object_or_404(Nouriture,id=ligne_pannier_rc[0].nouriture.id)
    ligne_pannier_rc.delete()
    return nouriture
class CommandeCreate(LoginRequiredMixin,CreateView):
    login_url = 'compte/login'
    model = Commande
    fields = ["adresse","code_postale","ville"]
    template_name = "restaurant/nouvelle_commande.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pannier"] = Pannier.objects.filter(utilisateur=self.request.user,commander=False).order_by('nouriture__nom')
        context["pannier_tc"] = Pannier.objects.filter(utilisateur=self.request.user,commander=False).aggregate(totale_pannier=Sum(F('quantite') * F('nouriture__prix')),nombre_element=Count('id'))
        print(context["pannier_tc"])
        return context
    def form_valid(self, form):
        adresse = form.cleaned_data.get('adresse')
        code_postale = form.cleaned_data.get('code_postale')
        ville = form.cleaned_data.get('ville')
        utilisateur = self.request.user 
        commande = Commande.objects.create(utilisateur=utilisateur ,adresse=adresse,code_postale=code_postale,ville=ville,commander=True)
        list_pannier = Pannier.objects.filter(utilisateur=utilisateur,commander=False)
        commande.nouritures.add(*list_pannier)
        commande.save()
        list_pannier.update(commander=True)
        return redirect("restaurant:index")

class PasswordResetViewB(PasswordResetView):
    template_name = "compte/mdp_reset.html"
    success_url= "reset_done"
    email_template_name = 'compte/email/reset_password.txt'
    def get_form(self):
        form = super(PasswordResetViewB, self).get_form()
        for visible in form.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        return form
class PasswordChangeViewB(PasswordResetConfirmView):
    template_name = "compte/mdp_change.html"
    success_url= "/compte/login"
    def get_form(self):
        form = super(PasswordChangeViewB, self).get_form()
        for visible in form.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        return form
class ResetDoneView(TemplateView):
    template_name = "compte/reset_done.html"
