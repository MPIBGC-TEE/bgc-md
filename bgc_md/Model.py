# vim:set ff=unix expandtab ts=4 sw=4:
from copy import copy, deepcopy
from pathlib import Path
from sympy import sympify, Symbol, flatten, Matrix, diff, MatrixSymbol, simplify, Eq, zeros, eye, diag 
from sympy.core import Atom

import re
import string
import yaml
import builtins
import sys
import pandas as pd
import numpy as np

from .ReportInfraStructure import Text, Math, ReportElementList, TableRow, Table, Header, Newline
from .bibtexc import BibtexEntry, DoiNotFoundException, online_entry
from .helpers import remove_indentation, create_symbols_func, eval_expressions, retrieve_or_default, retrieve_this_or_that, py2tex_silent
from .helpers_reservoir import factor_out_from_matrix
from .DataFrame import DataFrame
from .Exceptions import ModelInitializationException
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun


######### helper functions #############
# fixme: what does this function really count?
def depth(expr):
    expr = sympify(expr)

    if isinstance(expr, Atom):
        return 1
    else:
        if len(expr.args) == 0:
            return 0
        return 1 + max([depth(arg) for arg in expr.args])

#def load_complete_dict_and_id(complete_dict):
#    if ('model' not in complete_dict) or (not complete_dict['model']):
#        raise(ModelInitializationException("yaml file does not contain a model section:\n\n" + str(complete_dict)))
#
#    #mandatory_tags = tuple()
#    #for tag in mandatory_tags:
#    #    if (tag not in complete_dict) or (not complete_dict[tag]):
#    #        raise(ModelInitializationException("Did not find '" + tag +"' in:\n\n" + str(complete_dict)))
#
#    #fixme: remove that as soon as possible
#    #if 'model-id' not in complete_dict.keys():
#    #    complete_dict['model-id'] = ''
#
#    return complete_dict, complete_dict['model-id'] 


def convert_yaml_bibtex_str(yaml_bibtex_str):
    entry_str = yaml_bibtex_str
    entry_str = entry_str.replace(",", ",\n", 1)
    entry_str = entry_str.replace("},", "},\n")
    entry_str = entry_str.replace(" }", "\n}")
    return entry_str


def load_bibtex_entry(complete_dict):
    # load BibTex entry, priority: yaml file, then by doi, 
    # also retrieve abstract if entry is fetched by doi
    # we do not 
    tag = 'bibtex'
    if tag in complete_dict.keys():
        # prepare bibtex string from yaml file for initialisation
        entry_str = convert_yaml_bibtex_str(complete_dict[tag])
        return BibtexEntry.from_entry_str(entry_str)
    elif 'doi' in complete_dict.keys():
        return BibtexEntry.from_doi(doi=complete_dict['doi'], abstract=True)


def load_abstract(complete_dict, bibtex_entry):
    abstract = None
    # if abstract given in yaml file, keep it
    tag = 'abstract'
    if tag in complete_dict.keys() and complete_dict[tag]:
        abstract = complete_dict[tag]

    else:# load abstract from BibTeX entry if possible
        if bibtex_entry:
            abstract = bibtex_entry.get_abstract(format_str="BibLaTeX")

    # try to convert common strangely written terms in the abstract to good-looking ones
    # works only with Text("abstract: $a", a=abstract) from ReportElementList
    # attention: − is not - !!!
    if abstract:
        special_terms = {"CO\(2\)": 'CO$_2$', "CO2": 'CO$_2$', "yr-1": 'yr$^{-1}$', "MJ-1": 'MJ$^{-1}$', "year−1": 'year$^{-1}$', "ha−1": 'ha$^{-1}$', "\(lai\)": '(LAI)', "\slai\s": ' LAI '}
        for key in special_terms.keys():
            regexp = re.compile(key)
            abstract = regexp.sub(special_terms[key], abstract)

    return abstract


def load_further_references(complete_dict):
    further_references = []
    tag = 'further_references'
    # load BibTex entry, priority: yaml file, then by doi, also retrieve abstract if entry is fetched by doi
    if tag in complete_dict.keys():
        frefs = complete_dict[tag]
        # treat it always as a list
        if type(frefs) != type ([]): frefs = [frefs]

        for ref_dict in frefs:
            ref = dict()
            tag2 = 'bibtex'
            if (tag2 in ref_dict.keys()) and (ref_dict[tag2]):      
                # prepare bibtex string from yaml file for initialisation
                entry_str = convert_yaml_bibtex_str(ref_dict[tag2])
                ref['bibtex_entry'] = BibtexEntry.from_entry_str(entry_str)
            elif ('doi' in ref_dict.keys()) and (ref_dict['doi']):
                try:
                    ref['bibtex_entry'] = BibtexEntry.from_doi(ref_dict['doi'])
                except DoiNotFoundException as e:
                    ex_string = "Invalid doi in further_references."
                    raise(ModelInitializationException(ex_string + "\n" + e.__str__()))
            else:
                ex_string = "Missing 'doi' and 'bibtex' in further_references."
                raise(ModelInitializationException(ex_string))
            if ref:
                tag3 = 'desc'
                if tag3 in ref_dict.keys():
                    ref[tag3] = ref_dict[tag3]
                further_references.append(ref)
    else:
        further_references = None

    return further_references


def load_reviews(complete_dict):
    deeply_reviewed = False
    tag = 'reviews'
    if tag in complete_dict.keys():
        reviews = complete_dict[tag]
        for review in reviews:
            obligatory_keys = ('reviewer', 'date', 'desc', 'type')
            for obl_key in obligatory_keys:
                if (obl_key not in review.keys()) or (not review[obl_key]):
                    ex_string = "Missing '" + obl_key + "' in review list."
                    raise(ModelInitializationException(ex_string))
            if review['type'] == 'deep':
                deeply_reviewed = True        
    else:
        reviews = None       

    return (reviews, deeply_reviewed)


def load_sections_and_titles(complete_dict):
    # return sections of the model as a list, e.g., ['state_variables', 'section_variables']
    # return section_titles as a dictionary: section_title[section_name] = title
    # return a to the new section_names adapted complete_dict

    new_complete_dict = deepcopy(complete_dict)
    sections = [list(sec)[0] for sec in complete_dict['model']]
       
    # allow alternative section title
    # in yaml file 
    #               - state_variables
    #                   C:
    # leads to "State Variables" as section title
    #               - state_variables[Alternative Title]
    #                   C:
    # leads to "Alternative Title" as section title

    new_section_names = []
    section_titles = {}
    for section_name in sections:
        regexp = re.compile("\[(?P<title>.*)\]")
        result = regexp.search(section_name)
        if result:
            title = result.group('title')
            new_section_name = section_name.replace("[" + title + "]", "")
            new_section_names.append(new_section_name)

            # adapt the section name in new_complete_dict
            model_list = new_complete_dict['model']
            for index, dic in enumerate(model_list):
                if section_name in dic.keys():
                    section_data = dic[section_name]
                    new_section = {new_section_name: section_data}
                    model_list[index] = new_section

            section_titles[new_section_name] = title
        else:
            new_section_names.append(section_name)
            section_titles[section_name] = string.capwords(section_name.replace("_", " "))
    
    for section in new_section_names:
        if new_section_names.count(section) > 1:
            raise(ModelInitializationException("The model contains more than one subsection called '" + section + "'."))
            
    return (new_section_names, section_titles, new_complete_dict)


def section_subdict(complete_dict, target_key):   
    # extract the part of the complete_dict with which we are dealing
    model_list = complete_dict["model"]
    matching = [dic for dic in model_list if target_key in dic.keys()]

    if len(matching) == 0:
        raise(ModelInitializationException('Subsection ' + target_key + ' not found.'))
    if len(matching) > 1:
        raise(ModelInitializationException('Subsection ' + target_key + ' not unique.' + 'found:' + str(len(matching))+'.'))

    return matching[0]
        

