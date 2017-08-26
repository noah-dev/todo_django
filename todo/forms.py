# WIP - NOT YET OPERATIONAL
from django import forms

from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title_text', 'desc_text', 'impact_text']