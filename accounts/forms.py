from django import forms 
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser


        
class SignupForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name']        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'profile_pix')