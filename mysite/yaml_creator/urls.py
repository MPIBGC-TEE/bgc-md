from django.urls import path
#from . import views
from .views.index import index
from .views.model_overview import model_overview
from .views.create import create_new_ModelDescriptor
from .views.detail import detail
from .views.set_statevector import set_statevector
from .views.set_statevariable_descriptions import set_statevariable_descriptions
from .views.data_base_index import data_base_index

urlpatterns=[
    #path('data_base_index',views.IndexView.as_view(), name='data_base_index'),
    ##path('<str:pk>/detail',views.DetailView.as_view(), name='detail'),
    #path('',index, name='index'),
    path('',data_base_index, name='data_base_index'),
    path('create_new_ModelDescriptor',create_new_ModelDescriptor, name='create_new_ModelDescriptor'),
    path('<str:file_name>/set_statevector/',set_statevector, name='set_statevector'),
    path('<str:file_name>/set_statevariable_descriptions/',set_statevariable_descriptions, name='set_statevariable_descriptions'),
    #path('<str:file_name>/model_overview/',model_overview, name='model_overview'),
    path('<str:file_name>/detail/',detail, name='detail'),
]
