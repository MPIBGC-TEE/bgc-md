# vim:set ff=unix expandtab ts=4 sw=4:
import logging
import inspect
import numpy as np
import multiprocessing
import yaml
from pathlib import Path
import subprocess
from os.path import relpath, dirname
import os
import getopt, sys
from string import Template
from sympy import sympify, solve, Symbol, limit, oo, ceiling, simplify, Matrix
from sympy.core import Atom
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import argparse
from bgc_md.DataFrame import DataFrame
from bgc_md.ReportInfraStructure import ReportElementList, Header, Math, Meta, Text, Citation, Table, TableRow, Newline,EmptyLine,MatplotlibFigure, Link, LinkedSubPage, exprs_to_element, PlotlyFigure

from .Model import Model, check_parameter_set_complete
from .ModelList import ModelList
import bgc_md.bibtexc as bibtexc
from .helpers import py2tex_silent, key_from_dict_by_value
from bgc_md.plot_helpers import add_xhist_data_to_scatter
from bgc_md.gv import indexcolors, filled_markers
import bgc_md.gv as gv
from .Exceptions import ModelInitializationException
from CompartmentalSystems.bins.TsTpMassFieldsPerPoolPerTimeStep import TsTpMassFieldsPerPoolPerTimeStep
from CompartmentalSystems.bins.TimeStepIterator import TimeStepIterator
#def common_parser:
#    parser= argparse.ArgumentParser(add_help=False)
#    parser.add_argument(
#        '-t'
#        ,'--target_dir'
#        ,type=str
#        ,default='.'
#        ,help="where to generate the html files" 
#    )
#    return parser
common_parser= argparse.ArgumentParser(add_help=False)
common_parser.add_argument(
    '-t'
    ,'--target_dir'
    ,type=str
    ,default='.'
    ,help="where to generate the html files" 
)
default_html_filename='index.html'

def defaults():
    this=Path(__file__).parents[0] #the package dir
    tested_record_path=this.joinpath('data','tested_records')
    # fixme mm 
    # I would like to get rid of the Subdirectories 
    # and rather put the information if something is a soil or 
    # vegetation model in the yaml file only but at the moment 
    # someone might still use the distinct directories.
    dataPath=this.joinpath("data") 
    soilModelPath=dataPath.joinpath("SoilModels")
    vegModelPath =dataPath.joinpath("VegetationModels") 
    
    path_dict={
            "veg":vegModelPath
            ,"soil":soilModelPath
            ,"tested_records":tested_record_path
            ,'data':dataPath
            ,"report_templates":this.joinpath("report_templates")
            ,"static_report_templates":this.joinpath("static_report_templates")
            ,"new_models_path":this.parent.joinpath("prototypes","ModelsAsScriptsWithSpecialVarNames","models") 
    }
    
    dir_dict={key:value.as_posix() for key,value in path_dict.items()}
    msg_dict={key:"generating %s model website to" % key for key in path_dict.keys()}
    return {
         "dirs":dir_dict
        ,"paths":path_dict
        ,"msgs":msg_dict
        ,"html_filename":'index.html'
        }

#import mpld3 # interesting functionality for interactive web figures

#def generate_model_run_report():
#    parser = argparse.ArgumentParser(parents=[common_parser])
#    parser.description="Create markdown and html reports of a singel yaml file.\\n"
#    parser.add_argument('path', default=None, help="The path to the yaml file containing the description of the record." )
#    parser.epilog= "Example: %s Henin1945Annalesagronomiques.yaml-t SoilModels/html" % parser.prog
#
#    com=parser.parse_args()
#    print("Creating report from " + com.path + " to " + com.target_dir)
#    create_single_report(Path(com.path), Path(com.target_dir))
#    sys.exit(0)
#


