from django import forms
from .models import *

class ClinicalDataForm(forms.ModelForm):
    class Meta:
        model = ClinicalData
        exclude = ('user', 'psi_score', 'risk_class', 'mortality_prediction')

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = XRayData
        fields = ('image',)
