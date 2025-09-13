from django import forms
from .models import Plant, Accessory, CareAction

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'species', 'description', 'growth_stage', 'health', 'accessories']


class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['name', 'type', 'description']


class CareActionForm(forms.ModelForm):
    class Meta:
        model = CareAction
        fields = ['action_type', 'notes']
