# vim:set ff=unix expandtab ts=4 sw=4:
class ModelList(list):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def plot_data(self):
        #fixme:
        # a lot of potential and actual duplication with Model
        # ideally the head as well as the other lines should be delivered 
        # by the model instance in question
        target_keys=["scalar_func_phot"]
        plot_data = DataFrame([['name', 'nr_sv', 'nr_sym', 'nr_exprs', 'nr_ops', 'depth','nr_vars','nr_parms','part_scheme','s_scale','t_resol']+target_keys])
        for index, model in enumerate(model_list):
            # collect data for plots
            data_list = [model.name]

            nr_state_v = 0
            for sec in model.sections:
                if sec == "state_variables":
                    nr_state_v = model.section_vars('state_variables').nrow
            
            ops = 0
            d = 0
            for i in range(model.rhs.rows):
                for j in range(model.rhs.cols):
                    ops += model.rhs[i,j].count_ops()
                    d = max([d, depth(model.rhs[i,j])])

            
            if model.partitioning_scheme == "fixed": 
                boolean_part_scheme = 0
            else:
                boolean_part_scheme = 1
            scalar_func_phot_dep_set=model.depends_on_keys(target_keys[0]) 

            data_list += [nr_state_v, len(model.syms_dict), len(model.exprs_dict), ops, d,len(model.variables),len(model.parameters),boolean_part_scheme,model.space_scale,model.time_resolution,scalar_func_phot_dep_set]
            plot_data.append_row(data_list)
            
        return(plotdata)
        
