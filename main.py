from readFile import readFile

file = readFile('input.cnf')
file = file.openFile()

file.readClauses(file)
