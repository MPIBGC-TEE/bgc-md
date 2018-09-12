from django.views.i18n import JavaScriptCatalog
from django.urls import path
#from . import views
#from .views.index import index
#from .views.model_overview import model_overview
#from .views.create import create_new_ModelDescriptor
#from .views.set_statevector import set_statevector
#from .views.set_Matrices import set_Matrices
#from .views.set_Fluxes import set_Fluxes
#from .views.set_statevariable_descriptions import set_statevariable_descriptions
#from .views.set_FluxRepresentation import set_FluxRepresentation
from .views.detail import detail
from .views.data_base_index import data_base_index
#from .views.get_name import get_name

urlpatterns=[
    path('jsi18n/yaml_creator/',JavaScriptCatalog.as_view(packages=[]),name='javascript-catalog'), # for admin javascript
    path('',data_base_index, name='data_base_index'),
    path('<str:file_name>/detail/',detail, name='detail'),
    #path('data_base_index',views.IndexView.as_view(), name='data_base_index'),
    ##path('<str:pk>/detail',views.DetailView.as_view(), name='detail'),
    #path('',index, name='index'),
    #path('create_new_ModelDescriptor',create_new_ModelDescriptor, name='create_new_ModelDescriptor'),
    #path('<str:file_name>/set_statevector/',set_statevector, name='set_statevector'),
    #path('<str:file_name>/set_statevariable_descriptions/',set_statevariable_descriptions, name='set_statevariable_descriptions'),
    #path('<str:file_name>/set_FluxRepresentation/',set_FluxRepresentation, name='set_FluxRepresentation'),
    #path('<str:file_name>/set_Fluxes/',set_Fluxes, name='set_Fluxes'),
    #path('<str:file_name>/set_Matrices/',set_Matrices, name='set_Matrices'),
    #path('<str:file_name>/model_overview/',model_overview, name='model_overview'),
    #path('get_name',get_name, name='get_name'),
]