# helper function for load_df
def get_all_colnames(complete_dict, variables_sections):
    colnames = set()
    for sec in variables_sections:
        section_dic = section_subdict(complete_dict, sec) # {'state_variables': [...]}
        colnames |= get_all_colnames_of_section_dict(section_dic)
    return sorted(list(colnames))

# helper function for get_all_colnames
def get_all_colnames_of_section_dict(section_dic):
    colnames = set()
    for sec_name, var_list in section_dic.items():
        for var_dic in var_list:
            # var_dic = {'C': {'exprs': 'C=...', 'desc': '...'}}
            # or var_dic = 'C'
            if type(var_dic) == builtins.dict:
                for var, props in var_dic.items():
                    if props: # maybe var_dic = {'C': }
                        for colname, value in props.items(): # ('desc', '...')
                            colnames |= {colname}
    return colnames


def load_df(complete_dict, sections):
    no_variables_sections = ('parameter_sets', )
    variables_sections = [el for el in sections if el not in no_variables_sections]

    additional_colnames = get_all_colnames(complete_dict, variables_sections)

    row_list = []
    colnames = ['name', 'category'] + additional_colnames
    row_list.append(colnames)
    for sec in variables_sections:
        section_dic = section_subdict(complete_dict, sec) # {'state_variables': [...]}
        for sec_name, var_list in section_dic.items():
            for var_dic in var_list:
                # var_dic = {'C': {'exprs': 'C=...', 'desc': '...'}}
                # or var_dic = {'C': }
                if type(var_dic) == builtins.dict:
                    for var, props in var_dic.items():
                        row = [var, sec]
                        for colname in additional_colnames:
                            # props might be empty if var_dic = {'C:}
                            if props and colname in props.keys(): 
                                row.append(props[colname])
                            else:
                                row.append(None)
                elif type(var_dic) == builtins.str:
                    row = [var_dic, sec]
                    for colname in additional_colnames:
                        row.append(None)
                else:
                    raise(ModelInitializationException('Variable description wrong in ' + sec + '.'))
                row_list.append(row)

    df = DataFrame(row_list)

    var_list = df.get_column('name')
    for v in var_list:
        if var_list.count(v) > 1:
            raise(ModelInitializationException("Variable '" + v + "' defined more than once."))

    return df

        
def load_expressions_and_symbols(complete_df):
    exprs_list = []
    symbols_list = []

    for row_dic in complete_df.rows_as_dictionary:
        if row_dic['exprs']:
            exprs_list.append(row_dic['exprs'])
            exprs_list = flatten(exprs_list)
        else:
            symbols_list.append(row_dic['name'])

    # symbols_list contains a list of symbols as strings
    # exprs_list contains a list of strings representing equations given in the yaml file

    # create the symbols stored as strings --> python variables in l
    g, l = create_symbols_func(symbols_list)
  
    # run the commands coming from the equations stored as strings in self.expressions --> new python variables are created --> added to l
    eval_expressions(exprs_list, g, l)

    # store symboks in syms_dict (python variables)
    syms_dict = {name: l[name] for name in symbols_list}

    # store evaluated expressions in exprs_dict (python variables)
    exprs_dict = {}
    for expr_string in exprs_list:
        name = expr_string.split("=", 1)[0].strip()
        exprs_dict[name] = l[name]
    exprs_dict = exprs_dict

    # create 'empty' sympy symbols for all symbols in the yamls file and all symbols coming from equations
    # initialize them as 'empty' MatrixSymbol if they are a Matrix, so sympify will not reorder them alphanumerically ignoring rules of matrix multiplication
    # --> self.symbols_by_type
    symbols_by_type = {name: Symbol(name) for name in symbols_list}
    for name in exprs_dict.keys():
        sym = exprs_dict[name]
        if hasattr(sym, 'is_Matrix') and sym.is_Matrix == True:
            symbols_by_type[name] = MatrixSymbol(name, sym.rows, sym.cols)
        else:
            symbols_by_type[name] = Symbol(name)

    return (syms_dict, exprs_dict, symbols_by_type)


def load_model_run_data(complete_dict):
    try:
        tag = 'model_run_data'
        if tag in complete_dict.keys() and complete_dict[tag]:
            res = complete_dict[tag]
        else:
            res = {}
    except Exception as e:
        raise(Exception('Could not load model_run_data.\n' + e.__str__()))
    return(res)


# helper function for loading parameter sets and initial values since they have the same structure
def load_from_model_run_data(model_run_data, attr_name):
    # attr_name = 'parameter_sets' or attr_name = 'initial_values'
    
    # fixme mm 18.05.2018
    # this is a typical  examle of a function that seems too deeply nested
    # It tries to solve problems that should be solved on the level of the caller
    # This would make knowledge about fields like "values" and "table_head" unnecessary.
    # This is also a kind of duplication. (probably arising from the attempt to remove duplicated code)

    
    # fixme mm 18.05.2018
    # the next line checks something that looks as if it should be checked in the caller
    if (not attr_name in model_run_data.keys()) or (not model_run_data[attr_name]): return []

    parset_list = model_run_data[attr_name]

    res_list = []
    for parset in parset_list:
        for parset_name in parset.keys():
            lel = dict()
            # fixme mm 18.05.2018
            # The name "table_head" is secret knowledge spread through the class
            lel['table_head'] = parset_name
            lel.update(parset[parset_name])
            if not 'values' in lel.keys():
                raise(ModelInitializationException("No values given in data set '" + lel['table_head'] + "'."))

            if 'bibtex' in lel.keys():
                # prepare bibtex string from yaml file for initialisation
                entry_str = convert_yaml_bibtex_str(lel['bibtex'])
                lel['bibtex_entry'] = BibtexEntry.from_entry_str(entry_str)
                del lel['bibtex']
            elif 'doi' in lel.keys():
                try:
                    lel['bibtex_entry'] = BibtexEntry.from_doi(doi=lel['doi'])
                    del lel['doi']
                except DoiNotFoundException as e:
                    #ex_string = "Invalid doi in parameter set '" + lel['table_head'] + "'."
                    ex_string = "could not fetch doi " + lel['table_head'] + "'."
                    raise(ModelInitializationException(ex_string + "\n" + e.__str__()))
            else:
                lel['bibtex_entry'] = None

            if type(lel['values']) != type(dict()):
                raise(ModelInitializationException("Data set '" + lel['table_head'] + "' invalid, probably forgotten space after colon."))
    
            for par_key, par_val in lel['values'].items():
                if type(par_val) == type(''):      
                    try:                  
                        # no cnonversion to float here, because 'Rational(1,3)' needs to be kept
                        lel['values'][par_key] = par_val
                    except ValueError as e:
                        raise(ModelInitializationException("Data set '" +lel['table_head'] + "' invalid.\n" + e.__str__()))
        
        res_list.append(lel)

    return res_list


def load_parameter_sets(model_run_data):
    if not model_run_data: 
        return []
   
    target_key = 'parameter_sets' 
    
    if not target_key in model_run_data.keys():
        return []

    try:
        par_sets=load_from_model_run_data(model_run_data, target_key)
        return par_sets 

    except Exception as e:
        ex_str = "Could not load parameter sets."
        raise(ModelInitializationException(ex_str + "\n" + e.__str__()))
        

def load_initial_values(model_run_data):
    if not model_run_data: return []

    try:
        return load_from_model_run_data(model_run_data, 'initial_values')
    except Exception as e:
        ex_str = "Could not load initial values."
        raise(ModelInitializationException(ex_str + "\n" + e.__str__()))
        

