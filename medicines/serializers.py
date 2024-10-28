from rest_framework import serializers

from medicines.models import Medicine, Patient, Doctor, ReleaseForm, TherapeuticAction

class TherapeuticActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapeuticAction
        fields = "__all__"

class ReleaseFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseForm
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"

class PatientSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    class Meta:
        model = Patient
        fields = ['id', 'lastName', 'medicine']