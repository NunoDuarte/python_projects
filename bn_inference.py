from readBNFile import readBNFile
from readINFile import readINFile
from Graph import Graph
from BN import BN
import sys

#Python version: 3.5
#read input file
input1 = sys.argv[1]
input2 = sys.argv[2]
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

#start algorithm
BN = BN(graph, q_variable);
sol = BN.run()

solution = sol[0][-1]
#the probability of the query being false (in case it has 2 evidence variables)
solution_1 = sol[pow(2, 2)][-1]

output = input1.replace('.bn', '.sol')
output = open(output, 'w')
output.write('########## SOLUTION ##########\n')
output.write('QUERY '+ str(fileIn.query) + '\n')
output.write('QUERY_DIST '+ 'T ' + str(solution) + ' F ' +  str(solution_1) + '\n')

