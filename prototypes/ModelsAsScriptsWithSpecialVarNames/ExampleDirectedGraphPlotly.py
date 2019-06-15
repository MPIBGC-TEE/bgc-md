import plotly.offline as py 
import plotly.graph_objs as go 
from copy import copy
traces=[]
annotations=[]
traces.append(go.Scatter( 
     x=[1, 2, 2, 1]
    ,y=[3, 4, 3, 4] 
    ,mode='markers+text'
    ,text=["a",'b','c','d']
    ,hovertext=['variable a is cool','variable b is cool too','variable c is cooler','variable d is coolest']
    #,textposition='bottom center' #top center...
    ,marker=dict(size=[40, 30, 200, 50])
))
def add_arrow(annotations,source_x,source_y,target_x,target_y):
    a_new=copy(annotations)
    a_new.append(
        dict(
                ax=source_x, ay=source_y, axref='x', ayref='y'
                ,x=target_x, y=target_y, xref='x', yref='y'
                ,showarrow=True
                ,text='arrow_text'
                #,arrowhead=7
        )
    )
    return a_new

#            ))
annotations=add_arrow(annotations,1,3,2,4)
annotations=add_arrow(annotations,1,4,2,4)
# eval("dict(ax=2, ay=3, axref='x', ayref='y', x=1, y=4, xref='x', yref='y')")
fig = go.Figure(
     data=traces
    ,layout=go.Layout(
        # the annotation are used to make the arrowheads
        annotations=annotations
        ,shapes=[
            # filled Triangle could be molded into an arrowhead
            {
                'type': 'path',
                'path': ' M 1 1 L 1 3 L 4 1 Z',
                'fillcolor': 'rgba(44, 160, 101, 0.5)',
                'line': {
                    'color': 'rgb(44, 160, 101)',
                },
            }
            ]
    )
) 
py.plot(fig)
