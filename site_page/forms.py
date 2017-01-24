from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']



