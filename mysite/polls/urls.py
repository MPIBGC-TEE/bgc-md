from django.urls import path

from . import views
app_name ='polls'
urlpatterns = [
        # ex:/polls/
        path('', views.index, name='index'),
        #path('', views.IndexView.as_view(), name='index'),
		
    # ex:/polls/table
		path('table/',views.table,name='table'),


        # ex:/polls/5
        path('<int:question_id>/',views.detail,name='detail'),

		# ex:/polls/5/results/
		path('<int:question_id>/results/',views.results,name='results'),

		# ex:/polls/5/results/
		path('<int:question_id>/vote/',views.vote,name='vote'),

]
