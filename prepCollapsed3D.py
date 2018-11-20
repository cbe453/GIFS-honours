#!~/anaconda2/bin/python

import networkx as nx
import pygraphviz as pg
import graphIt3D
import re

########################################
# this method does the leg work to prepare a graph where isoforms
# are collapsed to base gene names.
def prepCollapsed3D(nxgraph2, file, subName):
	labels = []
	group = []
	shapes = []

	###########################################
	# node colours and shape management for the collapsed version of a network.
	for node,nodeDict in nxgraph2.nodes(True):
		#node['name'] += node
		#labels.append(nodeDict['name'])
	
		if re.match("TRINITY", node):
			shapes.append('circle')
			nodeDict['shape'] = 'ellipse'
			nodeDict['fillcolor'] = 'white'
			labels.append(node)
			splitID = node.split("_")
			group.append('red')
			nodeDict['fontcolor'] = 'red'
			nodeDict['color'] = 'red'
		elif re.match("RNASPADES", node):
			shapes.append('square')
			nodeDict['shape'] = 'box'
			nodeDict['fillcolor'] = 'white'
			labels.append(node)
			splitID = node.split("_")
			group.append('green')
			nodeDict['fontcolor'] = 'green'
			nodeDict['color'] = 'green'
		elif re.match("OASES", node):
			shapes.append('diamond')
			nodeDict['shape'] = 'hexagon'
			nodeDict['fillcolor'] = 'white'
			labels.append(node)
			group.append('blue')
			nodeDict['fontcolor'] = 'lightblue'
			nodeDict['color'] = 'lightblue'

	# similar IO and position calculations
	newFile = (re.sub(".dot", "", file) + "-grouped.dot")
	nx.nx_agraph.write_dot(nxgraph2, newFile)
	pos = nx.drawing.layout.spring_layout(nxgraph2, dim=3)
	outFile = ((re.sub(".dot", "", file) + "-grouped.html"))
	positionsName = (subName + "-positions-grouped.tsv")

	f2 = open(positionsName, "w+")
	for key in pos.keys():
		f2.write(key + "\t")
		for item in pos[key]:
			f2.write(str(item) + "\t")
		f2.write("\n")
	f2.close()

	# render 3D graph for collapsed version of network.
	graphIt3D.graphIt(nxgraph2, pos, outFile, shapes, labels, group)
	return