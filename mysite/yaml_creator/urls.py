from django.urls import path
#from . import views
from .views.index import index
from .views.model_overview import model_overview
from .views.create import create_new_ModelDescriptor
from .views.detail import detail
from .views.data_base_index import data_base_index

urlpatterns=[
    #path('data_base_index',views.IndexView.as_view(), name='data_base_index'),
    ##path('<str:pk>/detail',views.DetailView.as_view(), name='detail'),
    path('<str:modeldescriptor_filename>/detail/',detail, name='detail'),
    #path('',index, name='index'),
    path('',data_base_index, name='data_base_index'),
    path('create_new_ModelDescriptor',create_new_ModelDescriptor, name='create_new_ModelDescriptor'),
    path('<str:file_name>/model_overview/',model_overview, name='model_overview'),
]
