from django.core.management.base import BaseCommand

from faker import Faker

from medicines.models import Patient, Medicine, Doctor, ReleaseForm, TherapeuticAction

import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        for _ in range(100):
            #врачи
            def generate_full_name():
                last_name = fake.last_name() 
                first_name = fake.first_name()  
                patronymic = fake.middle_name() 
                return f"{last_name} {first_name} {patronymic}"
            
            Doctor.objects.create(
                name = generate_full_name()
            )
            
            #лекарства
            prefixes = ['Кардио', 'Вита', 'Меди', 'Тера', 'Имуно', 'Флюро']
            suffixes = ['норм', 'таб', 'плюс', 'кур', 'сейф', 'капс']

            def generate_medicine_name():
                prefix = random.choice(prefixes)
                suffix = random.choice(suffixes)
                return f"{prefix}{suffix}"

            releaseForm_instance = ReleaseForm.objects.order_by('?').first()
            therapeuticAction_instance = TherapeuticAction.objects.order_by('?').first()
            Medicine.objects.create(
                name = generate_medicine_name(),   
                releaseForm = releaseForm_instance,                
                therapeuticAction = therapeuticAction_instance
            )

            #пациенты
            medicine_instance = Medicine.objects.order_by('?').first()
            doctor_instance = Doctor.objects.order_by('?').first()
            Patient.objects.create(
                lastName = fake.last_name(),   
                firstName = fake.first_name(),                
                patronymic = fake.middle_name(),
                dateBirth = fake.date_of_birth(),
                number = fake.phone_number(),
                medicine=medicine_instance,   
                doctor=doctor_instance   
            )