from django.contrib import admin

# Register your models here.
from .models import Question
#from  bgc_md.Model import Model

#admin.site.register(Model)
admin.site.register(Question)
