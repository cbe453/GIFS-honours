#!~/anaconda2/bin/python

import plotly.graph_objs as go
import plotly.plotly as py
import plotly

###########################################
# generate a 3D graph based on previously computed positions, colours, shapes, etc.
# this code is a Frankenstein's monster of sorts. I smashed two examples from Plotly
# together to make this work!
def graphIt(graph, pos, outFile, shapes, labels, group):
	Xn = [pos[k][0] for k in graph.nodes()]
	Yn = [pos[k][1] for k in graph.nodes()]
	Zn = [pos[k][2] for k in graph.nodes()]
	Xe = []
	Ye = []
	Ze = []

	for e in graph.edges():
		Xe += [pos[e[0]][0],pos[e[1]][0], None]
		Ye += [pos[e[0]][1],pos[e[1]][1], None]
		Ze += [pos[e[0]][2],pos[e[1]][2], None]
	
	trace1=go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color='black',width=1.0),
    	#text=edgeWeight, 
    	hoverinfo='none')
               
	trace2=go.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers', name='name',
    	marker=dict(symbol=shapes, size=8, color=group, #colorscale='Viridis',
    	line=dict(width=0.3)), text=labels, hoverinfo='text')
               
	axis=dict(showbackground=False, showline=False, zeroline=True, showgrid=True,
    	showticklabels=False, title='')
    	      
	layout = go.Layout(title = outFile, width=5000, height=5000,
    	showlegend=False, scene=dict(xaxis=dict(axis), yaxis=dict(axis), zaxis=dict(axis)),
    	margin=dict(t=100), hovermode='closest')

	data=[trace2, trace1]
	fig=go.Figure(data=data, layout=layout)
	
	plotly.offline.plot(fig, filename=outFile, auto_open=False)
	
	return

