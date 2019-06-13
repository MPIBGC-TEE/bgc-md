import matplotlib.pyplot as plt
from bgc_md.resolve.helpers import  get3, computable_mvar_names,direct_predecessor_nodes,remove_supersets,update,node_2_string,edge_2_string,cartesian_union,draw_multigraph,powerset_Graph,draw_Graph_png
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer
from bgc_md.resolve.functions import srm_from_B_u_tens
from bgc_md.resolve.IndexedSet import IndexedSet
from copy import copy,deepcopy
import networkx as nx
from pygraphviz import *


# we produce a small set of Mvars with a loop (b could be something like a CompartmentalSystem that can be computed # in different ways and can also be queried about its constituents.
myMvars=IndexedSet({
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
myComputers=IndexedSet({
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
# only for visualization draw the connections of the mvars via computers
# note that this is not a graph we can query for connectivity
draw_multigraph(myMvars,myComputers)

# Now we build the directed Graph we can use to compute connectivity
# the Nodes are sets of Mvars (elemenst of the powerset of all Mvars)
# and a connection between two sets indicates computability of the targes set from 
# the source set.
# The complete graph would contain all elements of the powerset of allMvars and all
# possible connections, which is prohibitively expensive.
# Instead we will compute a subgraph where we start with one element sets as targets
# and infer the predecessors of those sets and then the predecessors of the predecessors and so on until we do not find new nodes=start_sets.

G=powerset_Graph(myMvars,myComputers)
draw_Graph_png(G,'test')    
# After the graph has been computed we can use it
# to infer computability of all Mvars
# We first create a graph with the direction of the edges reversed

#nx.independentSets? for directed graphs 
 
GR=G.reverse()

target=frozenset({myMvars['b']})
res=[p for p in nx.all_pairs_shortest_path(GR) if p[0]==target]
all_possible_startnodes=frozenset([n for n in res[0][1].keys()])
print("all_possible_startnodes for",node_2_string(target),[node_2_string(n) for n in all_possible_startnodes])
minimal_startnodes=remove_supersets(all_possible_startnodes)
print("minimal_startnodes for",node_2_string(target),[node_2_string(n) for n in minimal_startnodes if not(target.issubset(n))])

target2=frozenset({myMvars['a']})
res2=[p for p in nx.all_pairs_shortest_path(GR) if p[0]==target2]
all_possible_startnodes2=frozenset([n for n in res2[0][1].keys()])
print("all_possible_startnodes for",node_2_string(target2),[node_2_string(n) for n in all_possible_startnodes2])
minimal_startnodes2=remove_supersets(all_possible_startnodes2)
print("minimal_startnodes for",node_2_string(target2),[node_2_string(n) for n in minimal_startnodes2 if not(target2.issubset(n))])

# With the given graph we can also quite quickly compute possible sources for a given traget set of 
# more than one variable (additionally we could cache the results
#print([node_2_string(n) for n in cartesian_union([minimal_startnodes,minimal_startnodes2])])
print("minimal_startnodes for ",node_2_string(target.union(target2)),[node_2_string(n) for n in remove_supersets(cartesian_union([minimal_startnodes,minimal_startnodes2])) if not(target2.issubset(n) or target.issubset(n) )])
 
#for p in gen:
#    print(type(p[0]))
#    print(p[0]==target) #source (the target for the original grapht
#    print(node_2_string(p[0])) #source (the target for the original grapht


#draw
#ax=plt.subplot(121)
#nx.draw(G, with_labels=True, font_weight='bold',ax=ax)
