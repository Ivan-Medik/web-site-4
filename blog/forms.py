from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'id')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["title", "slug"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')

        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. we have "{}" slug already.'.format(new_slug))
        return new_slug


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "body", "tags"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')

        return new_slug

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user_name", "user_id", "status", "friends", "profile_id"]

        user_name = models.CharField(max_length=150, db_index=True)
        user_id = models.CharField(max_length=150, db_index=True)
        status = models.CharField(max_length=150, db_index=True)
        friends = models.CharField(max_length=150, db_index=True)
        profile_id = models.CharField(max_length=150, db_index=True)

        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_id': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'friends': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_id':forms.TextInput(attrs={'class': 'form-control'}),
        }

