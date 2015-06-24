from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from menus.models import Profile, Account

__author__ = 'kiyoakimenager'

from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Utilisateur'}),
        label='Utilisateur')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        label='Mot de passe')

    user_cache = None
    error_messages = ""
    error_code = 400

    def clean(self):
        cleaned_data = super(SignInForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                self.error_messages = "Identifiant ou mot de passe invalide"
                self.error_code = 403
                raise forms.ValidationError("auth failed")
            else:
                if not self.user_cache.is_active:
                    self.error_messages = "Utilisateur innactif"
                    self.error_code = 403
                    raise forms.ValidationError("user inactive")

        return cleaned_data


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Utilisateur'}),
        label='Utilisateur')
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        label='Mot de passe')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmation du mot de passe'}),
        label='Confirmation du mot de passe')

    user_cache = None

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        return cleaned_data

    def save(self, commit=True):
        self.user_cache = super(RegistrationForm, self).save(commit=False)
        self.user_cache.username = self.cleaned_data['username']
        self.user_cache.set_password(self.cleaned_data['password1'])

        if commit:
            self.user_cache.save()
            profile = Profile()
            profile.save()
            # profile.owner = self.user_cache

            account = Account()
            account.profile = profile
            account.user = self.user_cache
            account.save()
