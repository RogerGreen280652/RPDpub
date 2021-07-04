from django.shortcuts import render, redirect
from django.http.response import HttpResponse

import datetime
import os
import mimetypes
import re

from .models import RpdDocument, RpdDocumentTitle, RpdDocumentTargets, RpdDocumentTask, RpdPlaceDiscipline, DataBase

def download_file(request):
    doc_id = request.GET['id']

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'test.txt'
    filepath = BASE_DIR + '/files/' + filename


    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response

# Create your views here.
def index(request):
    documents = RpdDocument.objects.all()
    context = {'documents': documents}

    if(request.method == 'POST'):
        rpdDocObj = RpdDocument.objects.get(id=request.POST['deleteDocId'])
        rpdDocObj.delete()

    return render(request, "index.html", context)

def creationDocumentTitle(request):

    obj = DataBase()

    context = {
        'discipline_list': obj.get_disciplines(),
        'standarts_list': obj.get_standarts(),
        'date': "",
        'date_error': "",
        'discipline_name': "Выберите дисциплину",
        'discipline_name_error': "",
        'direction': "Выберите стандарт",
        'direction_error': ""
    }

    if(request.method == 'POST'):
        context['date'] = request.POST['date']
        if(not re.match(r"\d\d.\d\d.\d\d\d\d", context['date'])):
            context['date_error'] = "Некорректно введена дата"
        
        context['discipline_name'] = request.POST['discipline_name']
        if(context['discipline_name'] == "Выберите дисциплину"):
            context['discipline_name_error'] = "Выберите дисциплину"

        context['direction'] = request.POST['direction']
        if(context['direction'] == 'Выберите стандарт'):
            context['direction_error'] = "Выберите стандарт"

        if(len(context['date_error']) == 0 and len(context['discipline_name_error']) == 0 and len(context['direction_error']) == 0):
            doc_obj = RpdDocument(
                name = context['discipline_name'] + ".docx",
                date = datetime.datetime.now()
            )
            doc_obj.save()
            RDTobj = RpdDocumentTitle(
                document_id = doc_obj,
                date = datetime.datetime.strptime(context['date'], "%d.%m.%Y").date(),
                discipline_name = context['discipline_name'],
                direction_name = context['direction']
            )
            RDTobj.save()

            return redirect('targets-and-tasks', document_id=doc_obj.id)

    return render(request, "creationTitle.html", context)

def targetsAndTasks(request, document_id):

    context = {
        'document_id': document_id,
        'targets': "",
        'targets_errors': "",
        'tasks': [],
        'tasks_errors': ""
    }

    if(request.method == 'POST'):
        context['targets'] = request.POST['targets']
        if(len(context['targets']) < 10 or len(context['targets']) > 256):
            context['targets_errors'] = "Цели не должны быть меньше 10 и больше 256"

        context['tasks'] = request.POST.getlist('tasks[]')
        if(len(context['tasks']) == 0):
            context['tasks_errors'] = "Должна быть хотя бы 1 задача"

        context['document_id'] = request.POST['document_id']

        if(len(context['targets_errors']) == 0 and len(context['tasks_errors']) == 0):
            rpdDocObj = RpdDocument.objects.get(id=context['document_id'])

            targetsObject = RpdDocumentTargets(
                document_id = rpdDocObj,
                targets = context['targets']
            )
            targetsObject.save()

            for task in context['tasks']:
                taskObject = RpdDocumentTask(
                    document_id = rpdDocObj,
                    task = task
                )
                taskObject.save()

            return redirect('place', document_id=context['document_id'])

    return render(request, "targetsAndTasks.html", context)

def place(request, document_id):

    context = {
        'document_id': document_id,
        'nextDiscipline': "",
        'nextDiscipline_errors': "",
        'prevDiscipline': "",
        'prevDiscipline_errors': ""
    }

    if(request.method == 'POST'):
        context['nextDiscipline'] = request.POST['nextDiscipline']
        if(len(context['nextDiscipline']) < 10 or len(context['nextDiscipline']) > 256):
            context['nextDiscipline_errors'] = "Последущие дисциплины не должны быть меньше 10 и больше 256"

        context['prevDiscipline'] = request.POST['prevDiscipline']
        if(len(context['prevDiscipline']) < 10 or len(context['prevDiscipline']) > 256):
            context['prevDiscipline_errors'] = "Предшествующие дисциплины не должны быть меньше 10 и больше 256"

        context['document_id'] = request.POST['document_id']

        if(len(context['nextDiscipline_errors']) == 0 and len(context['prevDiscipline_errors']) == 0):
            rpdDocObj = RpdDocument.objects.get(id=context['document_id'])

            placeDiscObj = RpdPlaceDiscipline(
                document_id = rpdDocObj,
                disciplines = context['nextDiscipline'],
                type = 1
            )
            placeDiscObj.save()
            placeDiscObj = RpdPlaceDiscipline(
                document_id = rpdDocObj,
                disciplines = context['prevDiscipline'],
                type = 0
            )
            placeDiscObj.save()
            return redirect('/')  

    return render(request, "place.html", context)
