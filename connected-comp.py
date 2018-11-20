#!~/anaconda2/bin/python

import pygraphviz as pygv
import networkx as nx
import sys

size = sys.argv[2]
inGraph = sys.argv[1]

print("Fetching connected components greater than size " + size + " for further analysis")

pygraph = pygv.AGraph(inGraph)
nxgraph = nx.nx_agraph.from_agraph(pygraph)
clusterCount = 1

for cc in sorted(nx.connected_component_subgraphs(nxgraph), key=len, reverse=True):
	if len(cc.nodes()) > 10:
		#print(len(c))
		clusterFile = ("cluster" + str(clusterCount) + "_" + str(len(cc.nodes())) + ".dot")
		pycc = nx.nx_agraph.to_agraph(cc)
		for edge in pycc.edges():
			print(edge.attr['name'])
		#pycc.write(clusterFile)
		clusterCount += 1

