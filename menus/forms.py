from django.contrib.auth.models import User

__author__ = 'kiyoakimenager'

from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Utilisateur'}),
                               label='Utilisateur')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
                                label='Mot de passe')

    def clean(self):
        cleaned_data = super(SignInForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        return cleaned_data

class RegistrationForm(forms.Form):
    username = forms.EmailField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Utilisateur'}),
                               label='Utilisateur')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
                                label='Mot de passe')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmation du mot de passe'}),
                                label='Confirmation du mot de passe')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        return cleaned_data

    class Meta:
        model = User
