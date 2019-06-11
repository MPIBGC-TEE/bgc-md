import os
from typing import List,Set,Tuple
#import contextlib
from ..helpers import working_directory
import sys
from pathlib import Path
from functools import lru_cache
from copy import deepcopy
from testinfrastructure.helpers import pe
#from . import MvarsAndComputers as mvars
from .MvarsAndComputers import Mvars as myMvars
from .MvarsAndComputers import Computers as myComputers
from .IndexedSet import IndexedSet
from .MVar import MVar
from bgc_md.reports import defaults
from matplotlib.colors import CSS4_COLORS,BASE_COLORS,TABLEAU_COLORS
from pygraphviz import *
import networkx as nx

srcFileName="source.py"
d=defaults() 
modelFolderName=d['paths']['new_models_path']
special_var_string="special_vars"
def srcDirPath(model_id):
    return Path(modelFolderName).joinpath(model_id)

def srcPath(model_id):
    p=srcDirPath(model_id).joinpath(srcFileName)
    pe('p',locals())
    return p

def populated_namespace_from_path(p:Path):
    # this is the proxy function 
    # It will compile the user code and populate a sandbox by executing the code  
    

    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    
    # prepare the execution environment
    # and execute in the directory since the model might need input files and 
    # also other python code in the same directory
    with working_directory(p.parent):
        exec(code,gns)
    return gns

def populated_namespace(model_id):
    # this is the proxy function 
    # It will compile the user code and populate a sandbox by executing the code  
    
    # find the user code
    p=srcPath(model_id)

    with p.open() as f:
        code= compile(f.read(),p,mode='exec')
        #code= f.read()
    gns={}
    
    # prepare the execution environment
    # and execute in the directory since the model might need input files and 
    # also other python code
    with working_directory(srcDirPath(model_id)):
        exec(code,gns)
    return gns

def get_bgc(var_name:str,model_id:str):
    return get3(var_name,myMvars,myComputers,model_id)

def is_computable_bgc(var_name:str,model_id:str):
    return myMvars[var_name].is_computable(myMvars,myComputers,names_of_available_mvars(model_id))
    
def get3(var_name:str,allMvars,allComputers,model_id:str):
    # execute the model code
    #gns=populated_namespace(model_id)
    
    #mvar=[var for var in allMvars if var.name==var_name][0]
    #special_vars=gns[special_var_string] 
    mvar=allMvars[var_name]
    return mvar(allMvars,allComputers,special_vars(model_id))
    
def special_vars(model_id):
    gns=populated_namespace(model_id)
    return gns[special_var_string] 

def names_of_available_mvars(model_id):
    return [str(k) for k in special_vars(model_id).keys()]



@lru_cache(maxsize=None) 
def directly_computable_mvar_names(
        allMvars:IndexedSet
        ,allComputers:IndexedSet
        ,names_of_available_mvars:frozenset
    )->frozenset:
    # find the computers that have a source_set contained in the available_set
    return frozenset([c.target_name for c in allComputers if c.arg_name_set.issubset(names_of_available_mvars)])

@lru_cache(maxsize=None) 
def computable_mvar_names(
        allMvars:IndexedSet
        ,allComputers:IndexedSet
        ,names_of_available_mvars:frozenset
    )->frozenset:
    # bottom up approach: repeatedly compute all directly (in the next step) reachable Mvars 
    # and use the enriched set for the next iteration until the set stays constant 
    dcNames=directly_computable_mvar_names(allMvars,allComputers,names_of_available_mvars)
    
    if dcNames.issubset(names_of_available_mvars):
        return frozenset([allMvars[name] for name in names_of_available_mvars])
    else:
        return computable_mvar_names(allMvars,allComputers,names_of_available_mvars.union(dcNames))

# infrastructure to compute the graph that is used to compute source sets for a given set of Mvars
def node_2_string(node):
    return '{'+",".join([v.name for v in node])+'}'

def edge_2_string(e):
    return "("+node_2_string(e[0])+','+node_2_string(e[1])+')'

def cartesian_product(l:List[Set])->Set[Tuple]:
    left_tupels=frozenset([tuple(el) for el in l[0]])
    if len(l)==1:
        return left_tupels
    else:
        right_tupels=cartesian_product(l[1:])
        return frozenset([lt+rt for lt in left_tupels for  rt in right_tupels ])