def check_parameter_set_valid(par_set, syms_by_type):
    # fixme mm05.18.2018:
    # This whole function might be obsolete 
    # I think that it is enough to check for completeness of 
    # a parameter.
    # we should not need the execution of strings at all..
    cond=not par_set
    if cond : 
        return True

    par_dict = par_set['values']

    l = deepcopy(syms_by_type)
    l['par_dict'] = par_dict
    g = copy(l)
    #fixme mm 05.18.2018:
    #the following line looks realy dangerous
    exec("from sympy import *", g, l)
    for name in par_dict.keys():
        cmd = name + " = " + name + ".subs(par_dict)"
        try:
            exec(cmd, g, l)
        except Exception as e:
            ex_str = "Invalid parameter set: " + par_set['table_head']
            ex_str += "\nCould not substitute '" + name + "'"
            raise(ModelInitializationException(ex_str + "\n" + e.__str__()))

            return False   
    return True


def check_parameter_set_complete(par_set, state_vector, time_symbol, state_vector_derivative):
    if not par_set: return False

    par_dict = par_set['values']
    free_symbols = (state_vector_derivative['expr'].subs(par_dict)).free_symbols

    if time_symbol:
        free_symbols -= {time_symbol['symbol']} 
    free_symbols -= set(state_vector['expr'])

    if free_symbols != set():
        print(free_symbols)
    return free_symbols == set()


def check_initial_values_set_valid(par_set, syms_by_type, state_variables):
    if not par_set: return True

    par_dict = par_set['values']

    l = {sym_name: sym for sym_name, sym in syms_by_type.items() if sym_name in state_variables}
    l['par_dict'] = par_dict
    g = copy(l)
    exec("from sympy import *", g, l)
    for name in par_dict.keys():
        cmd = name + " = " + name + ".subs(par_dict)"
        try:
            exec(cmd, g, l)
        except Exception as e:
            ex_str = "Invalid initial values set: " + par_set['table_head']
            ex_str += "\nCould not substitute '" + name + "'"
            raise(ModelInitializationException(ex_str + "\n" + e.__str__()))

            return False   
    return True


def check_initial_values_complete(iv, state_vector):
    if not iv: return False

    iv_dict = iv['values']
    free_symbols = (state_vector['expr'].subs(iv_dict)).free_symbols

    return free_symbols == set()


def check_parameter_sets_valid(par_sets, syms_as_type):
    if par_sets is None: 
        return True

    valid = True
    for par_set in par_sets:
        cond=check_parameter_set_valid(par_set, syms_as_type)
        if not cond:
            valid = False
    return valid


def check_initial_values_valid(par_sets, syms_as_type, state_variables):
    if not par_sets: return True

    valid = True
    for par_set in par_sets:
        if not check_initial_value_set_valid(par_set, syms_as_type, state_variables):
            valid = False
    return valid


def load_run_times(model_run_data):
    if not model_run_data: return []
    if 'run_times' not in model_run_data.keys(): return []

    result = []

    run_times_dic_list = model_run_data['run_times']
    for dic in run_times_dic_list:
        res_dic = dict()
        for name in dic.keys():
            res_dic['name'] = name
            sub_dic = dic[name]

            mandatory_keys = ('start', 'end', 'step_size')
            for mk in mandatory_keys:
                if not mk in sub_dic:
                    raise(ModelInitializationException("'run_times' data set '" + name + "' does not contain '" + mk + "'"))

            res_dic.update(sub_dic)

            if res_dic['start'] > res_dic['end']:
                raise(ModelInitializationException("'run_times' data set '" + name + "' has 'start' > 'end'"))

        result.append(res_dic)
    
    return result


def load_model_run_combinations(model_run_data, parameter_sets, initial_values, run_times, state_vector, time_symbol, state_vector_derivative):
    if not model_run_data: 
        return [], None
    if not 'possible_combinations' in model_run_data.keys(): 
        return [], None

    msg = None

    poss_comb = model_run_data['possible_combinations']

    complete_parameter_sets = [par_set for par_set in parameter_sets if check_parameter_set_complete(par_set, state_vector, time_symbol, state_vector_derivative)]

    complete_initial_values = [iv for iv in initial_values if check_initial_values_complete(iv, state_vector)]

    result = []
    for pc in poss_comb:
        dic = dict()
  
        par_set = None
        for ps in complete_parameter_sets:
            if ps['table_head'] == pc[0]:
                par_set = ps
        dic['par_set'] = par_set

        iv = None
        for x in complete_initial_values:
            # we use negative indices to avoid trouble with missing parameter sets
            if x['table_head'] == pc[-2]:
                iv = x
        dic['IV'] = iv

        run_time = None
        for rt in run_times:
            # we use negative indices to avoid trouble with missing parameter sets
            if rt['name'] == pc[-1]:
                run_time = rt
        dic['run_time'] = run_time

        if iv and run_time:
            if par_set:
                result.append(dic)
            else:
                # even if there is no parameter set we might be able to run the model
                # if it does not contain free symbols
                free_symbols = (state_vector_derivative['expr']).free_symbols
                if time_symbol:
                    free_symbols -= {time_symbol['symbol']} 
                free_symbols -= set(state_vector['expr'])
                if  len(free_symbols)==0:
                    result.append(dic)
                else:
                    print("##########################################")
                    print(free_symbols)
                    print("##########################################")
                    msg = "Model run combination  '" + str(pc) + "' is invalid. There are free symbols but no parameter set is given"

            
        else:
            msg = "Model run combination  '" + str(pc) + "' is invalid"
            if not par_set:
                msg += "\nParameter set '" + pc[0] + "' is incomplete"
            if not iv:
                msg += "\nInitial values '" + pc[1] + "' are incomplete"

    return result, msg

            
