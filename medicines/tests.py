from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from medicines.models import Patient, Medicine

# Create your tests here.
class PatientsViewswtTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        med = baker.make("medicines.Medicine")
        doc = baker.make("medicines.Doctor")
        patient = baker.make("Patient", medicine = med, doctor = doc)

        r = self.client.get('/api/patients/')
        data = r.json()
        print(data)

        assert patient.lastName == data[0]['lastName']
        assert patient.doctor.id == data[0]['doctor']['id']
        assert patient.medicine.id == data[0]['medicine']['id']
        assert patient.id == data[0]['id']
        assert len(data) == 1

    def  test_create_patient(self):
        med = baker.make("medicines.Medicine")
        doc = baker.make("medicines.Doctor")

        print(med.id)
        print(doc.id)
        r = self.client.post("/api/patients/",{
            "lastName": 'Пациент',
            "firstName": 'Пациент',
            "patronymic": 'Пациент',
            "dateBirth": '10.08.2004',
            "number": '80000000000',
            "medicine": med.id,
            "doctor": doc.id,
        })
        assert r.status_code == 201
 
        new_patient_id = r.json()['id']

        patients = Patient.objects.all()
        assert len(patients) == 1

        new_patient = Patient.objects.filter(id=new_patient_id).first()
        assert new_patient.lastName == 'Пациент'
        assert new_patient.medicine == med
        assert new_patient.doctor == doc

    def test_delete_patient(self):
        patients = baker.make("Patient", 10)
        r = self.client.get('/api/patients/')
        data = r.json()
        assert len(data) == 10

        patient_id_to_delete = patients[3].id
        self.client.delete(f'/api/patients/{patient_id_to_delete}/')

        r = self.client.get('/api/patients/')
        data = r.json()
        assert len(data) == 9

        assert patient_id_to_delete not in [i['id'] for i in data]

    def test_update_patient(self):
        med = baker.make("medicines.Medicine")
        doc = baker.make("medicines.Doctor")
        patients = baker.make("Patient", 10)
        patient: Patient = patients[2]

        r = self.client.get(f'/api/patients/{patient.id}/') 
        data = r.json()
        assert data['lastName'] == patient.lastName

        r = self.client.put(f'/api/patients/{patient.id}/', {
            "lastName": "Фамилия",
            "firstName": 'Имя',
            "patronymic": 'Отчество',
            "dateBirth": '10.08.2004',
            "number": '80000000000',
            "medicine": med.id,
            "doctor": doc.id,
        }) 
        assert r.status_code==200

        r = self.client.get(f'/api/patients/{patient.id}/')
        data = r.json()
        assert data['lastName'] == "Фамилия"

        patient.refresh_from_db()
        assert data['lastName'] == patient.lastName

class MedicinesViewswtTestCase(TestCase):
    def test_get_list(self):
        form = baker.make("medicines.ReleaseForm")
        action = baker.make("medicines.TherapeuticAction")
        medicine = baker.make("Medicine", releaseForm = form, therapeuticAction = action)

        r = self.client.get('/api/medicines/')
        data = r.json()
        print(data)

        assert medicine.name == data[0]['name']
        assert medicine.releaseForm.id == data[0]['releaseForm']['id']
        assert medicine.therapeuticAction.id == data[0]['therapeuticAction']['id']
        assert medicine.id == data[0]['id']
        assert len(data) == 1

    def  test_create_medicine(self):
        form = baker.make("medicines.ReleaseForm")
        action = baker.make("medicines.TherapeuticAction")

        print(form.id)
        print(action.id)
        r = self.client.post("/api/medicines/",{
            "name": 'Лекарство',
            "releaseForm": form.id,
            "therapeuticAction": action.id,
        })
        assert r.status_code == 201
 
        new_medicine_id = r.json()['id']

        medicines = Medicine.objects.all()
        assert len(medicines) == 1

        new_medicine = Medicine.objects.filter(id=new_medicine_id).first()
        assert new_medicine.name == 'Лекарство'
        assert new_medicine.releaseForm == form
        assert new_medicine.therapeuticAction == action

    def test_delete_medicine(self):
        medicines = baker.make("Medicine", 10)
        r = self.client.get('/api/medicines/')
        data = r.json()
        assert len(data) == 10

        medicine_id_to_delete = medicines[3].id
        self.client.delete(f'/api/medicines/{medicine_id_to_delete}/')

        r = self.client.get('/api/medicines/')
        data = r.json()
        print(len(data))
        assert len(data) == 9

        assert medicine_id_to_delete not in [i['id'] for i in data]

    def test_update_medicine(self):
        form = baker.make("medicines.ReleaseForm")
        action = baker.make("medicines.TherapeuticAction")
        medicines = baker.make("Medicine", 10)
        medicine: Medicine = medicines[2]

        r = self.client.get(f'/api/medicines/{medicine.id}/') 
        data = r.json()
        assert data['name'] == medicine.name

        r = self.client.put(f'/api/medicines/{medicine.id}/', {
            "name": "Лекарство",
            "releaseForm": form.id,
            "therapeuticAction": action.id,
        },content_type="application/json") 
        assert r.status_code==200

        r = self.client.get(f'/api/medicines/{medicine.id}/')
        data = r.json()
        assert data['name'] == "Лекарство"

        medicine.refresh_from_db()
        assert data['name'] == medicine.name

