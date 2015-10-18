from readFile import readFile
from DFS import DFS
from BFS import BFS
from Graph import Graph

import copy 

clients = readFile('input2.cli');
cli = clients.openFile();

line = [];

mapas =  readFile('input1.map');
mapa = mapas.openFile();

graph = Graph();
#Read each connection and add a node respectively
for i in range(0, mapa.numConnects):
	graph.graph = mapas.readMap(graph.graph)
	
output = clients.file.replace('.cli', '.sol')
output = open(output, 'w')

#Read each client separately 
for i in range (0,  cli.numClients):
	
	line.append(i)
	line[i] = clients.readLine()
	print (line[i])
	
	#reset the graph
	graph.count = 0;
	loop_graph = copy.deepcopy(graph.graph);
	
	loop_graph = graph.checkConstraints(loop_graph, line[i], int(line[i][5]));

	#Associate child nodes to the respective parent (it is double because the inverted route
	for j in range(0, 2*mapa.numConnects - graph.count):
		loop_graph = graph.MakeGraph(j, loop_graph[j].arrival, loop_graph)
	
	# Depth First Search Algorithm
# 	dfs = DFS();
# 	dfs.limitCost = graph.limitCost;
# 	dfs.limitTime = graph.limitTime;
# 	startingNode = dfs.dfs_initState(loop_graph, line[i][1], int(line[i][3]))
# 	solution = dfs.dfs_search(startingNode, line[i][2])

	# Breadth First Search Algorithm
	bfs = BFS();
	bfs.limitCost = graph.limitCost;
	bfs.limitTime = graph.limitTime;
	startingNode = bfs.bfs_initState(loop_graph, line[i][1], int(line[i][3]))
	solution = bfs.bfs_search(startingNode, line[i][2])
	
	# Write to the .sol text file
	if not solution:
		solution = str(-1);
	solution = str(i+1) + ' ' + solution
	output.write(solution + '\n')
	

	


