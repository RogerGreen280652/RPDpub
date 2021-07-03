from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('rpd/', include('rpd.urls')),
    path('admin/', admin.site.urls),
]