#def generate_model_run_reports():
#    parser = argparse.ArgumentParser(parents=[common_parser])
#    parser.add_argument(
#        '-s'
#        ,'--src_dir'
#        ,type=str
#        ,help="create the model website from a directory  <src_dir> containing the yaml files"
#        ,default=defaults()['dirs']['tested_records']
#    )
#    parser.description="Create model database websites."
#
#    com = parser.parse_args()
#    generate_html_dir(com.src_dir,com.target_dir)
#
#
## fixme mm 14.5.2018
## deprecate! 
#def report_from_model(model):
#    #rel = model.get_meta_data_report()
#    #rel = Meta(model.long_name, model.name, model.version)
#    rel=ReportElementList()
#    rel+= Header("General Overview", 1)
#
#    reservoir_model = model.reservoir_model
#    if reservoir_model:
#        plt.rc('text', usetex=True)
#        plt.rc('font', family='serif')
#        rel += MatplotlibFigure(reservoir_model.figure(logo=True), "Logo", show_label=False, transparent=True)
#        #logofig = reservoir_model.figure(logo=True)
#        #logofig.savefig('ICBM_logo.svg', transparent=True)
#        #plt.show(logofig)
#        #print('Logo printed')
#
#    rel+= Text(r"This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by $curator (Orcid ID: $Oid) on $entryDate, and was last modified on $modDate." + "\n",
#            curator=model.entryAuthor,
#            entryDate=model.entry_creation_date,
#            modDate=model.last_modification_date,
#            Oid=model.entryAuthor_orc_id,
#             )
#
#    if model.model_type == "vegetation_model": modType = "carbon allocation"
#    if model.model_type == "soil_model": modType = "soil organic matter decomposition"
#
#    if model.approach:
#            article = "a"
#            if model.approach[0] in "aeiou":
#                article = "an"
#            modApproach = " with " + article + " " + model.approach + " approach."
#    else:
#                modApproach = "."
#
#    rel += Header("About the model", 2)
#    rel += Text(r"The model depicted in this document considers $modType$modApproach It was originally described by ", 
#                modType=modType, modApproach=modApproach)
#    rel += Citation(model.bibtex_entry, parentheses=False) + Text(".  \n")
#
#    # fixme: further references
#    # include further references
#    if model.further_references:
#        rel += Header("Further references" , 3)
#        for ref_dict in model.further_references:
#            rel += Citation(ref_dict['bibtex_entry'], parentheses=False)
#            if 'desc' in ref_dict.keys():
#                rel += Text(": $desc", desc=ref_dict['desc'])
#            rel += Text("\n")
#
#    # include the abstract
#    if hasattr(model,"abstract"):
#        rel += Header("Abstract", 3)
#        rel += Text("$abstract", abstract=model.abstract+"\n")
#
#    # include keywords
#    if model.keywords:
#        rel += Header("Keywords", 3)
#        rel += Text("$k\n", k = (", ").join(model.keywords))
#
#    # include principles
#    if model.principles:
#        rel += Header("Principles", 3)
#        rel += Text("$k\n", k = (", ").join(model.principles))
#
#    # include spaceScale:
#    if model.spaceScale:
#        rel += Header("Space Scale", 3)
#    
#        space_scale = model.spaceScale
#        if type(space_scale) == type(""):
#            space_scale = [space_scale]
#        rel += Text("$k\n", k = (", ").join(space_scale))
#
#    # include information on available parameter sets
#    if model.parameter_sets:
#        desc_exists = False
#        colname_list = [Text("Abbreviation")]
#        format_list = ["l"]
#        for par_set in model.parameter_sets:
#            sources_exist = False
#            desc_exists = False
#            if 'bibtex_entry' in par_set.keys() and par_set['bibtex_entry']: sources_exist = True
#            if 'desc' in par_set.keys() and par_set['desc']: desc_exists = True
#
#        if desc_exists:
#            colname_list.append(Text("Description"))
#            format_list.append("l")
#        if sources_exist:
#            colname_list.append(Text("Source"))
#            format_list.append("l")
#    
#        # show this section only if additional information to the parameter sets is given
#        if len(colname_list)>1:
#            rel += Header("Available parameter values", 3)
#            headers_row = TableRow(colname_list)
#            T = Table(" Information on given parameter sets", headers_row, format_list)
#            for par_set in model.parameter_sets:
#                l = [Text(par_set['table_head'])]
#                if desc_exists: 
#                    if par_set['desc']:
#                        l.append(Text(par_set['desc']))
#                    else:
#                        l.append(Text(" "))
#
#                if sources_exist: 
#                    if par_set['bibtex_entry']:
#                        l.append(Citation(par_set['bibtex_entry'], parentheses=False))
#                    else:
#                        l.append(Text(" "))
#
#                tr = TableRow(l)
#                T.add_row(tr)    
#            rel += T
#
#    # include information on available initial values sets
#    if model.initial_values:
#        desc_exists = False
#        colname_list = [Text("Abbreviation")]
#        format_list = ["l"]
#        for par_set in model.initial_values:
#            if 'bibtex_entry' in par_set.keys() and par_set['bibtex_entry']: sources_exist = True
#            if 'desc' in par_set.keys() and par_set['desc']: desc_exists = True
#
#        if desc_exists:
#            colname_list.append(Text("Description"))
#            format_list.append("l")
#        if sources_exist:
#            colname_list.append(Text("Source"))
#            format_list.append("l")
#    
#        # show this section only if additional information to the initial values sets is given
#        if len(colname_list)>1:
#            rel += Header("Available initial values", 3)
#            headers_row = TableRow(colname_list)
#            T = Table(" Information on given sets of initial values", headers_row, format_list)
#            for par_set in model.initial_values:
#                l = [Text(par_set['table_head'])]
#                if desc_exists: 
#                    if par_set['desc']:
#                        l.append(Text(par_set['desc']))
#                    else:
#                        l.append(Text(" "))
#
#                if sources_exist: 
#                    if par_set['bibtex_entry']:
#                        l.append(Citation(par_set['bibtex_entry'], parentheses=False))
#                    else:
#                        l.append(Text(" "))
#
#                tr = TableRow(l)
#                T.add_row(tr)    
#            rel += T
#
#    # show the secions of the model data
#    #for section_name in model.sections:
#    for section_name in model.model_subsections:
#        if section_name == 'state_variables':
#            rel += Header(model.section_titles[section_name], 1)
#            rel += Text("The following table contains the available information regarding this section:")
#            rel += model.state_variables_Table()
#        elif section_name == 'additional_variables':
#            rel += Header(model.section_titles[section_name], 1)
#            rel += Text("The following table contains the available information regarding this section:")
#            rel += model.additional_variables_Table()
#        elif section_name == 'allocation_coefficients':
#            rel += Header(model.section_titles[section_name], 1)
#            rel += Text("The following table contains the available information regarding this section:")
#            rel += model.allocation_coefficients_Table()
#        elif section_name == 'components':
#            rel += Header(model.section_titles[section_name], 1)
#            rel += Text("The following table contains the available information regarding this section:")
#            rel += model.components_Table()
#        elif section_name == 'parameter_sets':
#            # parameter_sets are treated completely differently
#            pass
#        else:
#            # custom section to be included in the report
#            rel += Header(model.section_titles[section_name], 1)
#            rel += Text("The following table contains the available information regarding this section:")
#            rel += model.variables_Table_from_section(section_name, parameter_values = True)
#
#    # include pool model plot
#    if reservoir_model:
#        inputs = reservoir_model.input_fluxes
#        outputs = reservoir_model.output_fluxes
#        internal_fluxes = reservoir_model.internal_fluxes
##        inputs, outputs, internal_fluxes = model.fluxes
#
#        rel += Text("\n")
#        rel += Header("Pool model representation", 2)
#
#        header = [Text("Pool model"), Text("Fluxes")]
#        header_row = TableRow(header)
#        T = Text("<table>")
#        T += Text("<thead>")
#        T += Text("<tr><th></th><th>Flux description</th></tr>")
#        T += Text("</thead><tbody>")
#        T += Text("<tr>")
#        T += Text("<td align=center, style='vertical-align: middle'>")  
#        fig = reservoir_model.figure(figure_size=(7,7))
#        fig_rel = MatplotlibFigure(fig, "Figure 1", "Pool model representation")
#        #T += fig_rel.pandoc_markdown()
#        T += fig_rel
#        T += Text("</td><td align=left style='vertical-align: middle'>")
#        
#        # write the fluxes to the table
#        legend = ReportElementList([])
#
#        # input fluxes
#        if len(inputs) > 0:
#            legend += Header("Input fluxes", 4)
#            for pool, flux in inputs.items():
#                legend += Math("$v: $f", v=py2tex_silent(model.state_variables[pool]), f=flux)
#                legend += Newline()
#        
#        # output fluxes
#        if len(outputs) > 0:
#            legend += Text("\n")
#            legend += Header("Output fluxes", 4)
#            for pool, flux in outputs.items():
#                legend += Math("$v: $f", v=py2tex_silent(model.state_variables[pool]), f=flux)
#                legend += Newline()
#        
#        # internal fluxes
#        if len(internal_fluxes) > 0:
#            legend += Text("\n")
#            legend += Header("Internal fluxes", 4)
#            if_sorted = [((i,j), f) for (i,j), f in internal_fluxes.items()]
#            if_sorted = sorted(if_sorted, key=lambda el: (el[0][0],el[0][1]))
#            for (pfrom, pto), flux in if_sorted:
#                legend += Math("$pf \\rightarrow $pt: $f", pf=py2tex_silent(model.state_variables[pfrom]), pt=py2tex_silent(model.state_variables[pto]), f=flux)
#                legend += Newline()
#        
#        T += legend
#        T += Text("</td></tr>")
#        T += Text("</tbody></table>")
#
#
#        rel += T
#
#
#    # include RHS and jacobian
#    rel += Header("The right hand side of the ODE", 2)
#    rel += Math("$eq", eq=model.rhs)
#    rel += Text("\n")
#    rel += Header("The Jacobian (derivative of the ODE w.r.t. state variables)", 2)
#    rel += Math("$J", J=model.jacobian())
#
#    rel += Text("\n")
# 
#    #fixme: suggested steady states  
#    # check suggested steady states
#
##    rhs = model.rhs
##    sug_ss = model.complete_dict['suggested_steady_states']
##    sug_ss = {key: sympify(val, locals=model.symbols_by_type) for key, val in sug_ss[0].items()}
##    sug_ss.update({'alpha': 1, 'beta': 0.5, 'Phi_i': 0, 'Phi_o': 0, 'Phi_up': 0, 'Phi_l': 0, 'A': 5.2, 'r': 2, 's': 1, 'i':1})
##    ss = rhs.subs(sug_ss)
##    for i in range(len(ss)):
##        ss[i] = simplify(ss[i])
##        print(ss[i])
#
#    # try to calculate the steady states for ten seconds
#    # after ten seconds stop it
#    q = multiprocessing.Queue()
#    def calc_steady_states(q):
##        rhs = Matrix(list(model.rhs)[1:])
##        sv = Matrix(list(model.state_vector['expr'])[1:])
#
#        ss = solve(model.rhs, model.state_vector['expr'], dict=True)
#
##        ss = solve(rhs, sv, dict=True)
##        srhs = rhs.subs(ss[0])
##        for i in range(len(srhs)):
##            print(simplify(srhs[i]))
#        q.put(ss)
#
#    p = multiprocessing.Process(target=calc_steady_states, args=(q,))
#    p.start()
#    p.join(10)
#    if p.is_alive():
#        p.terminate()
#        p.join()
#        steady_states = []
#    else:
#        steady_states = q.get()
#
##    rhs = model.rhs
##    srhs = rhs.subs(steady_states[0])
##    for i in range(len(srhs)):
##        print(simplify(srhs[i]))
#    
#
#    # check if steady states have all state variables
##    formal_steady_states = []
##    for ss in steady_states:
##        if len(ss) == len(model.state_vector['expr']):
##            formal_steady_states.append(simplify(ss))
#
#    formal_steady_states = steady_states
#    if formal_steady_states:
#        rel += Header("Steady state formulas", 2)
#        for ss in formal_steady_states:
#            for sv_symbol in model.state_vector['expr']:
#                if sv_symbol in ss.keys():
#                    ss[sv_symbol] = simplify(ss[sv_symbol])
#                else:
#                    ss[sv_symbol] = sv_symbol
#
#                rel += Math("$name = $value", name=sv_symbol, value=ss[sv_symbol]) + Newline()
#            rel += Newline()
#
#    # include parameter set information: steady states, eigenvalues, damping ratios
##    complete_parameter_sets = [par_set for par_set in model.parameter_sets if check_parameter_set_complete(par_set, model.state_vector, model.time_symbol, model.state_vector_derivative)]
#    
#    if model.time_symbol:
#        time_symbol = model.time_symbol['symbol']
#    else:
#        time_symbol = None
#
#    complete_parameter_sets = model.parameter_sets
#    if formal_steady_states and complete_parameter_sets:
#        rel += Text("\n")
#        rel += Header("Steady states (potentially incomplete), according jacobian eigenvalues, damping ratio", 2)
#        for par_set in complete_parameter_sets:
#            header_str = "Parameter set: " + par_set['table_head']
#            rel += Header(header_str, 3)
#
#            rhs = model.rhs
#            steady_states = solve(rhs.subs(par_set['values']), model.state_vector['expr'], dict=True)
#            #steady_states = solve(rhs, model.state_vector['expr'], dict=True)
#            for ss in steady_states:
#                # check if steady state calculation could solve for all state variables
##                if len(ss) == len(model.state_vector['expr']):
#                    ss_list = []
#                    for sv_symbol in model.state_vector['expr']:
#                        if sv_symbol in ss.keys():
#                            ss_expr = ss[sv_symbol]
#                        else:
#                            ss_expr = sv_symbol
#
#                        if time_symbol in ss_expr.free_symbols:
#                            # take limit of time to infinity if steady state still depends on time
#                            ss_expr = limit(ss_expr, time_symbol, oo)
#                            rel += Text("\nTaken limit ") + Math("$sv($t)", sv=sv_symbol, t=time_symbol)
#                            rel += Text(" for ") + Math("$t", t=time_symbol)
#                            rel += Text(" to infinity.\n\n")
#    
#                        sv_name = key_from_dict_by_value(model.symbols_by_type, sv_symbol)
#    
#                        ss_list.append({'name': sv_name, 'symbol': sv_symbol, 'value': ss_expr})
#                        
#                    for i in range(len(ss_list)):
#                        if ss_list[i]['value'].free_symbols == set():
#                            if ss_list[i]['value'] < 0:
#                                rel += Text('<font color="FF0000">')
#                                rel += Math(ss_list[i]['name'] + ": $v", v = round(ss_list[i]['value'], 3))
#                                rel += Text('</font>')
#                            else:
#                                rel += Math(ss_list[i]['name'] + ": $v", v = round(ss_list[i]['value'], 3))
#                        else:
#                                rel += Math(ss_list[i]['name'] + ": $v", v = ss_list[i]['value'])
#    
#                        if i< len(ss_list)-1:
#                            rel += Text(", ")
#    
#                    rel += Newline()*2
#    
#                    dic = par_set['values']
#                    for i in range(len(ss_list)):
#                        dic[ss_list[i]['name']] = ss_list[i]['value']
#    
#                    jacobian = model.jacobian().subs(dic)
#                    if jacobian.free_symbols == set():
#                        evs = [complex(v) for v in jacobian.eigenvals().keys()]
#                    else:
#                        evs = [v for v in jacobian.eigenvals().keys()]
#
#                    for i in range(len(evs)):
#                        ev = evs[i]
#                        
#                        if jacobian.free_symbols == set():
#                            if ev.imag == 0:
#                                ev = ev.real
#    
#                            lamda_i = Symbol('lamda_'+ str(i+1))
#                            rel += Math("$s: $v", s = lamda_i, v = "{:.3f}".format(ev)) + Newline()
#        
#                            if ev.imag != 0:                        
#                                rho = -ev.real/np.sqrt(ev.real**2+ev.imag**2)
#                                rel += Math("$s: $v", s = Symbol("rho_"+ str(i+1)), v = "{:-3f}".format(rho)) + Newline()
#                        else:
#                            lamda_i = Symbol('lamda_'+ str(i+1))
#                            rel += Math("$s: $v", s = lamda_i, v = ev.evalf(4)) + Newline()
#        
#                            #if ev.imag != 0:                        
#                            #    rho = -ev.real/np.sqrt(ev.real**2+ev.imag**2)
#                            #    rel += Math("$s: $v", s = Symbol("rho_"+ str(i+1)), v = "{:-3f}".format(rho)) + Newline()
#    
#        
#                    rel += Text("\n")*2
#                        
#
#    #fixme
##    steady_states=solve(model.rhs, model.state_vector['expr'], dict=True)
#
#    # include model simulations
#    if reservoir_model and model.model_runs:
#        rel += Header("Model simulations", 2)
#
#
#        model_runs = model.model_runs
#        for i, mr in enumerate(model_runs):
#            comb = model.model_run_combinations[i]
#            par_set = comb['par_set']['values']
#
#            run_data_str_basis = "Initial values: " + comb['IV']['table_head']
#            run_data_str_basis += ", Parameter set: " + comb['par_set']['table_head']
#
#            # plot solutions
#            fig = plt.figure(figsize=(7,3*len(model.state_vector["expr"])), tight_layout=True)          
##            time_unit = model.df.get_by_cond('unit', 'name', model.time_symbol['name'])
##            units = [model.df.get_by_cond('unit', 'name', sv.name) for sv in model.state_vector['expr']]
##            mr.plot_sols(fig, time_unit, units)
## fixme:mm-30.01.2018            mr.plot_sols(fig)
#
#            label = "Model run " + str(i+1) + " - solutions"
#            run_data_str = run_data_str_basis + ", Time step: " + str(comb['run_time']['step_size'])
#            rel += MatplotlibFigure(fig, label, run_data_str)
#            
#            # plot phase planes
#            fig = plt.figure(figsize=(3*len(model.state_vector["expr"]),7), tight_layout=True)
##            mr.plot_phase_planes(fig, units)
#            mr.plot_phase_planes(fig)
#
#            label = "Model run " + str(i+1) + " - phase planes"
#            run_data_str = run_data_str_basis + ", Start: " + str(comb['run_time']['start'])
#            run_data_str += ", End: " + str(comb['run_time']['end'])
#            run_data_str += ", Time step: " + str(comb['run_time']['step_size'])
#            rel += MatplotlibFigure(fig, label, run_data_str)
#
#            # plot external input 
##            fig = plt.figure(figsize=(7,3), tight_layout=True)
##            label = "Model run " + str(i+1) + " - external input"
##            mr.plot_external_input_fluxes(fig)
##            rel += MatplotlibFigure(fig, label, run_data_str)
#
#            # plot system-age distributions
#            fig = plt.figure(figsize=(10,15), tight_layout=True)
##            fig = plt.figure(figsize=(6,6), tight_layout=True)
#            tsi=TimeStepIterator.from_ode_reservoir_model_run(mr)
#            
#            age_dist_hist=TsTpMassFieldsPerPoolPerTimeStep.from_time_step_iterator(tsi)
#            print("Calculation done, creating plot.")
#            age_dist_hist.matrix_plot3d("plot_system_age_distributions_with_bins", fig, title="System age distribution", mr=mr)
#            print("Plot created.")
#            
#            label = "Model run " + str(i+1) + " - system-age-distributions"
#            
#            rel += MatplotlibFigure(fig, label, run_data_str_basis)
#            #fig.show()
#            #input()
#
#    # include references
#    rel += Text("\n")
#    rel += Header("References", 1)
#    return(rel)
#    
#######################################################################