######### Class #############
class Model:
    
    @classmethod
    def from_str(cls,yaml_str, id):
        try:
             complete_dict = yaml.load(yaml_str)
        except yaml.YAMLError as ye:
            raise(ye)
            
        model = cls(complete_dict, id ) # call to __init__
        return(model)

    @classmethod
    def from_file(cls, yaml_file_name): 
        yaml_file_path=Path(yaml_file_name)
        model = cls.from_path(yaml_file_path)
         
        return model
    
    @classmethod
    def from_path(cls, yaml_file_path): 
        # We could create the new model by a call to its
        #   model = cls.from_str(yaml_str,id=name)
        # This would call init and thus implicitly __new__(cls) 
        # to create the model  and  then initialize it.
        #
        # Instead we create the model explicitly with __new__(cls) 
        # and immidiately set its yaml_file_path property 
        # in case something goes wrong with the initialization 
        # we can at least report the location of the problematic file

        #create a new model
        model=object.__new__(cls)
        model.yaml_file_path=yaml_file_path
        
        with yaml_file_path.open() as f:
            yaml_str = f.read()
        name=yaml_file_path.stem
        # now load the yaml str into a dictionary
        try:
             complete_dict = yaml.load(yaml_str)
        except yaml.YAMLError as ye:
            msg=Template("The Yaml in file ${ps} caused the following exception ${submsg}").substitute(ps=str(model.yaml_file_path),submsg=str(ye))
            raise(ModelInitializationException(msg))
            

        model.__init__(complete_dict,id=name)
        return model

    def editable_vars(self):
        # fixme: this is still under construction
        #return ['yaml_file_path','id','bibtex_entry']
        return ['bibtex_entry']

    @property
    def name(self):
        return retrieve_this_or_that("name",self.id,self.complete_dict)

    def __init__(self, complete_dict, id= None):
        # every model can be given a unique id (like a key in a database table) 
        # usually we will use the filename for this because it is unique by definition
        # for models created directly from strings we provide it as a parameter.
        self.id=id
        try:
            self.complete_dict = complete_dict
            try:
                self.bibtex_entry = load_bibtex_entry(self.complete_dict)
            except DoiNotFoundException:
                print("could not find BibtexEntry by doi")
                if hasattr(self,'bibtex_entry'): 
                    abstract =load_abstract(self.complete_dict, self.bibtex_entry)
                if abstract is not None:
                    self.abstract = abstract

            self.further_references = load_further_references(self.complete_dict)
            self.reviews, self.deeply_reviewed = load_reviews(self.complete_dict)
            self.sections, self.section_titles, self.complete_dict = load_sections_and_titles(self.complete_dict)
            #fixme mm:
            # if we want to switch to pandas the load_df should become obsolete
            self.df = load_df(self.complete_dict, self.sections)
            self.syms_dict, self.exprs_dict, self.symbols_by_type = load_expressions_and_symbols(self.df) 
            self.set_component_keys()

            self.model_run_data = load_model_run_data(self.complete_dict)
            self.parameter_sets = load_parameter_sets(self.model_run_data)
            check_parameter_sets_valid(self.parameter_sets, self.symbols_by_type)
            self.initial_values = load_initial_values(self.model_run_data)
            self.run_times = load_run_times(self.model_run_data)

            self.model_run_combinations, msg = load_model_run_combinations(self.model_run_data, self.parameter_sets,
                     self.initial_values, self.run_times, self.state_vector, self.time_symbol, 
                     self.state_vector_derivative)
            if msg:
                print("-------------")
                print('Warning at initializing model ' + self.id)
                if hasattr(self,"yaml_file_path"):
                    print(str(self.yaml_file_path))
                print(msg)
                print("-------------")
            
            #self.parameter_sets=[]
        except Exception as ex:

            print("-------------")
            print('Initializing model ' + self.id + ' failed.')
            if hasattr(self,"yaml_file_path"):
                print(str(self.yaml_file_path))
            print(ex)
            print("-------------")
            raise(ex)

    @property
    def nr_state_v(self):
        nr_state_v = 0
        for sec in self.sections:
            if sec == "state_variables":
                nr_state_v = self.section_vars('state_variables').nrow
        return nr_state_v

    @property
    def state_variables(self):
        return [var for var in self.state_vector["expr"]]
        #return(self.section_vars("state_variables").get_column("name"))

    @property
    def time_symbol(self):
        name = self.get_component_name_by_key('time_symbol')
        if not name: return None

        sym = self.symbols_by_type[name]
        unit = self.df.get_by_cond('unit', 'name', name)
        return {'name': name, 'symbol': sym, 'expr': None, 'unit': unit}

   
    def get_component_name_by_key(self, comp_key):
        df = self.df
        for i, name in enumerate(df.get_column("name")): 
            entry = df[i,"key"]
            if entry:
                if not(isinstance(entry,list)):
                    entry=[entry]
                if comp_key in entry:
                    return(name)
        return None

    # fixme: 
    # duplicating set_component_keys(self) see below
    # lacking test
    def get_component_keys(self):
        df = self.df
        ed = self.exprs_dict
        syms = self.symbols_by_type
        comp_keys = flatten([keys for i, keys in enumerate(df.get_column('key')) if df[i, 'category'] == 'components'])
        comp_keys = [key for key in comp_keys if key]
        return(comp_keys)

    # fixme:
    # a bit dangerous since the name space inside the Model class
    # gets crowded by keys from the yaml file 
    # Instead of usign itself as a dict a Model instance could delegate this
    # task to a dict instead which would prevent possible collissions automatically
    # We have to think about a strategy for this

    def set_component_keys(self):
#        df = self.df
        ed = self.exprs_dict
        syms = self.symbols_by_type
#        comp_keys = flatten([keys for i, keys in enumerate(df.get_column('key')) if df[i, 'category'] == 'components'])
#        comp_keys = [key for key in comp_keys if key]
        comp_keys = self.get_component_keys()
        for comp_key in comp_keys:
            comp_name = self.get_component_name_by_key(comp_key)
            
            if comp_name in ed.keys():
                expr = ed[comp_name]
            else:
                expr = syms[comp_name]
            dic = {'name': comp_name, 'symbol': syms[comp_name], 'expr': expr}

            if hasattr(self, comp_key):
                raise(ModelInitializationException("Invalid component key: '" + comp_key + "'"))

            setattr(self, comp_key, dic)


