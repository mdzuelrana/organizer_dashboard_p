from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User,Group,Permission
from django import forms
import re

from tasks.forms import StyledFormMixin
class RegisterForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','password1','password2','email']
    def __init__(self,*args,**kwargs):
        super(UserCreationForm,self).__init__(*args,**kwargs)
        
        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text=None
            
            
class CustomRegisterForm(StyledFormMixin,forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        
    def clean_password(self):
        password=self.cleaned_data.get('password')
        errors=[]
        if len(password)<8:
            errors.append('password must be at least 8 character long')
        if not re.search(r'[A-Z]',password):
            errors.append('Password must be uppercase')
        if not re.search(r'[a-z]',password):
            errors.append('Password must be lowercase')
        if not re.search(r'\d',password):
            errors.append('Password must be number')
        if not re.search(r'[@#$%^&+=]',password):
            errors.append('Password must be special character')
        if errors:
            raise forms.ValidationError(errors)
        return password
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password do not match')
        return cleaned_data
    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_exists=User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError('Email already exists')
        return email

class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class AssignRoleForm(StyledFormMixin,forms.Form):
    role=forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label='Select a Role'
    )
    

class CreateGroupForm(StyledFormMixin,forms.ModelForm):
    permission=forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='AssignPermission'
    )
    class Meta:
        model=Group
        fields=['name','permission']