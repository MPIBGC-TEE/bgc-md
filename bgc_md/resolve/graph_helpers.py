
from typing import List,Set,Tuple
#import contextlib
from ..helpers import working_directory
import sys
from pathlib import Path
from functools import lru_cache,reduce
from copy import deepcopy
#from . import MvarsAndComputers as mvars
#from .MvarsAndComputers import Mvars as myMvars
#from .MvarsAndComputers import Computers as myComputers
from testinfrastructure.helpers import pe
#from .IndexedSet import IndexedSet
from .MVar import MVar
from matplotlib.colors import CSS4_COLORS,BASE_COLORS,TABLEAU_COLORS
from pygraphviz import *
import networkx as nx
from typing import List,Set,Tuple
# infrastructure to compute the graph that is used to compute source sets for a given set of Mvars
def powerlist(S):
    # We do not want to rely on the set union operation (which necessiates the creation of sets
    # in the first place which is a O(n^2) operation)
    # So we avoid the manyfold occurence of a sublit in the  resultlist 'manually' by not creating
    # it in the first place
    # we start with an empty list
    initial=[[]]
    # and gradually enhance it
    return reduce(lambda acc,el:acc+[ subset +[el] for subset in acc],S,initial)

def node_2_string(node):
    return '{'+",".join([v.name for v in node])+'}'

def nodes_2_string(node):
    return '[ '+",".join([node_2_string(n) for n in node])+' ]'

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


def update_step(G,extendable_nodes,allMvars,allComputers):
    
    # update the Graph by looking at the new_nodes and adding all their possible predecessors as new nodes 
    # The nodes representing one-element sets have been already treated by the first step 
    # (Thein predecessors found by their computers)
    # now we have to find the predecessors of the sets with more than one element
    # we do this by looking at the tensor product of the predecessor-sets  of the elements
    G=deepcopy(G)
    present_nodes=frozenset(G.nodes)
    present_edges=frozenset(G.edges)
    new_global_nodes=frozenset({})
    for n in extendable_nodes:
        print('\nextendable node:'+node_2_string(n))
        # it should actually be possible to infer the nodes that can 
        # be computed from other nodes from the graph G alone
        # Up to now we only use the computability of mvars
        # Actually the graph could in later stages also provide information
        # about the computablitiy of sets (which is its main purpose after all)
        # but up to now we do not use this knowledge for constructing it.
        pns=direct_predecessor_nodes(n,allMvars,allComputers) # this function should also return the computers it used 
        for pn in pns:
            G.add_node(pn) 
            e=(pn,n)
            #if not(e in present_edges):
            if not(e in G.edges()):
                print('new_edge:'+edge_2_string(e))
                G.add_edge(pn,n) 
        print('direct_predecessor_nodes:'+nodes_2_string(pns))
        arn=present_nodes.intersection(pns)
        print('allready known:'+nodes_2_string(arn))
        new_local_nodes= pns.difference(arn)
        new_global_nodes=new_global_nodes.union(new_local_nodes)
        print('new_local_node:'+nodes_2_string(new_global_nodes))

    print('new_global_nodes:'+nodes_2_string(new_global_nodes))
    #extendable_nodes=new_nodes
    #new_minimal_nodes=new_minimal_nodes#.difference(present_nodes)
    return (G,new_global_nodes)

def updated_Graph(G,extendable_nodes,allMvars,allComputers,counter=0):
    G_new,extendable_nodes_new=update_step(G,extendable_nodes,allMvars,allComputers)
    if len(extendable_nodes)==0: 
        return (G,extendable_nodes)
    else:
        draw_Graph_png(G,"updated_Graph"+str(counter))
        return updated_Graph(G_new,extendable_nodes_new,allMvars,allComputers,counter+1)

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

def sparse_powerset_Graph(allMvars,allComputers):
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
    A.add_nodes_from([v.name for v in allMvars])
    cols=['blue','red','green','orange'] 
    for v in allMvars:
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

def minimal_startnodes_for_single_var(spg:nx.Graph,targetVar:MVar):
    ''' spg is a sparse powerset Graph, which meeans that it only contains all one element'''
    # We first create a graph with the direction of the edges reversed
    targetSet=frozenset({targetVar})
    GR=spg.reverse()
    res=[p for p in nx.all_pairs_shortest_path(GR) if p[0]==targetSet]
    all_possible_startnodes=frozenset([n for n in res[0][1].keys()])
    print("all_possible_startnodes for",node_2_string(targetSet),[node_2_string(n) for n in all_possible_startnodes])
    minimal_startnodes=remove_supersets(all_possible_startnodes)
    minimal_startnodes=[n for n in filter(lambda n: not(n.issuperset(targetSet)),minimal_startnodes)]
    return frozenset(minimal_startnodes)
    

def minimal_startnodes_for_node(spg:nx.Graph,target:Set[MVar]):
    raise(Exception('not implemented yet. Idea: build the cartesian_union of the single variable sources and then remove all occurences of supersets of elements of the powerset of the targetnode') )
    # With the given graph we can also quite quickly compute possible sources for a given traget set of 
    # now we remove all supersets from 
    #minimal_startnodes2=remove_supersets(all_possible_startnodes2)
    #print("minimal_startnodes for",node_2_string(target2),[node_2_string(n) for n in minimal_startnodes2 if not(target2.issubset(n))])
    # more than one variable (additionally we could cache the results
