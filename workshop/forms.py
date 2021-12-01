from .models import Review, AdminRequest
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["workshop", "theme", "text"]
        widgets = {
            "theme": forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Введите тему отзыва'
            }),
            "text": forms.Textarea(attrs = {
                'class': 'form-control',
                'placeholder': 'Введите отзыв'
            }),
        }


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AdminReqForm(forms.ModelForm):
    class Meta:
        model = AdminRequest
        fields = ["req"]
        widgets = {"req": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите запрос'})}