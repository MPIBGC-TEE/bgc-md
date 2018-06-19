
from django.http import HttpResponse, HttpResponseRedirect
from yaml_creator.models.SingleFlux import SingleFlux

def set_Fluxes(request,file_name):
    return HttpResponse('set the fluxes here')
