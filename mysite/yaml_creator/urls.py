from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name='index'),
    path('<int:question_id>/',views.detail, name='detail'),
    path('<int:question_id>/results/',views.results, name='results'),
    path('<str:file_name>/change/',views.change, name='change'),
]
