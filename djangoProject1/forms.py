from django import forms
from .models import CustomUser

class AvatarForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar',)