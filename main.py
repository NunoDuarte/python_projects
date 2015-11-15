from readFile import readFile
from GSAT import GSAT


file = readFile('input.cnf')
file = file.openFile()

KB = file.readClauses(file)
print (KB)



max_restarts = 3;
max_climbs = 5;

GSAT = GSAT(KB, file, max_restarts, max_climbs);
solution = GSAT.search();

print (solution)


# print (random.randint(0,1))


