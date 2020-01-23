import matplotlib.pyplot as plt
from matplotlib.colors import CSS4_COLORS,BASE_COLORS,TABLEAU_COLORS
from typing import List,Set,Tuple
#import contextlib
from ..helpers import working_directory
import sys
from pathlib import Path
from functools import lru_cache,reduce
from copy import deepcopy
from testinfrastructure.helpers import pe
from .MVar import MVar
from pygraphviz.agraph import AGraph
#from pygraphviz import *
import networkx as nx
from typing import List,Set,Tuple
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
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

def draw_multigraph_graphviz(allMvars,allComputers):
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
                Ae.attr['fontcolor']=colordict[computer_colors[c.name]]
                Ae.attr['label']=c.name
    #print(A.string()) # print to screen
    A.draw('Multigraph.svg',prog="circo") # draw using circo

def create_multigraph(allMvars,allComputers):
    G=nx.DiGraph()
    for v in allMvars:
        for c in v.computers(allComputers):
            ans=c.arg_name_set
            for an in ans:
                G.add_edge(
                     an
                    ,v.name
                    ,computer=c
                )
    return G

def draw_multigraph_matplotlib(allMvars,allComputers):
    colordict=TABLEAU_COLORS
    color_names=[n for n in colordict.keys()]
    computer_colors={c.name:color_names[i] for i,c in enumerate(allComputers)}
    G=create_multigraph(allMvars,allComputers)
    # possibly create new Graph with text nodes
    g=G
    # create a colorlist for the edges using the computer attribute 
    edgelist=[e for e in g.edges]
    computers=[g[e[0]][e[1]]['computer'] for e in edgelist]
    edge_color=[computer_colors[c.name] for c in computers]
    fig=plt.figure(figsize=(5,5))
    axes=fig.add_subplot(1,1,1)
    nx.draw_networkx(
            g
            ,edgelist=edgelist
            ,edge_color=edge_color
            ,ax=axes)
    fig.savefig("Multigraph_matplotlib.pdf")

def draw_multigraph_plotly(allMvars,allComputers):
    # fixme mm:
    # Very immature, just a bearly adapted plotly example
    # We should:
    # - draw arrowheads (ExampleDirectedGraphPlotly.py for how to do it manually)
    # - color every computer (set of edges) with the same color and put it in the legend
    # - make the computername available as hover text
    # - we could do it in 3D easily which would realy make use of the interactiv possibiliteis


    # build initial multigraph
    # for visualization draw the directed Multigraph with the MVars as nodes
    # unfortunately it is not useful for connectivity computations
    # since all 'edges' defined by a computer c are misleading in the sense that 
    # we need the union of all the source variables of c to go to the target Mvar of c 
    # while the arrows suggest ways from any of the arguments...
    # for visualization it would helpful to draw all arcs belonging to the same computer
    # in the same color.
    # Since we do not compute anything from this graph we actually use the graphlibrary
    # only for convenience we could also use graphviz directly 
    # We use a unique color for every computer
    #colordict=CSS4_COLORS
    
    #build the graph in the mathematical sense
    G=create_multigraph(allMvars,allComputers)

    # now compute a a position to the nodes
    pos_dict=nx.planar_layout(G, scale=1, center=None, dim=2)
    nx.set_node_attributes(G,pos_dict,'pos')

    colordict=TABLEAU_COLORS
    color_names=[n for n in colordict.keys()]
    computer_colors={c.name:color_names[i] for i,c in enumerate(allComputers)}
    # now plot it:
    pos=nx.get_node_attributes(G,'pos')

    #dmin=1
    #ncenter=0
    #for n in pos:
    #    x,y=pos[n]
    #    d=(x-0.5)**2+(y-0.5)**2
    #    if d<dmin:
    #        ncenter=n
    #        dmin=d 
     
    edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none', #maybe be manage to put information about the computer here
    mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            #showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            #colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            #colorbar=dict(
            #    thickness=15,
            #    title='Node Connections',
            #    xanchor='left',
            #    titleside='right'
            #),
            line=dict(width=2,color='rgb(44, 160, 101)')))
    
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='''>Network graph made with plotly,
                    very incomplete yet. It seems easier to add legends, for the computer colors, 
                    but Arrows have to be drawn manually 
                    So we would have to create a scatter plot
                    for each edge''',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    plot(fig,filename="Multigraph.html") 
    
    #py.iplot(fig, filename='networkx')

    #https://plot.ly/python/static-image-export/
    #pio.write_image(fig, 'fig1.svg')

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
    #A.draw(file_name_trunk+'.png',prog="circo") # draw to png using circo
    A.draw(file_name_trunk+'.svg',prog='circo') 

def minimal_startnodes_for_single_var(
         spg:nx.Graph
        ,targetVar:MVar
    ):
    ''' spg is a sparse powerset Graph, which meeans that it only contains all one element'''
    # We first create a graph with the direction of the edges reversed
    targetSet=frozenset({targetVar})
    GR=spg.reverse()
    res=[p for p in nx.all_pairs_shortest_path(GR) if p[0]==targetSet]
    possible_startnodes=frozenset([n for n in res[0][1].keys()])
    print("possible_startnodes for including supersets",node_2_string(targetSet),[node_2_string(n) for n in possible_startnodes])
    minimal_startnodes=remove_supersets(possible_startnodes)
    minimal_startnodes=[n for n in filter(lambda n: not(n.issuperset(targetSet)),minimal_startnodes)]
    return frozenset(minimal_startnodes)
    

def minimal_startnodes_for_node(
         spg:nx.Graph
        ,targetNode:Set[MVar]
    ):
    single_sets=[
            minimal_startnodes_for_single_var(spg,var) for var in targetNode
    ]
    possible_startnodes=cartesian_union(single_sets)
    minimal_startnodes=remove_supersets(possible_startnodes)
    return frozenset(minimal_startnodes)
    
    def filter_func(n):
        # remove every set that contains one of the variables we are looking for ...
        return not(any([ (v in n) for v in targetNode]))

    minimal_startnodes=[n for n in filter(filter_func,minimal_startnodes)]
