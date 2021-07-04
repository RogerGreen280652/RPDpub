from django.db import models

class RpdDocument(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

class RpdDocumentTitle(models.Model):
    document_id = models.ForeignKey(RpdDocument, on_delete=models.CASCADE)
    date = models.DateField()
    discipline_name = models.CharField(max_length=255)
    direction_name = models.CharField(max_length=255)

class RpdDocumentTargets(models.Model):
    document_id = models.ForeignKey(RpdDocument, on_delete=models.CASCADE)
    targets = models.TextField()

class RpdDocumentTask(models.Model):
    document_id = models.ForeignKey(RpdDocument, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)

class RpdPlaceDiscipline(models.Model):
    document_id = models.ForeignKey(RpdDocument, on_delete=models.CASCADE)
    disciplines = models.TextField()
    type = models.IntegerField()

# Модель - компетенции
class Competence(models.Model):
    code =models.CharField(max_length=255)
    oop_code =models.CharField(max_length=255)
    competence_code =models.CharField(max_length=255)
    competence_name =models.TextField()


# Модель - дисциплины
class Discipline(models.Model):
    code =models.CharField(max_length=255)
    plane_code =models.CharField(max_length=255)
    oop_code =models.CharField(max_length=255)
    block_code =models.CharField(max_length=255)
    discipline_name =models.CharField(max_length=255)
    discipline_code =models.CharField(max_length=255)
    hours_in_zet =models.CharField(max_length=255)
    hours_po_zet =models.CharField(max_length=255)


# Модель - КомпетенцииДисциплины
class CompetenceDiscipline(models.Model):
    competence_code =models.CharField(max_length=255)
    discipline_code =models.CharField(max_length=255)


# Модель - профиль подготовки
class Standart(models.Model):
    code =models.CharField(max_length=255)
    group_code =models.CharField(max_length=255)
    name =models.CharField(max_length=255)
    purpose =models.TextField()


# Модель - СправочникВидыРабот
class ReferenceTypesWork(models.Model):
    code =models.CharField(max_length=255)
    work_name =models.CharField(max_length=255)
    code_type_work =models.CharField(max_length=255)
    abbreviation =models.CharField(max_length=255)


class DataBase(models.Model):

    # Метод, результатом которого является список компетенций по заданной дисциплине
    def get_competences(self, disc_name):
        competence_lst = []
        disc_code = Discipline.select().where(Discipline.discipline_name == disc_name).get().code
        for item in CompetenceDiscipline.select().where(CompetenceDiscipline.discipline_code == disc_code):
            competence = Competence.get(Competence.code == item.competence_code)
            competence_lst.append({competence.competence_code: competence.competence_name})
        return competence_lst

    def get_standarts(self):
        return Standart.objects.all()

    # Метод результатом которого является список дисциплин
    def get_disciplines(self):
        return Discipline.objects.all()

    # Метод, результатом которого является список профилей подготовки
    def get_profiles(self):
        profiles = []
        for item in Standart.select():
            profiles.append(item.name)
        return profiles

    def get_hours(self, disc_name):
        hours = []
        for item in Discipline.select().where(Discipline.discipline_name == disc_name):
            all_hours = item.hours_po_zet
            exam_hours = item.hours_in_zet
            credit_units = int(all_hours) // int(exam_hours)
            hours.append(credit_units)
            hours.append(all_hours)
            hours.append(exam_hours)
        return hours

    def get_work_type(self):
        work_types = []
        for item in ReferenceTypesWork.select().where(ReferenceTypesWork.code_type_work == '7').order_by(ReferenceTypesWork.work_name.asc()):
            work_types.append(item.work_name)
        return work_types