#    def set_state_vector(self):
#        df=self.df
#        ed=self.exprs_dict
#        for i,name in enumerate(df.get_column("name")): 
#            entry= df[i,"keys"]
#            if entry:
#                if not(isinstance(entry,list)):
#                    entry=[entry]
#                if "state_vector" in entry:
#                    return(ed[name])

   
    def _varlist_by_type(self,typestr): 
    #fixme: Move to Data Frame
        df=self.df
        h=df.head
        if "type" not in h:
            print("there is no type information in this file")
            #fixme throw a warning (or catchable exception here) 
            # so that printing and stopping can be chosen by a command
            # line flag
            return([])
         
        names=df[:,"name"]
        types=df[:,"type"]
        selected_names=[name for i,name in enumerate(names) if types[i]==typestr]
        return(selected_names) 

    @property
    def variables(self):
        selected_names=self._varlist_by_type("variable")
        return(selected_names+self.state_variables)

    @property
    def nr_variables(self):
        return(len(self.variables))

    @property
    def parameters(self):
        selected_names=self._varlist_by_type("parameter")
        return(selected_names)

    @property
    def nr_parameters(self):
        return(len(self.parameters))
	

        




    @property
    def entryAuthor(self):
        return retrieve_or_default(self.complete_dict, "entryAuthor")
        # fixme 
        # avoid complete_dict references outside init

    @property
    def entry_creation_date(self):
        return retrieve_or_default(self.complete_dict, "entryCreationDate")
        # fixme 
        # avoid complete_dict references outside init

    @property
    def last_modification_date(self):
        return retrieve_or_default(self.complete_dict, "lastModification")
        # fixme 
        # avoid complete_dict references outside init

    @property
    def entryAuthor_orc_id(self):
        return retrieve_or_default(self.complete_dict, "entryAuthorOrcid")
        # fixme 
        # avoid complete_dict references outside init

    @property
    def approach(self):
        appr = retrieve_or_default(self.complete_dict, "modApproach")
        if appr == "modApproach":
            appr = None
        return appr

    @property
    def partitioning_scheme(self):
        part = retrieve_or_default(self.complete_dict, "partitioningScheme")
        if part == "partitioningScheme":
            part = None
        return part
    
    @property
    def partitioning_scheme_nr(self):
        # This is a service for the scatterplots
        # Caution: do not use values = 0 because then it will asumme that it is None.
        if self.partitioning_scheme:
            if self.partitioning_scheme == "fixed": 
                part_scheme_nr = 1
            else:
                part_scheme_nr = 2
        else:
            part_scheme_nr=None
        return part_scheme_nr

    def yaml_file_provides(self,target_key):
        # the function checks if the Model defines target key
        # (was defined in the yaml file) or not
        return (target_key in self.complete_dict.keys())
    
    @property
    def claimed_dyn_part(self):
        return self.yaml_file_provides("claimedDynamicPart")
    
    @property
    def claimed_dyn_part_nr(self):
        # This is a service for the scatterplots to ask the model object 
        # whether the publication claimed to have a dynamic partitioning scheme or not.
        scdp= self.complete_dict["claimedDynamicPart"]
        if self.claimed_dyn_part:
            if scdp == "no": 
               claim_nr = 1
            else:
               claim_nr = 2
        else:
            claim_nr=None
        return claim_nr

    @property
    def cyc_matrix_diagonal_nr(self):
        # As a service to the scatterplot methods
        # we translate the  2 possible boolean values
        # true and false into integers 1, 2 or None
        if hasattr(self,"cyc_matrix"):
            scdp= self.cyc_matrix['expr'].is_diagonal()
            if not(scdp): 
               claim_nr = 1
            else:
               claim_nr = 2
        else:
            claim_nr=None
        return claim_nr


    @property
    def space_scale(self):
        sscale = retrieve_or_default(self.complete_dict, "spaceScale")
        if sscale == "spaceScale":
            sscale = None
        return sscale

    @property
    def time_resolution(self):
        tresol = retrieve_or_default(self.complete_dict, "timeResolution")
        if tresol == "timeResolution":
            tresol = None
        return tresol
    
    @property
    def fv(self):
        return(self.exprs_dict["f_v"])
        # fixme 
        # avoid complete_dict references outside init

    @property
    def fs(self):
        return(self.exprs_dict["f_s"])
    
    @property
    def rhs(self):
        if self.model_type == "vegetation_model":
            #return simplify(self.fv)
            return self.fv

        if self.model_type == "soil_model": 
            #return Matrix([simplify(c) for c in self.fs])
            return self.fs

        return None

    @property
    def model_type(self):
        fv = 0
        try:
            fv = self.fv
        except KeyError: pass
        if fv: return "vegetation_model"

        fs = 0
        try:
            fs = self.fs
        except KeyError: pass
        if fs: return "soil_model"

        return None

    @property    
    def keywords(self):
        if 'keywords' in self.complete_dict.keys():
            return  self.complete_dict['keywords']
        else:
            return None

    @property
    def principles(self):
        if 'principles' in self.complete_dict.keys():
            return self.complete_dict['principles']
        else:
            return None

    @property
    def spaceScale(self):
        if 'spaceScale' in self.complete_dict.keys():
            return self.complete_dict['spaceScale']
        else:
            return None


    @property
    def long_name(self):
        return retrieve_this_or_that("longName", None, self.complete_dict)
        # fixme 
        # avoid complete_dict references outside init


    @property
    def nr_ops(self):
        ops = 0
        for i in range(self.rhs.rows):
            #for j in range(self.rhs.cols):
            ops += self.rhs[i,0].count_ops()
        return ops

    @property
    def max_depth(self):
        d = 0
        for i in range(self.rhs.rows):
            d = max([d, depth(self.rhs[i,0])])
        return d

    @property
    def version(self):
        return retrieve_this_or_that("version","1",self.complete_dict)
        # fixme 
        # avoid complete_dict references outside init

    def jacobian(self):
        state_vec=self.state_vector['expr']
        vec=self.rhs
        dim = self.rhs.rows
        return(Matrix(dim,dim,lambda i,j: diff(vec[i],state_vec[j])))

    # fixme mm 14.5.2018
    # deprecate! 
    def allocation_coefficients_Table(self):
        return self.variables_Table_from_section("allocation_coefficients", parameter_values=True)
    
    # fixme mm 14.5.2018
    # deprecate! 
    def additional_variables_Table(self):
        return self.variables_Table_from_section("additional_variables", parameter_values=True)
    
    # fixme mm 14.5.2018
    # deprecate! 
    def state_variables_Table(self):
        # include possible initial values !!!
        return self.variables_Table_from_section("state_variables", parameter_values=False, initial_values=True)
    
    # fixme mm 14.5.2018
    # deprecate! 
    def components_Table(self):
        return self.variables_Table_from_section("components", parameter_values=False)

    # fixme mm 11.5.2018
    # deprecate! 
    def variables_Table_from_section(self, section_name, parameter_values = False, initial_values = False):
        df = self.section_vars(section_name)
        if parameter_values:
            df = self.add_data_columns_to_data_frame(df, self.parameter_sets)
        if initial_values:
            df = self.add_data_columns_to_data_frame(df, self.initial_values)
        # if table has only one column, add an empty second one for pandoc to treat it as a table
        if df.ncol == 1:
            df.append_column("-", ["-"]*df.nrow)
        return self.variables_Table_from_data_frame(df, self.section_titles[section_name])
        


    # fixme mm 11.5.2018
    # deprecate! 
    def variables_Table_from_data_frame(self, df, table_title, alternative_head=False):
        
        if df == None:
            return(Text(""))

        # check if parameter columns are there; if so, adapt the table head
        if alternative_head:
            add_el = Newline()
        else:
            add_el = Text("")
        
        provided_columns = df.head
        if alternative_head:
            colname_list = [Text("Name") + add_el*3]
        else:
            colname_list = [Text("Name")]
        format_list = ["c"]

        ignored_cols = ["key"]

        for index, colname in enumerate(provided_columns):
            if colname in ignored_cols:
                continue
            if index>0:
                if colname == "desc":
                    colname_list.append(Text("Description") + add_el*3)
                    format_list.append("l")
                elif colname == "exprs":
                    colname_list.append(Text("Expressions") + add_el*3)
                    format_list.append("c")
                elif colname == "key":
                    colname_list.append(Text("Keys") + add_el*3)
                    format_list.append("c")
                elif colname == "type":
                    colname_list.append(Text("Type") + add_el*3)
                    format_list.append("c")
                elif colname == "unit":
                    colname_list.append(Text("Units") + add_el*3)
                    format_list.append("c")
                elif colname == "-": # imaginary second column if table has just one: for pandoc to create a table
                    colname_list.append(Newline())
                    format_list.append("c")
                elif colname == "entryAuthorOrcid":
                    colname_list.append(Text("Entry Author Orcid") + add_el*3)
                    format_list.append("c")
                else:
                    if index == len(provided_columns) - len(self.parameter_sets):
                        colname_list.append(Text("Values") + Newline()*2 + Text(colname))
                    else:
                        colname_list.append(Newline()*2+ Text(colname))
                    format_list.append("c")

        name = provided_columns[0]
        headers_row = TableRow(colname_list)
        T = Table("Information on " + table_title, headers_row, format_list) #get the headline and number of columns and set format

        for row_dic in df.rows_as_dictionary:
            #for the first column we have to decide ... what?
            l = [Math("$v", v=sympify(row_dic[name], locals=self.symbols_by_type))]

            for colname in provided_columns:
                if colname in ignored_cols:
                    continue
                if colname != "name":
                    if colname in ("desc", "key", "type"):
                        d = row_dic[colname]
                        if d: 
                            l.append(Text("$d", d=d))
                        else: 
                            l.append(Text("-"))

                    elif colname == "exprs":
                        # fixme:
                        # in autogeneratedMD_holger.py there is a method for that
                        # maybe restructuring to a Model class and a Report class

                        # two possibilities in yaml file:
                        # 1)    exprs: "C = ..."
                        # 2)    exprs:
                        #           - "C = ..."
                        #           - "C = ..."
                        # so this table entry will be treated as a list of expressions
                        subl = ReportElementList([])
                        if row_dic["exprs"]:
                            if type(row_dic["exprs"]) == type(""):
                                expr_list = [row_dic["exprs"]]
                            if type(row_dic["exprs"]) == type([]):   
                                expr_list = row_dic["exprs"]

                            for index, expr_string in enumerate(expr_list):
                                if expr_string:
                                    # new line if not first entry
                                    if index > 0:
                                        subl.append(Newline()) 

                                    # fixme: with parsing first, we could use the evaluate=False option, probably. Would keep the order of the expressions.
                                    #fixme: as long as we allow printing of the expression only by coming from a python mathematical expression, we cannot prevent sympy from rearranging terms (except for matrix multiplication)
                                    # otherwise we would have to use something like py2tex to convert a python expression like 'f_s = I + A*C' to a latex string
                                    # py2tex cannot deal with 'Matrix([[1,2], [3,4]])'
                                    parts = expr_string.split("=",1)           
                                    parts[0] = parts[0].strip()
                                    parts[1] = parts[1].strip()
                                    p1 = sympify(parts[0], locals=self.symbols_by_type)
                                    p2 = sympify(parts[1], locals=self.symbols_by_type)

                                    # this is a hybrid version that keeps 'f_s = I + A*C' in shape, but if 'Matrix(...)' comes into play, rearranging by sympify within the matrix cannot be prevented
                                    # comment it out for a a clean version regarding use of ReportElementList, but with showing 
                                    # 'f_s = A * C + I' instead
                                    try:    
                                        p2 = py2tex_silent(parts[1]) 
                                    except TypeError:
                                       pass
 
                                    subl.append(Math("$p1=$p2", p1=p1,p2=p2))
                        else: 
                            subl.append(Text("-"))
                        l.append(subl)

                    elif colname == "unit":
                        u = row_dic["unit"]
                        if type(u) == type([]):
                            u = u[0]
                            
                        if u:
                            u = u.replace("*", "\cdot ")
                            u = u.replace("^-1", "^{-1}")
                            u = u.replace("^-2", "^{-2}")
                            u = u.replace("^-3", "^{-3}")
                            l.append(Math("$u", u=u))
                        else: 
                            l.append(Text("-"))
                    elif colname == "-":
                            l.append(Newline()) # imginary second column if table has only one: for pandoc to create table

                    elif colname == "entryAuthorOrcid":
                        orcid = row_dic["entryAuthorOrcid"]
                        if orcid:
                            l.append(Text("$o", o=orcid))
                        else:
                            l.append(Text("-"))

                    else: # considered to be used by parameter values
                        p = row_dic[colname]
                        if p or p==0:
                            l.append(Math("$par", par=sympify(p, locals=self.symbols_by_type)))
                        else:
                            l.append(Text("-"))

            tr = TableRow(l)
            T.add_row(tr)
        
        return(T)

    # fixme mm 11.5.2018
    # deprecate! 
    def add_data_columns_to_data_frame(self, data_frame, data):
        # return a data frame with appropriate parameter value columns from available parameter sets
        df = deepcopy(data_frame) # prevent side effects on 'data_frame' variable
        for par_set in data:
            new_column = []
            for variable in df[:, 0]:
                if variable in par_set['values'].keys():
                    new_column.append(par_set['values'][variable])
                else:
                    new_column.append(None)
            df.append_column(par_set['table_head'], new_column)

        return df


    def has_model_subsection(self,target_key):   
        # extract the part of the complete_dict with which we are dealing
        model_list = self.complete_dict["model"]
        matching = [dic for dic in model_list if target_key in dic.keys()]
        return len(matching)>0

    def section_subdict(self,target_key):   
        return(section_subdict(self.complete_dict,target_key))
    
    def section_pandas_df(self,target_key):   
        # pandas can create a DataFrame from a dictionary of array like objects
        # so we assemble it columnwise
        sd=section_subdict(self.complete_dict,target_key)
        dict_list=sd[target_key]
        additional_colnames = list(get_all_colnames_of_section_dict(sd))
        first_key=lambda d :list(d.keys())[0]
        first_val=lambda d :list(d.values())[0]

        first_col=[ first_key(d) for d in dict_list]
        col_dict={"name":first_col}
        for colname in additional_colnames:
            col=[]
            for var_dict in dict_list:
                # var_dict = {'C': {'exprs': 'C=...', 'desc': '...'}}
                # or var_dict = {'C': }
                var=first_val(var_dict)
                if type(var) == builtins.dict:
                    names=var.keys()
                    if colname in names:
                        col.append(var[colname])
                    else:
                        col.append(None)
                elif type(var) == builtins.str:
                    col.append(None)
                else:
                    raise(ModelInitializationException('Variable description wrong in ' + sec + '.'))
            col_dict[colname]=col
        return(pd.DataFrame(col_dict))
    
    @property
    def model_runs(self):
        mod=self.reservoir_model 
        model_runs=[]
        if hasattr(self, 'model_run_combinations'):
            for comb in self.model_run_combinations:
                # needs to have the symbols as keys, not the names
                if comb['par_set'] is not None:
                    par_set_names = comb['par_set']['values']
                    par_set = {self.symbols_by_type[name]: value for name, value in par_set_names.items()}
                else:
                    par_set=dict()
                # initial values need to be a list
                iv_dic = comb['IV']['values']
                iv = []
                for state_v_sym in self.state_vector['expr']:
                    for name, sym in self.symbols_by_type.items():
                        if sym == state_v_sym:
                            iv.append(iv_dic[name])
        
                run_time = comb['run_time']
                times = np.arange(run_time['start'], run_time['end']+run_time['step_size'], run_time['step_size'])
                mr = SmoothModelRun(mod, par_set, np.array(iv), times=times)
                model_runs.append(mr)
        return(model_runs)


    @property
    def reservoir_model(self):
            
        if self.model_type == "vegetation_model":
            C = self.state_vector['expr']
            f = self.state_vector_derivative['expr']

            if hasattr(self, 'input_vector'):
                I = self.input_vector['expr']
            else:
                if hasattr(self, 'scalar_func_phot') and hasattr(self, 'part_coeff'):
                    u = self.scalar_func_phot['expr']
                    b = self.part_coeff['expr']
                    I = u*b
                else:
                    I = zeros(x.rows, 1)
            if hasattr(self, 'cyc_matrix'):
                A = self.cyc_matrix['expr']
                if f != I + A*C:
                    raise(Exception('Unknown structure of time derivative of state variable'))
                state_vector=C
                compartmental_matrix=A
                input_vector=I

            elif hasattr(self, 'cyc_op_nonlin'): 
                N = self.cyc_op_nonlin['expr']
                
                if hasattr(self, 'trans_op'):
                    T = self.trans_op['expr']
                else:
                    T = eye(C.rows)
    
                if f != I + T*N*C:
                    raise(Exception('Unknown structure of time derivative of state variable'))
                state_vector=C
                compartmental_matrix=T*N
                input_vector=I

        elif self.model_type == "soil_model":
            C = self.state_vector['expr']
            f = self.state_vector_derivative['expr']
            df = self.df
    
            if hasattr(self, 'input_vector'):
                I = self.input_vector['expr']
            else:
                I = zeros(C.rows, 1)
    
            if hasattr(self, 'env_eff_mult'):
                xi = self.env_eff_mult['expr']
            else:
                xi = 1
            if hasattr(self, 'decomp_op_lin'):
                A = self.decomp_op_lin['expr']

                if f != I + xi*A*C:
                    raise(Exception('Unknown structure of time derivative of state variable'))
                state_vector=C
                compartmental_matrix=xi*A
                input_vector=I

            elif hasattr(self, 'decomp_op_nonlin'): 
                N = self.decomp_op_nonlin['expr']
                
                if hasattr(self, 'trans_op'):
                    T = self.trans_op['expr']
                else:
                    T = eye(C.rows)
    
                if f != I + xi*T*N*C:
                    raise(Exception('Unknown structure of time derivative of state variable'))
                state_vector=C
                compartmental_matrix=xi*T*N
                input_vector=I
        
        else:
            return None

        units = [self.df.get_by_cond('unit', 'name', sv.name) for sv in self.state_vector['expr']]
        #fixme: only one unit can be used for the contents, otherwise fluxes completely unclear
        # need to clearify unit treatment
        content_unit = units[0]

        if self.time_symbol:
            mod = SmoothReservoirModel.from_B_u(
                    C, 
                    self.time_symbol['symbol'],
                    compartmental_matrix, 
                    input_vector) 
                    #content_unit=content_unit, 
                    #time_unit=self.time_symbol['unit'])            
        else:
            mod = SmoothReservoirModel.from_B_u(
                    C, 
                    Symbol('t'), 
                    compartmental_matrix, 
                    input_vector)
                    #content_unit=content_unit)
            
            #fixme
            #raise(Exception("Not implemented yet:"))

            # The places to implement this feature are ReservoirModel and SmoothModelRun
            # SmoothModelRun should test if its ReservoirModel has  time_symbol and call
            # a different substitution
            # inventing a time Symbol is not a good solution since 
            # we would have to make sure that our invented symbol
            # has not already been used for something else which would be 
            # possible but cumbersome....
           
        return(mod)
    
    @property
    def fluxes(self):
        m=self.reservoir_model
        return(m.input_fluxes,m.output_fluxes,m.internal_fluxes)
