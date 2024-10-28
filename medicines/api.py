from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from medicines.serializers import PatientSerializer, MedicineSerializer, DoctorSerializer, ReleaseFormSerializer, TherapeuticActionSerializer
from medicines.models import Patient, Medicine, Doctor, ReleaseForm, TherapeuticAction


class PatientsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class MedicineViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

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

