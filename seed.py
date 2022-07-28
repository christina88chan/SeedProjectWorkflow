import sys 

print("Enter log file name: ")
logfile = input()

#Counts total lines
f = open(logfile, "r")
totalLines = 0
for line in f: 
    totalLines = totalLines+1     
print(totalLines) 
f.close()

#Normal Termination 
f = open(logfile, "r")

numLines = 0; 
count = 0; 

for line in f: 
    if "Normal termination" in line: 
        count = count + 1; 
        numLines = numLines + 1; 
    else: 
        numLines = numLines + 1; 

if numLines == totalLines:
    if count > 0:
        print("Normally terminated", count, "time(s).")
    else:
        print("Not normally terminated.")

f.close()


#Imaginary Frequency 
f = open(logfile, "r")

numLines = 0 
optLines = 0 

for i, line in enumerate(f):
    #print(i, line)
    if "opt freq" in line: 
        print("There is an opt freq. Found in line:", i)
    else:
        numLines = numLines + 1
        
    if "imaginary frequencies" in line:
        print(line[7:30], ".", sep='')
    else: 
        optLines = optLines+1
        
if numLines == totalLines: 
    print("Opt freq not found.") 
if optLines == totalLines: 
    print("0 imaginary frequency.")
        
    
f.close()

#Stability Check 
f = open(logfile, "r")

stabLine = 0; 
for i, line in enumerate(f):
    if "RHF -> UHF instability" in line: 
        print("Molecule is not stable. Found in line:", i, line)
        break 
    else: 
        stabLine = stabLine + 1
        
if stabLine == totalLines: 
    print("Molecule is stable.")
    
f.close()
