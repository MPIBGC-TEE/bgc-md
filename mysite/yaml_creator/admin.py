#from django.contrib import admin
## Register your models here.
#from .models.ModelDescriptor    import ModelDescriptor
#from .models.AdditionalVariable           import AdditionalVariable
#from .models.StateVector import StateVariable
#from .models.ComponentScheme    import ComponentScheme
#from .models.FluxRepresentation import FluxRepresentation
#
##admin.site.register(ModelDescriptor)
#
##class VariableInline(admin.StackedInline):
#
#
#class ComponentSchemeAdmin(admin.ModelAdmin):
#    model = ComponentScheme 
#    extra = 1
#
#class ComponentSchemeInline(admin.StackedInline):
#    model = ComponentScheme 
#    extra = 1
#
#class StateVariableInline(admin.TabularInline):
#    model = StateVariable
#    extra = 0
#
#
#class AdditionalVariableInline(admin.TabularInline):
#    model = AdditionalVariable
#    extra = 0
#
#class ModelDescriptorAdmin(admin.ModelAdmin):
#    fieldsets = [
#    (None,              {'fields':['doi']}),
#    ('Date Information',{'fields':['pub_date'],'classes':['collapse']}),
#    ]
#    #inlines = [StateVariableInline,AdditionalVariableInline,ComponentSchemeInline]
#    inlines = [AdditionalVariableInline,ComponentSchemeInline]
#    list_display = ('filename','pub_date')
#    list_filter=['pub_date']
#    search_fields = ['filename']
#
#admin.site.register(ModelDescriptor,ModelDescriptorAdmin)
#admin.site.register(ComponentScheme,ComponentSchemeAdmin)
