import networkx as nx
import igraph as ig
import matplotlib.pyplot as plt
G=nx.DiGraph()

n1=frozenset({'g'})
n2=frozenset({'a,b'})
n3=frozenset({'c,d'})
G.add_nodes_from([n1,n2,n3])
G.add_edges_from([
     (n2,n1,{'computers':frozenset({'g(a,b)'})})    
    ,(n3,n1,{'computers':frozenset({'g(c,d)'})})    
])