#

#    def section_vars(self, target_key):
#        ss = self.section_subdict(target_key)
#        # ss could be None if there is no such subsection
#        if ss == None:
#            return(None)
#        # now transform this into a table like structure
#        # which is a list of rows
#        # the first one containing the colnames
#        # the following rows the data
#
#
#        # sort the columns heads alphanumerically (after the first one)
#        # no confusion about the order can occur
#        name = list(ss.keys())[0]
#        sl = ss[name]
#        additional_colnames = []
#        for dic in sl:
#            for subdic in dic:
#                if type(dic) == builtins.dict and dic[subdic]:
#                    colnames_for_one_row = list(dic[subdic].keys())
#                    additional_colnames = list(set(additional_colnames+colnames_for_one_row))
#
#        additional_colnames = sorted(additional_colnames)
#        
#        # find the entries in the right order and add them to the row
#        colnames=[name.replace("_", " ")] + additional_colnames # should be the alternative section title here as well?
#
#        rows=[colnames]
#
#        for dic in sl:
#            for subdic in dic:
#                row = [subdic]
#                for col in additional_colnames:
#                    if type(dic) == builtins.dict and dic[subdic] and col in dic[subdic].keys():
#                        row.append(dic[subdic][col])
#                    else:
#                        row.append(None)
#                
#            rows.append(row)
#
#        # return it in as a data frame with similar access function as the R counterpart
#        df = DataFrame(rows)
#        df.remove_empty_columns()
#        return df
    def has_key(self,target_key):
        df=self.df
        keylist=flatten([key for key in  df.get_column("key") if key])
        return(target_key in keylist)
        
    def find_keys_used_in_key(self,target_key):
        # fixme:
        # this should live in a new class . I propose: ModelVars
        
        # the component keys can not be used in general since 
        # they are used only for the components...
        if not(self.has_key(target_key)):
            raise(Exception("The model:"+str(self.name)+" has no key: "+str(target_key)))
        #find the symbol or expression related to target_key
        df=self.df
        keys=df.get_column("key")
        i=keys.index(target_key)
        names=df.get_column("name")
        name=names[keys.index(target_key)]
        #fixme :
        # the following check should be made on model initialization for all keys found
        keys.remove(target_key)
        if target_key in keys: #still after one removal 
            raise(Exception("the key: "+str(target_key)+" has been used at least twice"))
        # now get all the varnames that are part of the expr
        var_names=self.find_all_variables_in_dependency_tree_of_expr(name)
        res=set([])
        for vn in var_names:
            key=self.get_key_of_var_name_or_None(vn)
            if key:
                res.update([key]) #note the list brackets wich prevent 
        return(res)

    def find_keys_or_symbols_used_in_key(self,target_key):
        # fixme:
        # this should live in a new class . I propose: ModelVars
        
        # the component keys can not be used in general since 
        # they are used only for the components...
        if not(self.has_key(target_key)):
            raise(Exception("The model:"+str(self.name)+" has no key: "+str(target_key)))
        #find the symbol or expression related to target_key
        df=self.df
        keys=df.get_column("key")
        i=keys.index(target_key)
        names=df.get_column("name")
        name=names[keys.index(target_key)]
        #fixme :
        # the following check should be made on model initialization for all keys found
        keys.remove(target_key)
        #
        if target_key in keys: #still after one removal 
            raise(Exception("the key: "+str(target_key)+" has been used at least twice"))
        # now get all the varnames that are part of the expr
        var_names=self.find_all_variables_in_dependency_tree_of_expr(name)
        res=set([])
        for vn in var_names:
            key=self.get_key_of_var_name_or_None(vn)
            if key:
                res.update([key]) #note the list brackets wich prevent 
            else:
                res.update([vn])
        return(res)
    
    def get_key_of_var_name_or_None(self,var_name):    
        df=self.df
        names=df.get_column("name")
        keys=df.get_column("key")
        rn=names.index(var_name)
        return(keys[rn])

    def get_expr_str_rhs_or_None(self,var_name):
        # fixme:
        # this should live in a new class . I propose: ModelVars
        
        # the method finds the unevaluated expression in self.df
        names=self.df.get_column("name")
        exprs=self.df.get_column("exprs")
        rn=names.index(var_name)
        expr_str=exprs[rn] #result could be None
        if expr_str:
            rhs= expr_str.split("=", 1)[1].strip()
            return(rhs)
        else:
            return(None)
        

        
        
    def find_all_variables_in_dependency_tree_of_expr(self,var_name):
        # fixme:
        # this should live in a new class . I propose: ModelVars
        expr_str=self.get_expr_str_rhs_or_None(var_name)
        names=set()
        if expr_str:
            expr=sympify(expr_str, locals=self.symbols_by_type)
            atoms=expr.free_symbols
            if len(atoms)>0:
                for atom in atoms:
                    names.update([str(atom)]) #note the list bracket that prevent the string from beeing treated as a list of characters
                    names.update(self.find_all_variables_in_dependency_tree_of_expr(str(atom)))
        return(names)












    def section_vars(self, section_name):
        #prevent side effects on self.df
        complete_df = deepcopy(self.df)
        new_rows = []
        new_rows.append(complete_df.head)
        for index, row in enumerate(complete_df.rows):
            if complete_df[index, 'category'] == section_name:
                new_rows.append(row)

        new_df = DataFrame(new_rows)
        new_df.remove_column('category')
        new_df.remove_empty_columns()
        return new_df
            
