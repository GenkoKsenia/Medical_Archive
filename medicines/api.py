from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from medicines.serializers import PatientSerializer, MedicineSerializer, DoctorSerializer, ReleaseFormSerializer, TherapeuticActionSerializer, MedicineGetSerializer, PatientGetSerializer
from medicines.models import Patient, Medicine, Doctor, ReleaseForm, TherapeuticAction


class PatientsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Patient.objects.all()
    

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PatientGetSerializer
        return PatientSerializer
    
    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        return qs.filter(user=user)      

class MedicineViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Medicine.objects.all()
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MedicineGetSerializer
        return MedicineSerializer



class DoctorViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class ReleaseFormViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = ReleaseForm.objects.all()
    serializer_class = ReleaseFormSerializer

class TherapeuticActionViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = TherapeuticAction.objects.all()
    serializer_class = TherapeuticActionSerializer