def input_output_path(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise(Exception("The input path " + input_path + " does not exist."))

    if not output_path.exists():
        output_path.mkdir()

    return input_path, output_path


def produce_model_report_markdown(yaml_file_name_list, md_file_name_list):
    if type(yaml_file_name_list) == type(""):
        yaml_file_name_list = [yaml_file_name_list]
    if type(md_file_name_list) == type(""):
        md_file_name_list = [md_file_name_list]

    if len(yaml_file_name_list) != len(md_file_name_list):
        raise(Exception("Length if input file list does not equal length of output file list."))

    for index, yaml_file_name in enumerate(yaml_file_name_list):
        md_file_name = md_file_name_list[index]
        with open(yaml_file_name) as f:
            yaml_str = f.read()

        rel, references = report_from_yaml_str(yaml_str)

        trunk = Path(md_file_name).stem
        bibtex_file_name = os.path.join(dirname(md_file_name), trunk + ".bibtex")
        bibtexc.entry_list_to_path(bibtex_file_name, references, format_str="BibTeX")
        rel.write_pandoc_markdown(md_file_name)   
 

def report_from_yaml_str(yaml_str):
    complete_dict = yaml.load(yaml_str)
    model = Model(complete_dict)
    return report_from_model(model)
    
 
def produce_model_report_markdown_directory(input_dir, output_dir):
    # fixme mm:
    # this method is not called from anywhere at the moment.
    
    input_path, output_path = input_output_path(input_dir, output_dir)

    yaml_file_list = [f for f in input_path.iterdir() if f.suffix == ".yaml"]
    md_file_list = [output_path / (f.stem + ".md") for f in yaml_file_list]

    yaml_file_name_list = [str(f) for f in yaml_file_list]
    md_file_name_list = [str(f) for f in md_file_list]
    produce_model_report_markdown(yaml_file_name_list, md_file_name_list)


#def create_html_from_pandoc_md(md_file_name_list, html_file_name_list, csl_file_name = "", css_file_name = "", slide_show = False):
#    if type(md_file_name_list) == type(""):
#        md_file_name_list = [md_file_name_list]
#    if type(html_file_name_list) == type(""):
#        html_file_name_list = [html_file_name_list]
#
#    if len(md_file_name_list) != len(html_file_name_list):
#        raise(Exception("Length if input file list does not equal length of output file list."))
#
#    for index, md_file_name in enumerate(md_file_name_list):
#        html_file_name = html_file_name_list[index]
#        trunk = Path(md_file_name).stem
#        bibtex_file_name = os.path.join(dirname(md_file_name), trunk + ".bibtex")
#
#        cmd = ["pandoc"]
#        cmd += [md_file_name,"-s","--mathjax", "-o", html_file_name]        
#        cmd += ["--filter=pandoc-citeproc", "--bibliography="+bibtex_file_name]
#        if css_file_name: 
#            rel_css_folder = relpath(dirname(css_file_name), dirname(html_file_name))
#            rel_css_file_name = os.path.join(rel_css_folder, os.path.split(css_file_name)[1])
#            cmd += ["-c", rel_css_file_name]
#
#        if csl_file_name: cmd += ["--csl", csl_file_name]
#        if slide_show: cmd += ["-t", "slidy"]
#            # "slidy" can be changed to: "s5", "slideous", "dzslides", or "revealjs". 
#            # For generating a beamer, we'll need: (["pandoc","-t","beamer","--mathjax",md_file,"-o","pdf"]), 
#            # where md_file should have TeX math embedded.
#
#        try:
#            subprocess.check_call(["rm","-rf", html_file_name])
#            subprocess.check_output(cmd)
#        except subprocess.CalledProcessError as e:
#            out=e.output
#            print(out)
#

#def create_html_from_pandoc_md_directory(input_dir, output_dir, csl_file_name = "", css_file_name = "", slide_show = False):
#    input_path, output_path = input_output_path(input_dir, output_dir)
#
#    md_file_list = [f for f in input_path.iterdir() if f.suffix == ".md"]
#    html_file_list = [output_path / (f.stem + ".html") for f in md_file_list]
#
#    md_file_name_list = [str(f) for f in md_file_list]
#    html_file_name_list = [str(f) for f in html_file_list]
#    create_html_from_pandoc_md(md_file_name_list, html_file_name_list, csl_file_name=csl_file_name, css_file_name=css_file_name, slide_show=slide_show)




#def create_overview_report(model_list, target_dir_path=Path('.'),output_file_name='list_report.html'):
#        # get  mapping from the modelnames to the symbols to keep them consistent in all the plots
#        symbol_list=gv.symbol_list
#        if len(model_list) < len(symbol_list):
#            mapping={(model_list[ind]).name:symbol_list[ind] for ind in range(len(model_list))}
#        else:
#            raise(Exception("The number of unique plot symbols is smaller than the number of models in the list. Change the way the symbol list is created."))
#
#        output_path = target_dir_path.joinpath(output_file_name)
#        if not target_dir_path.exists():
#            target_dir_path.mkdir()
#    
#        rel = Header('Overview of the models', 1)
#        
#        
#        
##        #fixme mm:
##        # the fact thet the following mehtod has 
##        # a target_dir_path argument
##        # points to it having side effects, which are to be avoided
#        rel += model_list.create_overview_table(target_dir_path)
#    
#        rel += Header("Figures", 1)
###########################################################################
#
##        fig = plt.figure(figsize=(15,10), tight_layout=True)
##        # Attention: The help of figure.add_subplot is wrong!
##        nr_col = 3
##        nr_row = 2
##        ax = fig.add_subplot(nr_row, nr_col, 1)
##        ax = model_list.create_histogram(ax,x='nr_state_v',x_label='No. state variables',y_label='No. models')
##    
##        # parameters and models
##        ax = fig.add_subplot(nr_row, nr_col, 2)
##        ax = model_list.create_histogram(ax,x='nr_parameters',x_label='No. parameters',y_label='No. models')
##    
##        # variables and models
##        ax = fig.add_subplot(nr_row, nr_col, 3)
##        ax = model_list.create_histogram(ax,x='nr_variables',x_label='No. variables',y_label='No. models')
##        rel += MatplotlibFigure(fig,'Figure 1',"Histograms,  variables") 
##
##
##
############################################################################
##        # scatter plots
##        fig = plt.figure(figsize=(10,10))
##        ax = fig.add_subplot(1,1,1)
##        ax= model_list.create_scatter_plot(
##            ax
##            ,x='nr_variables'
##            ,y='nr_parameters'
##            ,x_label='No. variables'
##            ,y_label='No. parameters'
##            ,model_symbol_mapping=mapping
##        )
##            
##        rel += MatplotlibFigure(fig,"Figure 2","No. variables & parameters" )
##
############################################################################
##        fig = plt.figure(figsize=(10,10))
##        ax = fig.add_subplot(1,1,1)
##        ax = model_list.create_scatter_plot(
##            ax
##            ,x='nr_variables'
##            ,y='nr_ops'
##            ,x_label='No. variables'
##            ,y_label='No. operations to calculate rhs'
##            ,model_symbol_mapping=mapping
##        )
##            
##        rel += MatplotlibFigure(fig,"Figure 3","No. variables & operations" )
##     
############################################################################
##        fig = plt.figure(figsize=(10,10))
##        ax = fig.add_subplot(1,1,1)
##        ax = model_list.create_scatter_plot(
##            ax
##            ,x='nr_variables'
##            ,y='max_depth'
##            ,x_label='No. variables'
##            ,y_label='Cascading depth of operations\n to calculate the rhs'
##            ,model_symbol_mapping=mapping
##        )
##            
##        rel += MatplotlibFigure(fig,"Figure 4","No. variables & cascading depth of operations" )
##        
############################################################################
##        fig = plt.figure(figsize=(10,10))
##        ax = fig.add_subplot(1,1,1)
##        ax = model_list.create_scatter_plot(
##            ax
##            ,x='nr_ops'
##            ,y='max_depth'
##            ,x_label='No. operations to calculate the rhs'
##            ,y_label='Cascading depth of operations\n to calculate the rhs'
##            ,model_symbol_mapping=mapping
##        )
##            
##        rel += MatplotlibFigure(fig,"Figure 5","No. variables & cascading depth of operations" )
##
###########################################################################
##        model_list = ModelList(
##            m for m in model_list 
##            if m.partitioning_scheme
##        )
##        fig = plt.figure(figsize=(6,len(model_list)*0.53))
##        fig.subplots_adjust(bottom=0.2, top=0.8, left=0.2)
##        ax = fig.add_subplot(1,1,1)
##        ax.set_xlim(0,3)
##        ax = model_list.create_scatter_plot_plus_rand(
##            ax
##            ,x='partitioning_scheme_nr'
##            ,y='nr_ops'
##            ,x_label='Partitioning scheme'
##            ,y_label='No. operations to calculate the rhs'
##            ,model_symbol_mapping=mapping
##        )
##        ax.set_xticks([1,2])
##        ax.set_xticklabels(['fixed','dynamic'], fontsize = "14")
##        
##        rel += MatplotlibFigure(fig,"Figure 6","Type of carbon partitioning scheme among pools and No.  operations" )
##
###########################################################################
##        model_list = ModelList(
##            m for m in model_list 
##            if m.partitioning_scheme and m.yaml_file_provides("claimedDynamicPart")
##        )
##        #fig = plt.figure()
##        fig = plt.figure(figsize=(7,len(model_list)*0.53))
##        fig.subplots_adjust(bottom=0.2, top=0.8, left=0.2)
##        ax = fig.add_subplot(1,1,1)
##        ax.set_xlim(0,3)
##        ax = model_list.create_scatter_plot_plus_rand(
##            ax
##            ,x='partitioning_scheme_nr'
##            ,y='claimed_dyn_part_nr'
##            ,x_label='Partitioning scheme'
##            ,y_label='Claimed to have a \n dynamic partitioning scheme?'
##            ,model_symbol_mapping=mapping
##        )
##        ax.set_xticks([1,2])
##        ax.set_xticklabels(['fixed','dynamic'])
##        ax.set_yticks([1,2])
##        ax.set_yticklabels(['No','Yes'])
##        
##        rel += MatplotlibFigure(fig,"Figure 7","Type of carbon partitioning scheme among pools and claim to have a dynamic partitionings" )
##
###########################################################################
##        # fixme:
##        # the models in the model_list should be selected by whether they have a cycling matrix or not (Vegetation Models)
##        model_list= ModelList(
##            m for m in model_list 
##            if hasattr(m,"cyc_matrix")
##        )
##        fig = plt.figure(figsize=(7,len(model_list)*0.53))
##        fig.subplots_adjust(bottom=0.2, top=0.8, left=0.2)
##        ax = fig.add_subplot(1,1,1)
##        ax = model_list.create_scatter_plot_plus_rand(
##            ax
##            ,x='nr_state_v'
##            ,y='cyc_matrix_diagonal_nr'
##            ,x_label='No. state variables'
##            ,y_label='Diagonal matrix?'
##            ,model_symbol_mapping=mapping
##        )
##        ax.set_yticks([1,2])
##        ax.set_yticklabels(['No','Yes'])
##        
##        rel += MatplotlibFigure(fig,"Figure 8","Number of state variables and C cycling among compartments" )
##
############################################################################
##
##        target_key="state_vector"
##        # first check wich models actually provide the target_key we are looking for
##        models_with_target_key = ModelList(
##           m for m in model_list
##           if m.has_key(target_key)
##        )
##
##        fig = plt.figure(figsize=(30,15), tight_layout=True)
##        # note that the second argument 1 in figsize is required by matplotlib 
##        # but ignored by the following method because the 
##        # height will be adapted inside the method
##        nr_row = 2
##        ax = fig.add_subplot(nr_row,1,1)
##        models_with_target_key.plot_dependencies(target_key,ax)
##        ax = fig.add_subplot(nr_row,1,2)
##        models_with_target_key.plot_model_key_dependencies_scatter_plot(target_key,ax)
##
##        rel += MatplotlibFigure(fig,"Figure 6","Dependency plots of compartment variables" )
############################################################################
##        
##
##        rel += Header("Bibliography", 1)
#        rel.write_pandoc_html(output_path)
#






#def generate_html_dir(src_dir, target_dir):
#
#    target_dir_path = Path(target_dir)
#    src_dir_path= Path(src_dir)
#    print("Targetdirectory: "+str(target_dir_path))
#    
#    html_dir_path = target_dir_path.joinpath("html")
#    
#    rec_list=[ rec  for rec in src_dir_path.glob('*.yaml')]
#    for rec in rec_list:
#        try:
#            create_single_report(rec,html_dir_path)
#        except Exception as e:
#            print("##################")
#            print("problems with file: "+str(rec))
#            print(e)
#            print("##################")
#    
#
#    ml=ModelList.from_dir_path(src_dir_path)
#    create_overview_report(ml,html_dir_path,'list_report.html')
#
#def create_single_report(yaml_file_path, target_dir_path):
#    model = Model.from_path(yaml_file_path)
#    dir_name = yaml_file_path.stem
#    #dir_name = model.bibtex_entry.key
#    #if model.modelID: dir_name += "-" + model.modelID
#    #fixme mm: I think we should avoid the modelID property
#    #and ensure uniqe filenames by requesting them
#
#    #html_file_path= target_dir_path.joinpath(dir_name,"Report.html")
#    html_file_path= target_dir_path.joinpath(dir_name,"index.html")
#    rel = report_from_model(model) 
#    rel.write_pandoc_html(html_file_path)

#def generate_website():
#    generate_model_run_reports()

def render_parse():
    parser = argparse.ArgumentParser(parents=[common_parser])

    parser.description="""
    Create markdown and html report from a template and either a single yaml file  or a directory of yaml files.
    This command line tool calls the render function with either a Model or a ModelList object. You can write your own scripts to provide your own templates with more arguments for rendering.
    """
    parser.add_argument('template', default=None, help="The path to the template file containing the description of the report." )

    sources= parser.add_mutually_exclusive_group(required=True)
    sources.add_argument('-sd','--src_dir', default=None, help="The path to the directory containing the yaml files sourced by the report. Either this or -y must be present. " )
    sources.add_argument('-y', '--yaml', default=None, help="The path to the yaml file containing the description of the record. Either this or -sd must be present." )
    
    parser.epilog= Template("""Examples:\n
        ### example 1:
        ${p} report_templates/multiple_model/Website.py -sd data/tested_records -t ${o}
        ### example 2:
       ${p} report_templates/single_model/MinimalSingleReport.py -y data/tested_records/Henin1945Annalesagronomiques.yaml  -t ${o} """).substitute(p=parser.prog,o="output" ) 

    com=parser.parse_args()
    template_path=Path(com.template)
    #reference the template in the output html filename
    #fn=template_path.stem+".html"
    #fn="index.html"
    fn=defaults()['html_filename']

    if com.target_dir is not None:
        target_dir_path=Path(com.target_dir)
    else:
        target_dir_path=Path(".")

    if com.yaml: 
        yaml_file_path=Path(com.yaml)
        model=Model.from_path(yaml_file_path)
        rel=render(template_path,model)
        dir_name = yaml_file_path.stem
        html_file_path= target_dir_path.joinpath(dir_name,fn)
        rel.write_pandoc_html(html_file_path)
    else:
        model_list=ModelList.from_dir_path(Path(com.src_dir))
        rel=render(template_path,model_list)
        html_file_path= target_dir_path.joinpath(fn)
        rel.write_pandoc_html(html_file_path)
    sys.exit(0)
    

########################################################################
def render(template_path,*args,**kw):
    
    with template_path.open() as f:
        #print('####################')
        #print(str(template_path))
        code= compile(f.read(),template_path,mode='exec')
        #code=f.read()
    
    exec(code,globals(),locals()) # this makes the template function defined in the file available 
    
    # fixme mm 2019:
    # the function should not become part of the global namespace
    # but be executed in a separate environment

    # call the function defined in the template
    func=locals()['template']
    rel= func.__call__(*args,**kw)
    return rel

########################################################################
def render2(template_path,*args,**kw):
    
    with template_path.open() as f:
        print('####################')
        print(str(template_path))
        code= compile(f.read(),template_path,mode='exec')
        #code=f.read()
    
    exec(code,globals(),locals()) # this makes the template function defined in the file available 
    
    # fixme mm 2019:
    # the function should not become part of the global namespace
    # but be executed in a separate environment

    # call the function defined in the template
    func=locals()['template']
    rel= func.__call__(*args,**kw)
    return rel
