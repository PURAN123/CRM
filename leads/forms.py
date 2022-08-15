
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Agent, Lead

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model= Lead
        fields=(
            "first_name",
            "last_name",
            "age",
            "agent"
        )


class Leadform(forms.Form):
    first_name= forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    age= forms.IntegerField(min_value=0)


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class LeadAssignFrom(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        queryset = Agent.objects.filter( organisation = request.user.userprofile )
        super(LeadAssignFrom, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = queryset


