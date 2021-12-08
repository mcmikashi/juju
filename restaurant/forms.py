from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms
from django.db.models.fields import TextField
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email')
    nom = forms.CharField(max_length=25, required=True,label="Nom")
    prenom = forms.CharField(max_length=25, required=True,label="Prenom")
    field_order = ['nom', 'prenom','email']
    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class ContactForm(forms.Form):
    nom = forms.CharField(max_length=50, required=True,label="Nom")
    email = forms.EmailField(required=True,label='Email')
    sujet = forms.CharField(max_length=150, required=True,label="Sujet")
    message = forms.CharField(max_length=2500, required=True,widget=forms.Textarea(attrs={"rows":"3"}))
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'