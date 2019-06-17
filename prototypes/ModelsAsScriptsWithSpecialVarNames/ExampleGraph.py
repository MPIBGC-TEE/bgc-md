import matplotlib.pyplot as plt
from bgc_md.resolve.helpers import  get3, computable_mvar_names
from bgc_md.resolve.graph_helpers import ( 
     direct_predecessor_nodes
    ,minimal_startnodes_for_single_var
    ,minimal_startnodes_for_node
    ,update_step
    ,remove_supersets
    ,node_2_string
    ,nodes_2_string
    ,edge_2_string
    ,cartesian_union
    ,create_multigraph
    ,draw_multigraph_graphviz
    ,draw_multigraph_matplotlib
    ,draw_multigraph_plotly
    ,sparse_powerset_Graph
    ,draw_Graph_png
    ,powerlist
)
from matplotlib.colors import CSS4_COLORS,BASE_COLORS,TABLEAU_COLORS
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer
from bgc_md.resolve.functions import srm_from_B_u_tens
from bgc_md.resolve.IndexedSet import IndexedSet
from copy import copy,deepcopy
import networkx as nx
from pygraphviz import *
from unittest import TestCase
from copy import copy
from functools import reduce

allMvars=IndexedSet({
    MVar('a',description= """ a varible we assume to be given """)
    ,MVar('b')
    ,MVar('c')
    ,MVar('d')
    ,MVar('e')
    ,MVar('f') 
    ,MVar('g')
    ,MVar('h')
    ,MVar('i')
})
allComputers=IndexedSet({
    Computer(
        'a(i)'
        ,func=lambda e: e**2
        ,description="""computes f from e"""
    )
    ,Computer(
        'b(c,d)'
        ,func=lambda c,d: 3
        ,description="""computes b from c and d"""
    )
    ,Computer(
        'b(e,f)'
        ,func=lambda c,d: 3
        ,description="""computes b from e and f"""
    )
    ,Computer(
        'c(b)'
        ,func=lambda b:2*b
        ,description="""computes c from b"""
    )
    ,Computer(
        'd(b)'
        ,func=lambda b:5 # we make it consistent but atually the result is not important for the test
        ,description="""computes d from b """
    )
    ,Computer(
        'd(g,h)'
        ,func=lambda g,h:5
        ,description="""computes d from g  and h """
    )
    ,Computer(
        'e(b)'
        ,func=lambda b: 4
        ,description="""computes e from b"""
    )
    ,Computer(
        'f(b)'
        ,func=lambda b: 4
        ,description="""computes f from b"""
    )
})

G=create_multigraph(allMvars,allComputers)
colordict=TABLEAU_COLORS
color_names=[n for n in colordict.keys()]
computer_colors={c.name:color_names[i] for i,c in enumerate(allComputers)}
