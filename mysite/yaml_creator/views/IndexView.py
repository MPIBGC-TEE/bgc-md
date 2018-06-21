class IndexView(generic.ListView):
    template_name='yaml_creator/data_base_index.html'
    context_object_name='latest_modeldescriptor_list'
    
    def get_queryset(self):
    	"""Return the last five published ModelDescriptors."""
    	return ModelDescriptor.objects.order_by('-pub_date')[:5]

