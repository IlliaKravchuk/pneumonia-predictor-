from django.urls import path
from .views import *

app_name = 'diagnosis'

urlpatterns = [
    path('clinical_data/', ClinicalDataView.as_view(), name='clinical_data'),
    path('diagnosis_cd/<int:pk>', DiagnosisClinicalDataView, name='diagnosis_cd'),
    path('xray_data/', XRayDataView.as_view(), name='xray_data'),
    path('diagnosis_xrd/<int:pk>', DiagnosisXRayDataView, name='diagnosis_xrd'),
    path('info/', InfoView, name='info'),
    path('history/', HistoryView, name='history'),
]