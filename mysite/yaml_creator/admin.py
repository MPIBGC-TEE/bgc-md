from django.contrib import admin
# Register your models here.
from .models import ModelDescriptor,Variable

#admin.site.register(ModelDescriptor)

#class VariableInline(admin.StackedInline):
class VariableInline(admin.TabularInline):
    model = Variable
    extra = 0

class ModelDescriptorAdmin(admin.ModelAdmin):
    fieldsets = [
    (None,              {'fields':['doi']}),
    ('Date Information',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    inlines = [VariableInline]
    list_display = ('filename','pub_date')
    list_filter=['pub_date']
    search_fields = ['filename']

admin.site.register(ModelDescriptor,ModelDescriptorAdmin)
