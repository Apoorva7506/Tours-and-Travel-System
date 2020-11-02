from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.conf.urls import url
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import path, include
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

class AddUserForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            'email', 'username', 'fname','mname','lname', 'phone' , 'age', 'houseno','city','state' 'password'
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'password','username', 'fname','mname','lname', 'phone' , 'age', 'houseno','city','state'
        )

    def clean_password(self):
        # Password can't be changed in the admin
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('email',  'phone',
                    'is_staff', 'username', 'fname','mname','lname', 'phone' , 'age', 'houseno','city','state')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ['name', 'username', 'phone', 'username', 'fname','mname','lname', 'phone' , 'age', 'houseno','city','state']}),

    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',  'phone', 'username', 'password1',
                    'password2', 'fname','mname','lname', 'phone' , 'age', 'houseno','city','state'
                )
            }
        ),
    )
    search_fields = ('email', 'fname')
    ordering = ('email', 'username', 'fname')
    filter_horizontal = ()


# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerNumber)
admin.site.register(Destination)
admin.site.register(PopularSpots)
admin.site.register(Hotel)
admin.site.register(Luxury)