def cartesian_union(l:List[Set])->Set[Set]:
    #pe('l',locals())
    return frozenset([frozenset(t) for t in cartesian_product(l)])

def remove_supersets_once(sets):
    key_func=lambda s:len(s)
    sets=sorted(sets,key=key_func)
    #print('Startnodes:')
    #print([node_2_string(val)  for val in sets])
    #print('##############################:')

    minimal_sets=[]
    for n in sets:
        if not(any([m.issubset(n) for m in minimal_sets])):
            minimal_sets.append(n)

    return frozenset(minimal_sets)

def remove_supersets(sets):
    new_nodes=remove_supersets_once(sets)
    
    if new_nodes==sets:
        return(new_nodes)
    else:
        return remove_supersets(new_nodes)
    
def direct_predecessor_nodes(node:Set[MVar],allMvars,allComputers)->Set[Set[str]]:
    # assume that we want to compute a set of MVars (a node in out graph) from other sets of Mvars
    # let s_a be the set of nodes from which we can reach the set {a} (where a is a MVar} 
    # and s_b the set of nodes from which we can reach the node {b} (where b is an Mvar
    # to reach the node set {a,b} we can combine any startnode from s_a with any startnode from s_b
    # in fact we can reach {a,b} from all nodes in the set {s: s=n_a v n_b for na in sa v {a}  for nb in sb v {b} }
    # we call this set the 'cartesian_union(A,B) with  A=s_a v {a}  and B=s_b v {b} 
    # This can be generalized to an arbitrary list of sets. We build the cartesian product of the sets A,B,... and then
    # transform every tupel of the product to a set (thereby removing the duplicates and order)
    res=cartesian_union(
        [ {frozenset({v})}.union(v.arg_set_set(allMvars,allComputers)) for v in node]
    )
    #pe('node',locals())

    # note that the cartesian product contains the original node
    # we remove all nodes that are just supersets of it
    # and afterwards the node itself
    #return res.difference(frozenset({node}))
    return remove_supersets(res).difference(frozenset({node}))

def update(G,extendable_nodes,allMvars,allComputers):
    ## fixme
    ## This function should become obsolete as soon as update step is well tested
    print("##############################")
    print("extendable_nodes")
    print([node_2_string(n) for n in extendable_nodes])
    
    # update the Graph by looking at the new_nodes and adding all their possible predecessors as new nodes 
    # The nodes representing one-element sets have been already treated by the first step 
    # (Thein predecessors found by their computers)
    # now we have to find the predecessors of the sets with more than one element
    # we do this by looking at the tensor product of the predecessor-sets  of the elements
    G=deepcopy(G)
    present_nodes=frozenset(G.nodes)
    present_edges=frozenset(G.edges)
    new_minimal_nodes=frozenset({})
    for n in extendable_nodes:
        # it should actually be possible to infer the nodes that can 
        # be computed from other nodes from the graph G alone
        # Up to now we only use the computability of mvars
        # Actually the graph could in later stages also provide information
        # about the computablitiy of sets (which is its main purpose after all)
        # but up to now we do not use this knowledge for constructing it.
        pns=direct_predecessor_nodes(n,allMvars,allComputers) # this function should also return the computers it used 
        print("n="+node_2_string(n))
        print("predecessors="+','.join([node_2_string(n) for n in pns]))
        new_minimal_nodes=new_minimal_nodes.union(pns.difference(present_nodes))

        for pn in new_minimal_nodes:
            G.add_node(pn) 
            e=(pn,n)
            if not(e in present_edges):
                G.add_edge(pn,n) 
    #extendable_nodes=new_nodes
    #new_minimal_nodes=new_minimal_nodes#.difference(present_nodes)
    print("new_minimal_nodes="+','.join([node_2_string(n) for n in new_minimal_nodes]))
    return (G,new_minimal_nodes)

