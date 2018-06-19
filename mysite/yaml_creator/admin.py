from django.contrib import admin
# Register your models here.
from .models.ModelDescriptor    import ModelDescriptor
from .models.Variable           import Variable
from .models.ComponentScheme    import ComponentScheme
from .models.FluxRepresentation import FluxRepresentation

#admin.site.register(ModelDescriptor)

#class VariableInline(admin.StackedInline):


class ComponentSchemeAdmin(admin.ModelAdmin):
    model = ComponentScheme 
    extra = 1

class ComponentSchemeInline(admin.StackedInline):
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
    inlines = [VariableInline,ComponentSchemeInline]
    #inlines = [ComponentSchemeInline]
    list_display = ('filename','pub_date')
    list_filter=['pub_date']
    search_fields = ['filename']

admin.site.register(ModelDescriptor,ModelDescriptorAdmin)
admin.site.register(ComponentScheme,ComponentSchemeAdmin)
