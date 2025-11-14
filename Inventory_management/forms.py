from .models import Profile
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username','email','password']
        help_texts ={
            'username' : None
        }


        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')
            if password != confirm_password:
                raise forms.ValidationError('Password Not Matching')
            return cleaned_data
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'profile_pic']