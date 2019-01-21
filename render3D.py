#!~/anaconda2/bin/python

#######################################
# Connor Burbridge
# connor.burbridge@gifs.ca
# Global Institute for Food Security
#
# Script(s) and methods for rendering various 3D and 2D visualizations
# of comparison data from my honours project. Output from this program 
# is indicated by the base name of the file supplied.
#
# Usage: python render3D.py input.dot

import networkx as nx
import pygraphviz as pg
import plotly.graph_objs as go
import plotly.plotly as py
import plotly
#, prepIsoform3D, prepCollapsed3D
import sys, re

#######################################
# Base method for generating 3D figures. Call this script with the name of the dot
# file being the only argument. This method performs some pre-render work. Mostly
# storing information for isoform detection and some IO stuff.
def render3D():
	graph = nx.nx_agraph.read_dot(sys.argv[1])
	geneGraph = pg.AGraph()

	N = len(graph.nodes())
	print(N)

	subName = re.sub(".dot", "", sys.argv[1])
	f1Name = (subName + "-edges.txt")
	f2Name = (subName + "-edges-grouped.txt")
	#f1 = open(f1Name, "w+")
	#f2 = open(f2Name, "w+")
	edgeColor = []
	edgeWeight = []
	count = 0

	###########################################
	# go through edges in the input graph to generate edge files as well as the 
	# collapsed form of the 3D graph. Weights and colours are tracked throughout
	# the process.
	for (u,v,d) in graph.edges(data=True):
		d['weight'] = int(d['weight'])
		#f1.write(str(u) + " -- " + str(v) + "\n")
		edgeColor.append(d['color'])
		edgeWeight.append(d['weight'])
		count += 1
	
		splitName1 = u.split('_')
		splitName2 = v.split('_')
	
		if re.match("TRINITY", u):
			nodeName1 = ("TRINITY_" + splitName1[1])
		elif re.match("NODE", u):
			nodeName1 = ("RNASPADES_" + splitName1[6])
		elif re.match("Locus", u):
			nodeName1 = ("OASES_" + splitName1[1])
		if re.match("TRINITY", v):
			nodeName2 = ("TRINITY_" + splitName2[1])
		elif re.match("NODE", v):
			nodeName2 = ("RNASPADES_" + splitName2[6])
		elif re.match("Locus", v):
			nodeName2 = ("OASES_" + splitName2[1])

		if (geneGraph.has_edge(nodeName1, nodeName2)):
			edge = geneGraph.get_edge(nodeName1, nodeName2)
			edge.attr['weight'] = int(edge.attr['weight']) + int(d['weight'])
			continue
		else:	
			geneGraph.add_edge(nodeName1, nodeName2)
			edge = geneGraph.get_edge(nodeName1, nodeName2)
			edge.attr['weight'] = d['weight']
			#f2.write(nodeName1 + " -- " + nodeName2 + "\n")
			edge.attr['color'] = d['color']

	print("Collapsed graph stats numbers:")
	print("Nodes: " + str(len(geneGraph.nodes())))
	print("Edges: " + str(len(geneGraph.edges())))	
	
	#f1.close()
	#f2.close()
	nxgraph2 = nx.nx_agraph.from_agraph(geneGraph)
	
	for (u,v,d) in graph.edges(data=True):
		d['weight'] = (1/float(d['weight']))
		#print(d['weight'])
	
	for (u,v,d) in nxgraph2.edges(data=True):
		d['weight'] = (1/float(d['weight']))
		#print(d['weight'])

	labels = []
	group = []
	shapes = []
	isoformHash = {}
	#f1 = open(subName + "-nodes.txt", "w+")

	###########################################
	# generating a hash to check for isoforms output from programs
	for node, nodeDict in graph.nodes(True):
		if re.match("TRINITY", nodeDict['name']):
			#print(node)
			splitLine = node.split("_")
			#f1.write(splitLine[1] + "\n")
			if splitLine[1] in isoformHash:
				isoformHash[splitLine[1]] += 1
			else:
				isoformHash[splitLine[1]] = 1
		elif re.match("NODE", nodeDict['name']):
			splitLine = node.split("_")
			#f1.write(splitLine[6] + "\n")
			if splitLine[6] in isoformHash:
				isoformHash[splitLine[6]] += 1
			else:
				isoformHash[splitLine[6]] = 1
				
	###########################################
	# run external methods for generating positions, node colours, shapes etc.
	#prepIsoform3D.prepIsoform3D(graph, isoformHash, sys.argv[1], subName)
	#prepCollapsed3D.prepCollapsed3D(nxgraph2, sys.argv[1], subName)
	newFile = (re.sub(".dot", "", sys.argv[1]) + "-grouped.dot")
	nx.nx_agraph.write_dot(nxgraph2, newFile)
	print("Rendering complete.")
	sys.exit()

if __name__ == "__main__":
	if (len(sys.argv) < 2 or len(sys.argv) > 2):
		print("Incorrect number of arguments!")
		print("Usage: python render3D.py input.dot")
	else:
		render3D()
	
	
