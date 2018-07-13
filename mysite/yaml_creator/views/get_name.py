from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..forms import NameForm
from ..forms import ModelDescriptorForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = NameForm(request.POST)
        form = ModelDescriptorForm(request.POST)
        context={
            'form':form
        }
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            # ...
            # show them once again
            context={'success':form.cleaned_data}
            # or redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
        else:
            # an error occurred
            print('##########################################')
            for name,field in form.fields.items():
                print(name)
                print(field)

            context={
                'form':form
                ,
                'doi_dict':form.fields['doi'].__dict__
                ,
                'error':form.errors
            }


    # if a GET (or any other method) we'll create a blank form
    else:
        initial={'your_name':'http://google.com'}
        #form = NameForm(initial=initial)
        form = ModelDescriptorForm(initial=initial)
        context={'form':form}

    return render(request, 'yaml_creator/get_name.html', context)
