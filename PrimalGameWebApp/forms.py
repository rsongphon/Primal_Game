from PrimalGameAPI.models import Primals
from django import forms

class PrimalsForm(forms.Form):
    name = forms.CharField(max_length=255)