import matplotlib.pyplot as plt
from bgc_md.resolve.helpers import  get3, computable_mvar_names,direct_predecessor_nodes,remove_supersets,update,node_2_string,edge_2_string,cartesian_union
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer
from bgc_md.resolve.functions import srm_from_B_u_tens
from bgc_md.resolve.IndexedSet import IndexedSet
from copy import copy,deepcopy
import networkx as nx
from pygraphviz import *
from matplotlib.colors import CSS4_COLORS,BASE_COLORS,TABLEAU_COLORS

#import igraph as ig
def draw_multigraph(myMvars,myComputers):
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
    computer_colors={c.name:color_names[i] for i,c in enumerate(myComputers)}
    A=AGraph(directed=True)
    A.node_attr['style']='filled'
    A.node_attr['shape']='circle'
    A.node_attr['fixedsize']='false'
    A.node_attr['fontcolor']='#FFFFFF'
    A.node_attr['color']='black'
    A.add_nodes_from([v.name for v in myMvars])
    cols=['blue','red','green','orange'] 
    for v in myMvars:
        for c in v.computers(myComputers):
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

Graphs=dict()
G=nx.DiGraph()
# add all Vvars
G.add_nodes_from([frozenset({v}) for v in myMvars])
draw_Graph_png(G,"PowersetSubGraph_"+str(0))
Graphs[0]=deepcopy(G)
# add the connections implied by the computers
new_nodes=[]
present_nodes=G.nodes
for v in myMvars:
    v_comps=v.computers(myComputers)
    for c in v_comps:
        ans=c.arg_set(myMvars)
        # the nodes already present would  be ignored anyway but we want to 
        # know them to save time in the next step
        if not(ans in present_nodes):
            new_nodes.append(ans)
            G.add_node(ans) 
        G.add_edge(ans,frozenset({v}),computers=v_comps) 

extendable_nodes=new_nodes
draw_Graph_png(G,"PowersetSubGraph_"+str(1))
Graphs[1]=deepcopy(G)


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

print(GraphsEqual(Graphs[0],Graphs[1]))
#while len(extendable_nodes)>0: 
i=1
while not(GraphsEqual(Graphs[i],Graphs[i-1])):
    i+=1 
    print(i)
    G,extendable_nodes=update(G,extendable_nodes,myMvars,myComputers)
    Graphs[i]=G
    draw_Graph_png(G,"PowersetSubGraph_"+str(i))
    
# After the graph has been computed we can use it
# to infer computability of all Mvars
# We first create a graph with the direction of the edges reversed
# 
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
