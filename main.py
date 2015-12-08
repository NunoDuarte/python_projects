from readBNFile import readBNFile
from Graph import Graph
import sys

#Python version: 3.5
#read input file
input1 = 'input1.bn'

graph = Graph()


if '.bn' in input1:
    #it is Bayesian Network specification extension
    #self.numClients = int(first_line);
    fileBN = readBNFile(input1)
    graph = fileBN.readfile(graph.graph)

if '.in' in input1:
    print ('nothing')
    #it is the query and evidence variable
#             line = line.split(' ')
#             #convert to integer
#             first_line = [int(p) for p in line];
#             self.numCities = first_line[0];
#             self.numConnects = first_line[1];
    
# else:
#     print ('ERROR: wrong format')  
