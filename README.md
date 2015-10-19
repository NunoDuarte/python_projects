# SearchAlgorithm
Search Algorithm for the best route

This is Python (version 3.5) code for 3 Search Algorithms.
The objective is given a client that wants to go from city A to city B, and with some personal preferences (doesn't want to go buy plain, or it want the fastest journey).

The 3 Search Algorithms are:
  Uninformed Search Algorithm:
  - Breadth First Search
  - Depth First Search
  
  Informed Search Algorithm:
  - A* Algorithm 

-------------//--------------

You give a input.map file with all the different connections between 2 cities;

cityA TypeofTransport cityB duration cost Ti Tf Intervals

Ti = time instant of the rst depart on each day
Tf = time instant after which there are no more departures
Intervals = daily periodicity

You give a input.cli with all the clients that want the best route corresponding to his/her specifications;

i cityA cityB Ti criteria number A typeA B typeB

i = the number of clients
two integer numbers identifying the initial (typeA) and final cities (typeB) ;
Ti = a non-negative integer number representing the time instant after which the client is available to travel;
criteria =  'tempo' or 'custo'; What does the client wants to optimize
number = the number of constraints (0, 1 or 2)

A typeA:
- a pair of two elements, where the rst can be A1, A2 or A3, and the second can be aviao, comboio, autocarro or barco if the first is A1 or an integer number if the rst is either A2 or A3;
B typeB
- a pair of two more elements composed by one of the words B1 or B2, followed by an integer number.



