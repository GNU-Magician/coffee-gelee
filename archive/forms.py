from django import forms
from .models import Post, Category, Tag
from django.conf import settings
import datetime


class NameForm(forms.Form):
    choices = (
        (True, ('Everyone')),
        (False, ('Just Friends'))
    )
    name = forms.CharField(label="The post's name", max_length=100)
    category = forms.ChoiceField(choices=[(obj.id, str(obj)) for obj in Category.objects.all()], label='Category')
    description = forms.CharField(max_length=5000, label='Description', widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "20", }))
    file = forms.FileField(label='Select the file to be uploaded.')
    can_see = forms.ChoiceField(choices=choices, label="Who can see this?")

    class Meta:
        model = Post


class UpdateForm(forms.Form):
    choices = (
        (True, ('Everyone')),
        (False, ('Just Friends'))
    )
    name = forms.CharField(label="The post's name", max_length=100)
    category = forms.ChoiceField(choices=[(obj.id, str(obj)) for obj in Category.objects.all()], label='Category')
    description = forms.CharField(max_length=5000, label='Description', widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "20", }))
    file = forms.FileField(label='Select the file to be uploaded.')
    can_see = forms.ChoiceField(choices=choices, label="Who can see this?")

    class Meta:
        model = Post


class RegisterForm(forms.Form):
    username = forms.CharField(label="Your username")
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
