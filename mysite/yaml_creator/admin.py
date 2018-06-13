from django.contrib import admin
# Register your models here.
from .models import ModelDescriptor,Variable,ComponentScheme,FluxRepresentation,FluxDict

#admin.site.register(ModelDescriptor)

#class VariableInline(admin.StackedInline):
class CompartmentSchemeInline(admin.TabularInline):
    model = ComponentScheme 
    extra = 1

class VariableInline(admin.TabularInline):
    model = Variable
    extra = 0

class ModelDescriptorAdmin(admin.ModelAdmin):
    fieldsets = [
    (None,              {'fields':['doi']}),
    ('Date Information',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    #inlines = [VariableInline,CompartmentSchemeInline]
    inlines = [CompartmentSchemeInline]
    list_display = ('filename','pub_date')
    list_filter=['pub_date']
    search_fields = ['filename']

admin.site.register(ModelDescriptor,ModelDescriptorAdmin)