#def categories():  
#    dic={
#            'VegComponents':{
#               desc:
#               subcategories: ["state_vector","scalar_func_phot","part_coeff","cyc_matrix","resp_matrix","C_content", "state_vector_derivative"]
#            },
#            'SoilComponents':{
#               desc:
#               subcategories: ["state_vector","input_vector","trans_op","decomp_op_nonlin","decomp_op_lin", "env_eff_mult", "state_vector_derivative"]
#            },
#            'Temperature':{
#		        desc:"Parameters and variables related to temperature",
#		        subcategories:["soil_temperature","air_temperature", "Q_10", "func_temp"]
#            },
#            'func_temp':{
#                desc: "Empiric? function of temperature"
#            },
#            'func_soil_moist':{
#                desc: "Empiric? function of soil moisture"
#            },
#            'env_scalar':{
#                desc: "Empiric? function of soil moisture"
#            },
#            'Vegetation':{
#		        desc:"Vegetation pools or components",
#		        subcategories:["roots","foliage","wood", "sapwood"]
#            },
#            'partitioning':{
#                desc: "Fractions, coeficients and functions that describe partitioning of NPP"
#                subcategories:["part_foliage","part_wood","part_roots","part_reproduction", "part_defense"]
#            },
#            'cycling':{
#                desc: "Rates, coeficients and functions that describe the cycling (turnover) of pools or components"
#                subcategories:["cyc_foliage","cyc_wood","cyc_roots"]
#            },
#            'N_depend_NPP':{
#                desc: "Function that represents NPP dependance on nitrogen"
#            },
#            'root_N':{
#                desc: "Nitrogen in roots"
#            },
#            'leaf_P_C_ratio':{
#                desc: "Foliar P:C ratio"
#            },
#            'nutrient_uptake':{
#                desc: ""
#            },
#            'leaf_P':{
#                desc: "Foliar Phosphorus"
#            },
#            'leaf_P':{
#                desc: "Foliar Phosphorus"
#            },
#            'wood_N':{
#                desc: "Wood Nitrogen"
#            },
#            'leaf_N':{
#                desc: "Foliar Nitrogen"
#            },
#            'reproductive_N_C_ratio':{
#                desc: "Reproductive propagules N:C ratio"
#            },
#            'root_N_C_ratio':{
#                desc: "Root N:C ratio"
#            },
#            'wood_N_C_ratio':{
#                desc: "Wood N:C ratio"
#            },
#            'leaf_N_C_ratio':{
#                desc: "Foliar N:C ratio"
#            },
#            'leaf_N_C_ratio_crit':{
#                desc: "Foliar N:C ratio below which production is N-limited"
#            },
#            'stand_age':{
#                desc: ""
#            },
#            'photosynthesis':{
#                desc: "Parameters and variables used to estimate photosynthesis"
#                subcategories:["IPAR","PAR","light_ext","LAI"]
#            },
#            'LAI':{
#                desc: "Leaf area index: leaf area / ?"
#            },
#            'light_use_eff':{
#                desc: "Light use (utilization) efficiency. Also, PAR use efficiency"
#            },
#            'PAR':{
#                desc: "Photosynthetically Active Radiation"
#            },
#            'IPAR':{
#                desc: "Incident or intercepted photosynthetically active radiation"
#            },
#            'APAR':{
#                desc: "Absorbed photosynthetically active radiation"
#            },
#            'NPP':{
#                desc: "Net Primary Productivity"
#            },
#            'GPP':{
#                desc: "Gross Primary Productivity"
#            },
#            'root_N':{
#                desc: "Gross Primary Productivity"
#            },
#            'roots':{
#                desc:"Nitrogen content of fine roots",
#                subcategories:["fine_roots","woody_roots"]
#            }, 
#            'foliage':{
#                desc:"Foliage component or pool",
#                subcategories:["canopy_area"]
#            },
#            'respiration':{
#                desc:"Plant components respiration",
#                subcategories:[""]
#            },
#            'Soil':{
#                desc:"bla ...",
#		        subcategories:["soil_temperature","soil_moisture","soil_ph","soil_decomposition_speed", "soil_sand"]
#            }
#            } 
#    return(dic)
#
#def available_keys( 
#        dic=categories()
#        # find all the subcatogories
#   )	
# test available keys
# expected result: Temperature,soil_temperature,vegetation_temperature,Vegatation,roots,foiliage,wood,fine_roots,woody_roots
# example task 1:
# per yaml file find all symbols that describe carbon content in roots!
# test:
#   fixture yaml snippet:
#        ...
#        ...   
#           key: "foliage"
#       - C_r: 
#           desc: Carbon in fine roots 
#           key: "fine_roots"
#        ...
#        ...   
#       - C_wr
#           desc: Carbon in woody roots 
#           key: "woody_roots"
#
#  result: [C_r,C_wr]  


