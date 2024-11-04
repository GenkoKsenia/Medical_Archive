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
    GenericViewSet
    ):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class ReleaseFormViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):
    queryset = ReleaseForm.objects.all()
    serializer_class = ReleaseFormSerializer

class TherapeuticActionViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):
    queryset = TherapeuticAction.objects.all()
    serializer_class = TherapeuticActionSerializer

