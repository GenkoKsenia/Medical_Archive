from typing import Any
from django.http import HttpResponse
from django.views.generic import TemplateView

from medicines.models import Patient

# Create your views here.

#class ShowPatientsView(TemplateView):
#    template_name = "medicines/show_patients.html"

#    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#        context = super().get_context_data(**kwargs)
#        context['patients'] = Patient.objects.all()

#        return context

    