def update_step(G,extendable_nodes,allMvars,allComputers):
    
    # update the Graph by looking at the new_nodes and adding all their possible predecessors as new nodes 
    # The nodes representing one-element sets have been already treated by the first step 
    # (Thein predecessors found by their computers)
    # now we have to find the predecessors of the sets with more than one element
    # we do this by looking at the tensor product of the predecessor-sets  of the elements
    G=deepcopy(G)
    present_nodes=frozenset(G.nodes)
    present_edges=frozenset(G.edges)
    new_minimal_nodes=frozenset({})
    for n in extendable_nodes:
        # it should actually be possible to infer the nodes that can 
        # be computed from other nodes from the graph G alone
        # Up to now we only use the computability of mvars
        # Actually the graph could in later stages also provide information
        # about the computablitiy of sets (which is its main purpose after all)
        # but up to now we do not use this knowledge for constructing it.
        pns=direct_predecessor_nodes(n,allMvars,allComputers) # this function should also return the computers it used 
        new_minimal_nodes=new_minimal_nodes.union(pns.difference(present_nodes))

        for pn in new_minimal_nodes:
            G.add_node(pn) 
            e=(pn,n)
            if not(e in present_edges):
                G.add_edge(pn,n) 
    #extendable_nodes=new_nodes
    #new_minimal_nodes=new_minimal_nodes#.difference(present_nodes)
    return (G,new_minimal_nodes)

def updated_Graph(G,extendable_nodes,allMvars,allComputers):
    G_new,extendable_nodes_new=update_step(G,extendable_nodes,allMvars,allComputers)
    if len(G_new)>0: 
        return (G,extendable_nodes)
    else:
        return update_step(G_new,extendable_nodes_new,allMvars,allComputers)

def GraphsEqual(G1,G2):
    retval=True
    new_nodes=frozenset(G1.nodes).symmetric_difference(G2.nodes) 
    new_edges=frozenset(G1.edges).symmetric_difference(G2.edges)
    if len(new_nodes)>0:
        #print("##############################")
        #print("different nodes")
        #print([node_2_string(n) for n in new_nodes])
        retval=False
    if len(new_edges)>0:
        #print("different edges")
        #print([edge_2_string(e) for e in new_edges])
        retval=False
    return retval

def powerset_Graph(allMvars,allComputers):
    new_nodes=frozenset([frozenset({v}) for v in allMvars])
    G=nx.DiGraph()
    G.add_nodes_from(new_nodes)
    G_final,new_nodes=updated_Graph(G,new_nodes,allMvars,allComputers)
    # new_nodes is now empty 
    return G_final

def draw_multigraph(allMvars,allComputers):
    # build initial multigraph
    # for visualization draw the directed Multigraph with the MVars as nodes
    # unfortunately it is not useful for connectivity computations
    # since all 'edges' defined by a computer c are misleading in the sense that 
    # we need the union of all the source variables of c to go to the target Mvar of c 
    # while the arrows suggest ways from any of the arguments...
    # for visualization it would helpful to draw all arcs belonging to the same computer
    # in the same color.
    # Since we do not compute anything from this graph we actually do not need a graphlibrary
    # but can visualize it immediately with graphviz
    # We use a unique color for every computer
    #colordict=CSS4_COLORS
    colordict=TABLEAU_COLORS
    color_names=[n for n in colordict.keys()]
    computer_colors={c.name:color_names[i] for i,c in enumerate(allComputers)}
    A=AGraph(directed=True)
    A.node_attr['style']='filled'
    A.node_attr['shape']='circle'
    A.node_attr['fixedsize']='false'
    A.node_attr['fontcolor']='#FFFFFF'
    A.node_attr['color']='black'
    A.add_nodes_from([v.name for v in myMvars])
    cols=['blue','red','green','orange'] 
    for v in myMvars:
        for c in v.computers(allComputers):
            ans=c.arg_name_set
            edges=[(an,v.name)  for an in ans]
            for e in edges:
                A.add_edge(e)
                Ae=A.get_edge(e[0],e[1])
                Ae.attr['color']=colordict[computer_colors[c.name]]
    #print(A.string()) # print to screen
    A.draw('Multigraph.png',prog="circo") # draw to png using circo


def draw_Graph_png(G,file_name_trunk):
    # the next line is the standard translation 
    # We could do this using the attributes of the edges to
    # make much niceer pictures representing the different computers in different
    # colors or annotate them....
    A=nx.nx_agraph.to_agraph(G)
    A=AGraph(directed=True)
    A.node_attr['style']='filled'
    A.node_attr['shape']='rectangle'
    A.node_attr['fixedsize']='false'
    A.node_attr['fontcolor']='black'
    
    for node in G.nodes:
        A.add_node(node_2_string(node))
    for edge in G.edges:
        A.add_edge(node_2_string(edge[0]),node_2_string(edge[1]))
    #print(A.string()) # print to screen
    A.draw(file_name_trunk+'.png',prog="circo") # draw to png using circo

