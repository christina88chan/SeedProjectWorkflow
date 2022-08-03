import sys 
import os 
import re

#INPUT FILE
filename = sys.argv[1]

#CHECK INPUT FILE 
if filename.find(".gjf") == -1:
	print("You have not submitted a proper input file. Please try again with a .gjf file")
	print("Exiting program.")
	exit() 

#FILE NAME EXTRACTOR
def fileNameEx(filename):
	index = filename.rfind(".gjf")
	fileN = filename[:index]
	return fileN
	print(fileN)

#TOTAL LINES FUNCTION
def totalLines(file):
	f = open(file, "r")
	totalLines = 0
	for line in f: 
		totalLines = totalLines+1
	return totalLines
	f.close()
#NORMAL TERMINATION FUNCTION 
def NormalTermination(logfile):
	f = open(logfile, "r")
	allLines = totalLines(logfile) 
	numLines = 0
	count = 0
	for line in f:
		if "Normal termination" in line:
       			 count = count + 1
        		 numLines = numLines + 1
		else:
		       	 numLines = numLines + 1
	if numLines == allLines:
		if count > 0:
			print("Normally terminated", count, "time(s).")
		else:
			print("Job not normally terminated. Exiting program. ")
			exit()
	f.close()
#STABLE = OPT JOB
def Stability(logfile):
	f = open(logfile, "r")
	allLines = totalLines(logfile)
	stabLine = 0;
	for i, line in enumerate(f):
		if "RHF -> UHF instability" in line:
			print("Molecule is not stable. Found in line:", i, line)
			break
		else:
			stabLine = stabLine + 1
	if stabLine == allLines:
		print("Molecule is stable.")
	f.close
#OPT FREQ
def OptFrequency(logfile):
	f = open(logfile, "r")
	allLines = totalLines(logfile)
	numLines = 0
	optLines = 0
	for i, line in enumerate(f):
		if "Opt Freq" in line:
			print("There is an opt freq. Found in line:", i)
		else:
			numLines = numLines + 1
		if "imaginary frequencies" in line:
			print(line[7:30], ".", sep='')
		else:
			optLines = optLines + 1
	if numLines == allLines:
		print("Opt freq not found.")
	if optLines == allLines:
		print("0 imaginary frequency found, there is a minima.")	
	f.close()

job = fileNameEx(filename)

print("Input running: " + job)
print()

#SINGLE POINT ENERGY JOB
print("* Running single-point energy job *")
cmd = "g16 " + filename
logfile = job + ".log"
os.system(cmd)
NormalTermination(logfile)
print()

#STABILITY JOB
print("* Running stability job. *")
cmd ="g16 -ic="+job+".chk -y="+job+"-2.chk -x='#p chkmethod chkbasis geom=allcheck guess=read Stable=opt' < /dev/null >&"+job+"-2.log"
os.system(cmd)
job2 = job + "-2.log" 
NormalTermination(job2)
Stability(job2)
print()

#OPT FREQ JOB
print("* Running optimization frequency job. *")
cmd="g16 -ic="+job+"-2.chk -y="+job+"-3.chk -x='#p chkmethod chkbasis geom=allcheck guess=read Opt Freq' < /dev/null >&"+job+"-3.log"
os.system(cmd)
job3 = job + "-3.log"
NormalTermination(job3)
OptFrequency(job3) 
print()

print("Workflow manager has finished running. Thank you! Exiting Program.")
exit()
