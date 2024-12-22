from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from medicines.serializers import PatientSerializer, MedicineSerializer, DoctorSerializer, ReleaseFormSerializer, TherapeuticActionSerializer, MedicineGetSerializer, PatientGetSerializer
from medicines.models import Patient, Medicine, Doctor, ReleaseForm, TherapeuticAction
from rest_framework.decorators import action
from openpyxl import Workbook
from io import BytesIO
from django.http import HttpResponse


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

    @action(detail=False, methods=['get'], url_path='export-excel')
    def export_to_excel(self, request, *args, **kwargs):
        # Создаем Excel документ
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Patients"

        # Добавляем заголовки
        headers = ["ID", "Фамилия", "Имя", "Отчество", "Дата рождения", "Номер телефона"]
        sheet.append(headers)

        # Добавляем данные из модели 
        for p in Patient.objects.all():
            sheet.append([
                p.id,
                p.lastName,
                p.firstName,
                p.patronymic,
                p.dateBirth,
                p.number
            ])

        # Сохраняем Excel в байтовый поток
        stream = BytesIO()
        workbook.save(stream)
        stream.seek(0)

        # Возвращаем файл через API
        response = HttpResponse(
            stream,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="Patients.xlsx"'
        return response   

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

