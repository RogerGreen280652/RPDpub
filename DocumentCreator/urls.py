from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create-title', views.creationDocumentTitle, name="create-title"),
    path(r'^targets-and-tasks/(?P<document_id>[0-9]+)/$', views.targetsAndTasks, name="targets-and-tasks"),
    path(r'^place/(?P<document_id>[0-9]+)/$', views.place, name="place"),
    path('download', views.download_file, name="download")
]
