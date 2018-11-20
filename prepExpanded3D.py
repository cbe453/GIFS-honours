#!~/anaconda2/bin/python

import graphIt3D
import networkx as nx
import pygraphviz as pg
import re

#########################################
# this method does most of the leg work for building a graph where
# isoforms are permitted
def prepIsoform3D(graph, isoformHash, file, subName):
	labels = []
	group = []
	shapes = []

	###########################################
	# set node colours and shapes based on the presence of isoforms. This is for the
	# network that includes isoforms.	
	for node, nodeDict in graph.nodes(True):
		#node['name'] += node
		#labels.append(nodeDict['name'])
	
		if re.match("TRINITY", nodeDict['name']):
			shapes.append('circle')
			nodeDict['shape'] = 'ellipse'
			nodeDict['fillcolor'] = 'white'
			labels.append(nodeDict['name'])
			splitID = node.split("_")
			if isoformHash[splitID[1]] > 1:
				group.append('pink')
				nodeDict['fontcolor'] = 'pink'
				nodeDict['color'] = 'pink'
			else:
				group.append('red')
				nodeDict['fontcolor'] = 'red'
				nodeDict['color'] = 'red'
		elif re.match("NODE", nodeDict['name']):
			shapes.append('square')
			nodeDict['shape'] = 'box'
			nodeDict['fillcolor'] = 'white'
			labels.append("rnaspades_" + nodeDict['name'])
			splitID = node.split("_")
			if isoformHash[splitID[6]] > 1:
				group.append('springgreen')
				nodeDict['fontcolor'] = 'green4'
				nodeDict['color'] = 'green4'
			else:
				group.append('green')
				nodeDict['fontcolor'] = 'green'
				nodeDict['color'] = 'green'
		elif re.match("Locus", nodeDict['name']):
			shapes.append('diamond')
			nodeDict['shape'] = 'hexagon'
			nodeDict['fillcolor'] = 'white'
			labels.append("oases_" + nodeDict['name'])
			if re.search("_1/1_", nodeDict['name']):
				group.append('blue')
				nodeDict['fontcolor'] = 'white'
				nodeDict['color'] = 'white'
			else:
				group.append('lightblue')
				nodeDict['fontcolor'] = 'lightblue'
				nodeDict['color'] = 'lightblue'

	# IO stuff for dot files and calculating positions
	newFile = (re.sub(".dot", "", file) + "-iso.dot")
	nx.nx_agraph.write_dot(graph, newFile)
	pos = nx.drawing.layout.spring_layout(graph, dim=3)
	outFile = ((re.sub(".dot", "", file) + ".html"))
	positionsName = (subName + "-positions.tsv")

	f2 = open(positionsName, "w+")
	for key in pos.keys():
		f2.write(key + "\t")
		for item in pos[key]:
			f2.write(str(item) + "\t")
		f2.write("\n")
	f2.close()
	#print(pos)

	# generate 3D network
	graphIt3D.graphIt(graph, pos, outFile, shapes, labels, group)
	return
