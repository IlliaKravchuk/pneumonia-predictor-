from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from keras.src.ops import scan
from .utils import *
from .models import *
from .forms import *

# Create your views here.
class ClinicalDataView(LoginRequiredMixin, CreateView):
    model = ClinicalData
    form_class = ClinicalDataForm
    template_name = 'diagnosis/clinical_data.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)

        psi_score = calculate_psi_score(self.object)
        risk_class, mortality = get_risk_class(psi_score)

        self.object.psi_score = psi_score
        self.object.risk_class = risk_class
        self.object.mortality_prediction = mortality

        self.object.save()
        return redirect('diagnosis:diagnosis_cd', pk=self.object.pk)

def DiagnosisClinicalDataView(request, pk):
    clinical_record = get_object_or_404(ClinicalData, pk=pk)
    if clinical_record.user != request.user:
        return redirect('home')

    context = {'clinical_record': clinical_record}

    return render(request, 'diagnosis/diagnosis_clinical_data.html', context)

class XRayDataView(LoginRequiredMixin, CreateView):
    model = XRayData
    form_class = DiagnosisForm
    template_name = 'diagnosis/xray_data.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        img = self.object.image.path

        try:
            result, confidence = calculate_xray_probability(img)

            self.object.result = result
            self.object.confidence = confidence
            self.object.save(update_fields=['result', 'confidence'])

        except Exception as e:
            print(f"ML Error: {e}")
            self.object.result = "Помилка аналізу"
            self.object.confidence = 0.0
            self.object.save()

        return redirect('diagnosis:diagnosis_xrd', pk=self.object.pk)

def DiagnosisXRayDataView(request, pk):
    scan_result = get_object_or_404(XRayData, pk=pk)
    if scan_result.user != request.user:
        return redirect('home')

    context = {'scan_result': scan_result}

    return render(request, 'diagnosis/diagnosis_xray_data.html', context)

def InfoView(request):
    return render(request, 'diagnosis/info.html')

@login_required
def HistoryView(request):
    clinical_records = ClinicalData.objects.filter(user=request.user).order_by('-created_at')[:5]
    xray_records = XRayData.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'clinical_records': clinical_records,
        'xray_records': xray_records,
    }
    return render(request, 'diagnosis/history.html', context)