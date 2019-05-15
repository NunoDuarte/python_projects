from readFile import readFile
from GSAT import GSAT
from WalkSAT import WalkSAT
from DPLL import DPLL
import time
import sys

#Python version: 3.5
#read input file
file = readFile(sys.argv[1])
file = file.openFile()

output = file.file.replace('.cnf', '.sol')
output = open(output, 'w')
output.write('c TYPE SOLUTION VARIABLES CLAUSES CPUSECS MEASURE1 \n')

#The knowledge Base
KB = file.readClauses(file)

## uf20-files take on average 30 s using GSAT
max_restarts = 10000;
max_climbs = 10;

## uf20-files are almost instantly for the WalkSAT
max_flips = 30000;
probability = 5;

GSAT = GSAT(KB, file, max_restarts, max_climbs);
start_time = time.time()
solution = GSAT.search();
cpu_secsGSAT = time.time() - start_time;
cpu_secsGSAT = round(cpu_secsGSAT, 2)
   
# Write to the .sol text file
if not solution:
    output.write('s' + ' ' + str(file.formatID) + ' ' + str(0) + ' ' + str(file.variables) + ' ' + str(file.clauses) + ' ' + str(cpu_secsGSAT) + ' ' + str(0) + '\n')
else: 
    output.write('s' + ' ' + str(file.formatID) + ' ' + str(1) + ' ' + str(file.variables) + ' ' + str(file.clauses) + ' ' + str(cpu_secsGSAT) + ' ' + str(0) + '\n')
    file.writeOutput(output, solution)

WalkSAT = WalkSAT(KB, file, probability, max_flips);
start_time = time.time()
solution = WalkSAT.search();
cpu_secsWalkSAT = time.time() - start_time;
cpu_secsWalkSAT = round(cpu_secsWalkSAT, 2)

# Write to the .sol text file
if not solution:
    output.write('s' + ' ' + str(file.formatID) + ' ' + str(0) + ' ' + str(file.variables) + ' ' + str(file.clauses) + ' ' + str(cpu_secsWalkSAT) + ' ' + str(0) + '\n')
else: 
    output.write('s' + ' ' + str(file.formatID) + ' ' + str(1) + ' ' + str(file.variables) + ' ' + str(file.clauses) + ' ' + str(cpu_secsWalkSAT) + ' ' + str(0) + '\n')
    file.writeOutput(output, solution)

DPLL = DPLL(KB, file);
start_time = time.time()
solution = DPLL.satisfiable();
cpu_secsDPLL = time.time() - start_time;
cpu_secsDPLL = round(cpu_secsDPLL, 2)
     
# Write to the .sol text file
if not solution:
    output.write('s' + ' ' + str(file.formatID) + ' ' + str(0) + ' ' + str(file.variables) + ' ' + str(file.clauses) + ' ' + str(cpu_secsDPLL) + ' ' + str(0) + '\n')
else: 
    output.write('s' + ' ' + str(file.formatID) + ' ' + str(1) + ' ' + str(file.variables) + ' ' + str(file.clauses) + ' ' + str(cpu_secsDPLL) + ' ' + str(0) + '\n')
    file.writeOutput(output, solution)



