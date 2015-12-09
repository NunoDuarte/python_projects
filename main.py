from readBNFile import readBNFile
from readINFile import readINFile
from Graph import Graph
import sys

#Python version: 3.5
#read input file
input1 = 'input1.bn'
input2 = 'input2.in'
graph = Graph()


if '.bn' in input1:
    #it is Bayesian Network specification extension
    fileBN = readBNFile(input1)
    graph = fileBN.readfile(graph.graph)

if '.in' in input2:
    fileIn = readINFile(input2)
    q_variable = fileIn.readfile(graph)
    
else:
    print ('ERROR: wrong format')  
