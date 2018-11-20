#!~/anaconda2/bin/python
#
#####################################
# Connor Burbridge
# connor.burbridge@gifs.ca
# Global Institute for Food Security
# Bioinformatics Technician
#
# script for comparing alignments generated by mapping reads back to de-novo 
# transcript assemblies.
# call the script like so: python compare-assemblies-3.3.py sample1.sam sample2.sam output-file.dot
# This algorithm builds a graph of nodes as contigs and edges as unique reads shared
# shared between them that mapped back after assembly. This script outputs one large
# DOT file containing all contigs and edges after some filtering. It also outputs 
# DOT format graphs as well as sequences for each connected component with greater than 5
# nodes or contigs.

from collections import defaultdict
import re, sys
import graphBuild as gb

def hashBuild():
	######################################
	# file management and hash definitions
	print("Hello, world!")

	programOneFile = open(sys.argv[1], "r")
	programTwoFile = open(sys.argv[2], "r")
	progOneReadHash = defaultdict(list)
	progTwoContigHash = defaultdict(list)
	sequenceHash = defaultdict(dict)

	######################################
	# reading in lines from first .sam file and building dictionaries
	for line in programOneFile:
		line = re.sub("\n", "", line)
		splitLine = line.split()
	
		if (splitLine[0] == "@SQ" or splitLine[0] == "@HD" or splitLine[0] == "@PG"):
			continue
	
		read = splitLine[0]
		contig = splitLine[2]
		progOneReadHash[contig].append(splitLine[9])

		if ((splitLine[9] in sequenceHash) and (contig in sequenceHash[splitLine[9]])):
			sequenceHash[splitLine[9]][contig] += 1
		else:	
			sequenceHash[splitLine[9]][contig] = 1

	print(sys.argv[1] + " dictionary complete")
	programOneFile.close()

	######################################
	# reading in lines from second .sam file and building dictionaries
	for line in programTwoFile:
		line = re.sub("\n", "", line)

		splitLine = line.split()
	
		if (splitLine[0] == "@SQ" or splitLine[0] == "@HD" or splitLine[0] == "@PG"):
			continue
	
		read = splitLine[0]
		contig = splitLine[2]
		progTwoContigHash[splitLine[9]].append(contig)
	
		if ((splitLine[9] in sequenceHash) and (contig in sequenceHash[splitLine[9]])):
			sequenceHash[splitLine[9]][contig] += 1
		else:	
			sequenceHash[splitLine[9]][contig] = 1

	print(sys.argv[2] + " dicts complete")
	programTwoFile.close() 
	print("comparing assemblies")

	f = open("sequence-hash.tsv", "w+")
	for key in sequenceHash.keys():
		for contig in sequenceHash[key].keys():
			f.write(key + "\t" + contig + "\t" + str(sequenceHash[key][contig]) + "\n")

	gb.graphBuilder(progOneReadHash, progTwoContigHash, sequenceHash, sys.argv[3])

if __name__ == "__main__":
	if (len(sys.argv) < 4 or len(sys.argv) > 4):
		print('Incorrect number of arguments supplied! Please enter an appropriate number of values.')
		print('Example usage: python comparison-hash-build.py sample1.sam sample2.sam output-file.dot')
	else: 
		hashBuild()