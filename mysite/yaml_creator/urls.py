from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='index'),
    #path('data_base_index',views.data_base_index, name='data_base_index'),
    path('data_base_index',views.IndexView.as_view(), name='data_base_index'),
    path('<str:modeldescriptor_filename>/detail/',views.detail, name='detail'),
    #path('<str:pk>/detail',views.DetailView.as_view(), name='detail'),
    path('<str:file_name>/model_overview/',views.model_overview, name='model_overview'),
]
