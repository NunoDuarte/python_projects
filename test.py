from readFile import readFile
from DFS import DFS
from BFS import BFS
from Graph import Graph

clients = readFile('input2.cli');
cli = clients.openFile();

line = [];

mapas =  readFile('input1.map');
mapa = mapas.openFile();

graph = Graph();
#Read each connection and add a node respectively
for i in range(0, mapa.numConnects):
	graph.graph = mapas.readMap(graph.graph)

#Associate child nodes to the respective parent (it is double because the inverted route
for i in range(0, 2*mapa.numConnects):
	graph.graph = graph.MakeGraph(i, graph.graph[i].arrival, graph.graph)
	

	

#Read each client separately 
for i in range (0,  cli.numClients):
	
	line.append(i)
	line[i] = clients.readLine()
	
	#tree = node.MakeGraph(line[i][1], graph.graph, tree)
# 	dfs = DFS();
# 	startingNode = dfs.dfs_initState(graph.graph, line[i][1])
# 	solution = dfs.dfs_search(startingNode, line[i][2])
	bfs = BFS();
	startingNode = bfs.bfs_initState(graph.graph, line[i][1])
	solution = bfs.bfs_search(startingNode, line[i][2])
	print (solution)
	#print (solution)
	#search = dfs(line[2])
	

	


