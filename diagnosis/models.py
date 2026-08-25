from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.conf import settings
from .utils import *

class ClinicalData(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пацієнт"
    )

    GENDER_CHOICES = [
        ('M', 'Чоловік'),
        ('F', 'Жінка'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name="Стать")

    age = models.PositiveIntegerField(verbose_name="Вік")
    cough = models.BooleanField(default=False, verbose_name="Кашель")
    rasp = models.BooleanField(default=False, verbose_name="Хрипи")
    cancer = models.BooleanField(default=False, verbose_name="Онкологічні захворювання")
    liver_disease = models.BooleanField(default=False, verbose_name="Захворювання печінки")
    heart_disease = models.BooleanField(default=False, verbose_name="Серцева недостатність")
    cerebrovascular_disease = models.BooleanField(default=False, verbose_name="Цереброваскулярні хвороби (інсульт)")
    renal_disease = models.BooleanField(default=False, verbose_name="Захворювання нирок")
    nursing_home = models.BooleanField(default=False, verbose_name="Проживання в будинку престарілих")
    altered_mental_status = models.BooleanField(default=False, verbose_name="Сплутаність свідомості")

    respiratory_rate = models.PositiveIntegerField(
        verbose_name="Частота дихання (вдихів/хв)",
        default=18,
        validators=[MinValueValidator(5), MaxValueValidator(80)]
    )
    systolic_bp = models.PositiveIntegerField(
        verbose_name="Систолічний тиск (верхній)",
        default=120,
        validators=[MinValueValidator(40), MaxValueValidator(300)]
    )
    pulse = models.PositiveIntegerField(
        verbose_name="Пульс (уд/хв)",
        default=70,
        validators=[MinValueValidator(30), MaxValueValidator(250)]
    )
    temperature = models.FloatField(
        verbose_name="Температура (°C)",
        validators=[MinValueValidator(30.0), MaxValueValidator(45.0)]
    )
    hemoglobin = models.FloatField(
        verbose_name="Гемоглобін (г/л)",
        validators=[MinValueValidator(20.0), MaxValueValidator(250.0)]
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата аналізу")

    psi_score = models.IntegerField(
        null=True, blank=True,
        verbose_name="Бал PSI"
    )
    risk_class = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name="Клас ризику"
    )
    mortality_prediction = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name="Прогноз смертності"
    )

    def __str__(self):
        return f"Аналіз користувача {self.user.username} від {self.created_at.strftime('%d.%m.%Y')}"

class XRayData(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to=user_directory_path,
        verbose_name="Рентген",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    confidence = models.FloatField(blank=True, null=True)
    result = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата аналізу")

    def __str__(self):
        return f"Знімок {self.id} від {self.user.username}"