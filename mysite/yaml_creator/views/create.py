from django.http import HttpResponse, HttpResponseRedirect
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme import ComponentScheme
from django.utils import timezone
from django.template import loader
from django.urls import reverse

def create_new_ModelDescriptor(request):
    key='filename'
    if key in request.POST.keys():
        yaml_file_name=request.POST[key]
        return HttpResponseRedirect(reverse("detail",kwargs={'file_name':yaml_file_name}))

