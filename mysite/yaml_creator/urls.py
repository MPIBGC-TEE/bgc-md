from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='index'),
    path('<str:file_name>/model_overview/',views.model_overview, name='model_overview'),
]
