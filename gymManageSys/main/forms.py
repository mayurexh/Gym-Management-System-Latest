from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ('full_name','email','details')

class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name","last_name", "email", "username" ,"password1", "password2")

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name","last_name", "email", "username")

class TrainerLoginForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ("username", "pwd")


class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ("full_name","mobile","details","img")

class TrainerChangePassword(forms.Form):
    old_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    
class ReportForTrainerForm(forms.ModelForm):
    class Meta:
        model = TrainerSubscriberReport
        fields = ('report_for_trainer', 'report_msg')


class ReportForUserForm(forms.ModelForm):
    class Meta:
        model = TrainerSubscriberReport
        fields = ('report_for_user', 'report_msg')
