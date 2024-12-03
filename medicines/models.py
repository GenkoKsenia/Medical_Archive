from django.db import models

# Create your models here.
class Patient(models.Model):
    lastName = models.TextField("Фамилия")
    firstName = models.TextField("Имя")
    patronymic = models.TextField("Отчество")
    dateBirth = models.TextField("Дата рождения")
    number = models.TextField("Номер телефона")
    medicine = models.ForeignKey("Medicine", on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, null=True)

    picture = models.ImageField("Изображение", null=True, upload_to="patients")
    
    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
    
class Medicine(models.Model):
    name = models.TextField("Название")
    releaseForm = models.ForeignKey("ReleaseForm", on_delete=models.CASCADE, null=True)
    therapeuticAction = models.ForeignKey("TherapeuticAction", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Лекарство"
        verbose_name_plural = "Лекарства"

    def __str__(self) -> str:
        return self.name
    
class Doctor(models.Model):
    name = models.TextField("ФИО")

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self) -> str:
        return self.name
    
class ReleaseForm(models.Model):
    form = models.TextField("Форма")

    class Meta:
        verbose_name = "Форма выпуска"
        verbose_name_plural = "Формы выпуска"

    def __str__(self) -> str:
        return self.form
    
class TherapeuticAction(models.Model):
    action = models.TextField("действие")

    class Meta:
        verbose_name = "Терапевтическое действие"
        verbose_name_plural = "Терапевтические действия"

    def __str__(self) -> str:
        return self.action
    
