"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from medicines import views
from rest_framework.routers import DefaultRouter
import medicines
from medicines.api import PatientsViewset, MedicineViewset, DoctorViewset, ReleaseFormViewset, TherapeuticActionViewset
   

router = DefaultRouter()
router.register("patients", PatientsViewset, basename="patients")
router.register("medicines", MedicineViewset, basename="medicines")
router.register("doctors", DoctorViewset, basename="doctors")
router.register("forms", ReleaseFormViewset, basename="releaseForms")
router.register("actions", TherapeuticActionViewset, basename="actions")

urlpatterns = [
    #path('', views.ShowPatientsView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
