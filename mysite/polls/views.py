from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.shortcuts import render,get_object_or_404
from .models import Choice,Question

#class IndexView(generic.ListView):
#    #template_name = 'polls/index.html'
#    context_object_name = 'latest_question_list'
#    def get_queryset(self):
#        """Return the last five puplished questions."""
#        return Question.objects.order_by('-pub_date')[:5]
#
def table(request):
    from bgc_md.ModelList import ModelList
    from bgc_md.reports import  defaults
    d=defaults() 
    source_dir_path=d['paths']['tested_records']    
    ml=ModelList.from_dir_path(src_dir_path)
    target_dir_path=Path('.').joinpath('html')
    targetFileName='table.html'
    rel=ml.create_overview_table(target_dir_path,targetFileName)
    
    return HttpResponse('Test') 

def index(request):
	latest_question_list=Question.objects.order_by('-pub_date')[:5]
	template =loader.get_template('polls/index.html')
	context={
		'latest_question_list':latest_question_list,}
	#output=template.render(context,request)
	#return HttpResponse(output)
	return render(request,'polls/index.html',context)

def detail(request, question_id):
	#try:
	#	question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
	#	raise Http404('Question does not exist.')
	question = get_object_or_404(Question,pk=question_id)
	return render(request,"polls/detail.html",{'question':question})

def results(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    #return HttpResponse("You're looking at the results of question %s." % question_id)
    return render(request,'polls/results.html',{'question':question})

def vote(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice= question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request
            ,'polls/detail.html'
            ,{
                'question':question
                ,'error_message':"You didn't select a Choice." 
            }
        )
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
