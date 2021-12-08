from django.urls import path
from .views import NouritureListView,CommandeCreate,LoginFormView,InscriptionFormView,ContactFormViews,PasswordResetViewB,PasswordChangeViewB,ResetDoneView,ajouterNourriture,viderPannier,effacerPannier,categorieCarte,rechercheCarte,logout_view
app_name = "restaurant"

urlpatterns = [
    path('', NouritureListView.as_view(),name="index"),
    path('ajouter-pannier/<int:id>', ajouterNourriture,name="ajouter_pannier"),
    path('delete-pannier/<int:id>', effacerPannier,name="delete_pannier"),
    path('vider-pannier/', viderPannier,name="vider_pannier"),
    path('recherche-nouriture/<str:recherche>', rechercheCarte,name="cherche_carte"),
    path('categorie-nouriture/<int:id>', categorieCarte,name="categorie_nouriture"),
    path('commande/', CommandeCreate.as_view(),name="commande"),
    path('contact', ContactFormViews.as_view(),name="contact"),
    #Gestion utilisateur
    path('compte/login', LoginFormView.as_view(),name="login"),
    path('compte/logout', logout_view,name="logout"),
    path('compte/inscription', InscriptionFormView.as_view(),name="inscription"),
    path('compte/reset_password', PasswordResetViewB.as_view(),name="password_reset"),
    path('compte/reset_done', ResetDoneView.as_view(),name="password_reset_done"),
    path('compte/change_password/<uidb64>/<token>', PasswordChangeViewB.as_view(),name="password_reset_confirm"),
]
