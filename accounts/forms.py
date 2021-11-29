from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User, Profile
from django.contrib import messages
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.core.validators import RegexValidator

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        try:
            User.objects.get(username__exact=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("This username is already taken.")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('__all__')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class UserProfileForm(forms.ModelForm):   
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = forms.ChoiceField(
        label='Gender', choices=GENDER, widget=forms.RadioSelect, required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=False)
    phonenumber = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='IN')
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phonenumber', 'country', 'avatar', 'address', 'gender',
                  'date_of_birth', 'pincode', 'language', 'location', 'website', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'your last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you emai@gmail.com'}),
            'country': forms.TextInput(attrs={'placeholder': 'country you where you live'}),
            'address': forms.TextInput(attrs={'placeholder': 'your address where you live'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'pincode'}),
            'language': forms.TextInput(attrs={'placeholder': 'language'}),
            'location': forms.TextInput(attrs={'placeholder': 'location'}),
            'bio': forms.TextInput(attrs={'placeholder': 'about you'}),
            'website': forms.TextInput(attrs={'placeholder': 'your website url e.g. https://your_website.com'}),
        }
