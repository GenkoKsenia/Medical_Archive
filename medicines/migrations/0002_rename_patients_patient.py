# Generated by Django 5.1.2 on 2024-10-28 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Patients',
            new_name='Patient',
        ),
    ]