# example task 2:
# per yaml file look for Fv and find out how many levels of substitution are necessary to reach a variable
# related to foliage.
# test:
#   fixture yaml snippet:
#        ...
#        ...   
#        - C_f:
#           desc: Carbon in foliage
#           key: "foliage"
#        ...
#        - x: 
#            exprs: "x=Matrix(3,1,[C_f, C_r, C_w])"
#            desc: vector of states for vegetation
#        ...
#        ...   
#        - f_v: 
#            exprs: "fv = u*b + A*x"
#            desc: the righthandside of the ode
#            unit: "kg/s"
#  result:2
#  The result would be reached in 2 steps:
#  - first find a symbol with key foliage ->C_f
#  - count the number of substitutions (x=Matrix[..C_f,..]) and f=A*x+...) ->2 substitutions
#
# example task 3:
# per yaml file look for Fv and find out how many levels of substitution are necessary to reach a variable
# related to Vegetation.
# Since Vegetation has subcatogories these have to be found first.
# For the same reasons the answer is no longer a single number but a list containing the depth for every symbol
# belonging to one of the subcategories of Vegetation 
# test:
#   fixture yaml snippet:
#        ...
#        ...   
#        - C_f:
#           desc: Carbon in foliage
#           key: "foliage"
#        ...
#        - x: 
#            exprs: "x=Matrix(3,1,[C_f, C_r, C_w])"
#            desc: vector of states for vegetation
#        ...
#        ...   
#        - f_v: 
#            exprs: "fv = u*b + A*x"
#            desc: the righthandside of the ode
#            unit: "kg/s"
#
#  result:[2,2,2]
#  The result would be reached in 2 steps:
#  - first find symbols with key in the subcategories of Vegetation which are [foliage ->C_f,wood->C_w,and roots ->C_r]
#  - count the number of substitutions for each of them 
#  e.g.:
#  x=Matrix[..C_f,..]) and f=A*x+...) ->2 substitutions
#  x=Matrix[..,..C_r]) and f=A*x+...) ->2 substitutions
#  ...

# example task 3:
# How are the symbols describing Soil related to the symbols 
# describing Temperature, more precisely: how many substitutions
# are needed to reach a Soil symbol by looking at an expression i # for Temperature or vice versa?

# test:
#   fixture yaml snippet:
#        ...
#        ...   
#        -T_s:
#           desc: Temperature in soil
#           key:  "soil_temperature" 
#        ...
#        ...   
#        -g:
#           desc: bla
#           key:  "something_unrelated" 
#           exprs: T_s*b
#
#        ...
#        ...   
#        -k_s:
#           desc: turnover rate in soil
#           exprs: g*T_m
#           key:  "soil_decomposition_speed" 
#         
# result:{k_s:{T_s:2,T_s:{T_s:0},T_m:1}
#   explain how the entry T_s:2 would be reached by the alg:  
#   - decide if you want to start from the soil or temperature side
#     we assume to start at the soil end 
#   - find all subcatogories of Soil :
#      ->l= ["soil_temperature","soil_moisture","soil_ph","soil_decomposition_speed"]
#     for sc in l:
#         find all expressions beloning to sc
#         ->expression_list=[k_s,....]
#         for e in expression_list:    
#             ...
#             e.g e=k_s
#             # check if k_s is a decendant of Temperature  
              #  (not the case)
#             vars=[g,r]
#             # first try if g or r belong to some subcategorie of Temperature
#             # (this does not happen here) 
#             for v in vars:
#                 kv=Key(v)
#                 e.g. v=g -> kv="something_unrelated"               
#                 as =ancestors("something_unrelated")
#                 if T is in ancestors: 
#                     result=1    
#                 ....
#             # now decompose g and r further
#             g=Ts*b    
#             ...
#             for Ts we find T as ancestor
#             -> k_s is 2 substitutions distant from T_s
#             ...
#             e.g e=T_s (because soil_temperature is a subcategory of Soil)
#             # check if T_s is a decendant  
#             vars=[g,r]
#             # first try if g or r belong to some subcategory of Temperature
#               this is the case 
#               so the distance is 0
#  T_m:1 
#  same procedure but only one subs needed since T_m is directly contained in k_s expression

 
 
