from readFile import readFile
from DFS import DFS
from Node import Node

clients = readFile('input2.cli');
cli = clients.openFile();

line = [];

mapas =  readFile('input1.map');
mapa = mapas.openFile();

graph = [];
#Read each connection and add a node respectively
for i in range(0, mapa.numConnects):
	graph = mapas.readMap(graph)
	

#Read each client separately 
for i in range (0,  cli.numClients):
	
	line.append(i)
	line[i] = clients.readLine()
	
	node = Node();
	tree = [];
	tree = node.MakeGraph(line[i][1], graph, tree)
	dfs = DFS();
	solution = dfs.dfs_search(tree, line[i][2], graph)
	print (solution)
	#search = dfs(line[2])
	

	


