from rest_framework import serializers

from medicines.models import Medicine, Patient, Doctor, ReleaseForm, TherapeuticAction

class TherapeuticActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapeuticAction
        fields = ['id', 'action']

class ReleaseFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseForm
        fields = ['id', 'form']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name']

class MedicineGetSerializer(serializers.ModelSerializer):
    releaseForm = ReleaseFormSerializer(read_only=True)
    therapeuticAction = TherapeuticActionSerializer(read_only=True)
    class Meta:
        model = Medicine
        fields = ['id', "name", 'releaseForm', 'therapeuticAction']

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', "name", 'releaseForm', 'therapeuticAction']

class PatientGetSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    doctor = DoctorSerializer(read_only=True)
    medicine = MedicineSerializer(read_only=True)
    class Meta:
        model = Patient
        fields = ['id', 'lastName', 'firstName', 'patronymic', 'dateBirth', 'number', 'doctor', 'medicine', 'picture', 'user']

class PatientSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        model = Patient
        fields = ['id', 'lastName', 'firstName', 'patronymic', 'dateBirth', 'number', 'doctor', 'medicine', 'picture', 'user']

    