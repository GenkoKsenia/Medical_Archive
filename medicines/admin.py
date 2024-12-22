from django.contrib import admin

from medicines.models import Medicine, Patient, Doctor, ReleaseForm, TherapeuticAction

# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['lastName', 'firstName', 'patronymic', 'dateBirth', 'number', 'medicine__name', 'user']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ReleaseForm)
class ReleaseFormAdmin(admin.ModelAdmin):
    list_display = ['form']

@admin.register(TherapeuticAction)
class TherapeuticActionAdmin(admin.ModelAdmin):
    list_display = ['action']