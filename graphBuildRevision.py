import pygraphviz as pygv
import networkx as nx
from collections import defaultdict

#####################################
# Method definition that builds a graph with contigs as nodes and the edges
# between them as the reads that are shared by both contigs.
def graphBuilder(progOneReadHash, progTwoContigHash, sequenceHash, outFile):

	#print(progTwoReadHash)
	#print(progTwoContigHash)
	#edgeReadHash = defaultdict(list)
	seqCheckHash = defaultdict(list)
	edgeSequenceHash = defaultdict(set)
	graph = pygv.AGraph(format="svg", rankdir='LR')
	identicalSeqs = 0
	checkedSeqs = 0
	totalSeqs = 0
	
	# Building the full graph from hashed reads and contigs.
	# Iterates through contigs from program one by size: largest -> smallest
	# For each contig, iterate through all the reads mapped to it. If that
	# read is in the other programs hash, iterate through all the contigs
	# that it mapped to and create nodes, and edges and maintain edge weights
	# if the sequence shared bewteen contigs is unique. 
	# NOTE: this algorithm  does not consider redundant sequences (sequences that map 
	# between contigs more than once). Only non-redundant sequences are included in the
	# final graphs.
	for contig in sorted(progOneReadHash, key=lambda contig: len(progOneReadHash[contig]), reverse=True):
		graph.add_node(contig)
		vertex1 = graph.get_node(contig)
		vertex1.attr['fontcolor'] = 'blue'
		vertex1.attr['group'] = "1"
		vertex1.attr['name'] = contig
		
		for read in progOneReadHash[contig]:
			totalSeqs += 1
			if (sequenceHash[read][contig] > 1):
				if (read in seqCheckHash):
					identicalSeqs += 1
					continue
				else:
					seqCheckHash[read] = True
					checkedSeqs += 1 #duplicated seqs....
			else:
				for hit in progTwoContigHash[read]:
					graph.add_node(hit)
					vertex2 = graph.get_node(hit)
					vertex2.attr['fontcolor'] = 'red'
					vertex2.attr['group'] = "2"
					vertex2.attr['name'] = hit
										
					if (graph.has_edge(contig, hit)):
						existingEdge = graph.get_edge(contig, hit)
						existingEdge.attr['weight'] = int(existingEdge.attr['weight']) + 1
						existingEdge.attr['label'] = existingEdge.attr['weight']
						edgeSequenceHash[existingEdge.attr['name']].add(read)
					else:
						graph.add_edge(contig, hit)
						newName = (contig + "_" + hit)
						newEdge = graph.get_edge(contig, hit)
						newEdge.attr['name'] = newName
						newEdge.attr['weight'] = "1"
						newEdge.attr['label'] = newEdge.attr['weight']
						edgeSequenceHash[newEdge.attr['name']].add(read)
	
	graph.format = 'svg'
	print("Number of nodes: " + str(graph.number_of_nodes()))
	print("Number of edges before filtering: " + str(graph.number_of_edges()))
	
	# Filtering and colouring edges based on the number of unique sequences
	# shared between contigs.
	for edge in graph.edges():
		#if (int(edge.attr['weight']) < 5):
			#graph.remove_edge(edge)
		if (int(edge.attr['weight']) <= 50):
			edge.attr['color'] = 'red'
		elif (int(edge.attr['weight']) <= 200):
			edge.attr['color'] = 'orange'
		elif (int(edge.attr['weight']) <= 1000):
			edge.attr['color'] = 'yellow'
		elif (int(edge.attr['weight']) > 1000):
			edge.attr['color'] = 'green'
	print("Number of edges after filtering: " + str(graph.number_of_edges()))	
	print("Writing graphs and sequence files now...")	
	graph.write(outFile)
	
	# Convert original graph to a NetworkX graph
	nxgraph = nx.nx_agraph.from_agraph(graph)
	isolates = nx.number_of_isolates(nxgraph)
	clusterCount = 0
	oneToOne = 0
	what = 0

	# Pulling out the individual connected components of size 5 and greater.
	# For each connected component, write a graph file and a file with all 
	# sequences present in the connected component
	for cc in sorted(nx.connected_component_subgraphs(nxgraph), key=len, reverse=True):
		if len(cc.nodes()) > 2:
			clusterFile = ("cluster" + str(clusterCount) + "_" + str(len(cc.nodes())) + ".dot")
			clusterReads = ("cluster" + str(clusterCount) + "_reads.seq")
			readFile = open(clusterReads, "a")
			pycc = nx.nx_agraph.to_agraph(cc)
			#for edge in pycc.edges():
				#name = str(edge.attr['name'])
				#for read in edgeSequenceHash[name]:
					#readFile.write(read + "\n")
			#readFile.close()
			pycc.write(clusterFile)
			clusterCount += 1
		elif len(cc.nodes()) == 2:
			oneToOne += 1
		else:
			what += 1
			
	print("Number of clusters with a 1-to-1 equivalence: " + str(oneToOne))
	print("Clusters with a 1-to-n equivalence: " + str(clusterCount))
	print("Total number of connected components: " + str(clusterCount + oneToOne))
	print("Isolated nodes: " + str(isolates))
	print("Identical sequences count: " + str(identicalSeqs))
	print("Number of sequences checked: " + str(checkedSeqs))
	print("Total number of sequences checked: " + str(totalSeqs))
	print("What count: " + str(what))
			
	