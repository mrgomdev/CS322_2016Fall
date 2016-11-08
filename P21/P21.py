#-*- coding: utf-8 -*-

DEBUG=False # flag for debug printing.

import sys
sys.path.append("./")

def quitWithHelp(causeStr="") :
  print(causeStr)
  print("="*10)
  print("Running Policy of P21 : python P21.py --enfa [e-nfa file path] --mdfa [m-dfa output file path] --input [input file path for testing] --output [output file path for testing]")
  print("    Given output file path is for e-nfa")
  print("    Generated m-dfa will output to \"mdfa[outputFilePath]\" ")
  quit(-1)

eNfaFilePath=""
mDfaFilePath=""
inputFilePath=""
outputFilePath=""
# flag for path of enfa and mdfa file
if '--enfa' in sys.argv : eNfaFilePath=sys.argv[sys.argv.index('--enfa')+1]
else : quitWithHelp("The path of e-NFA description file not found") 
if '--mdfa' in sys.argv : mDfaFilePath=sys.argv[sys.argv.index('--mdfa')+1]
else : quitWithHelp('The path for output m-DFA description file not found')


# flags for paths of input and output files
if '--input' in sys.argv : inputFilePath=sys.argv[sys.argv.index('--input')+1]
else : quitWithHelp("The path of input file not found")
if '--output' in sys.argv : outputFilePath=sys.argv[sys.argv.index('--output')+1]
else : quitWithHelp("The path for output file of e-nfa not found")

# flag for debug printing option. 0 for off, 1 for on
if '--debug' in sys.argv :
  if sys.argv[sys.argv.index('--debug')+1] == '1' :
    DEBUG=True
  else :
    DEBUG=False

import nfa
# read nfa from file
nfa.read(eNfaFilePath)

outputFile=open(outputFilePath,'w')
inputFile=open(inputFilePath,'r')

for line in inputFile.readlines() :
  if line[:3] == 'end' : break
  def track(state, restStr) :
    global nfa
    if len(restStr)==0 :
      if nfa.isFinal(state) : return True
      else : return 'Not Final'
    if (state, 'E') in nfa.delta :
      for q2 in nfa.delta[(state,'E')] :
        t=track(q2,restStr)
        if t==True : return True
    if (state, restStr[0]) in nfa.delta :
      for q2 in nfa.delta[(state,restStr[0])] :
        t = track(q2,restStr[1:])
        if t==True : return True
    return 'No Transition'
  if track(nfa.initState, line[:-1])==True :
    outputFile.write("네\n")
  else :
    outputFile.write("아니오\n")
outputFile.close()
inputFile.close()

nfa.convert()

mDfaFile=open(mDfaFilePath,'w')
mDfaFile.write(nfa.toString())
mDfaFile.close()

# removing last new line 
outputFile=open(outputFilePath,'r')
buffer=outputFile.read()
outputFile.close()

outputFile=open(outputFilePath,'w')
outputFile.write(buffer[:-1])
outputFile.close()

import os
print("python P01.py --input %s --output %s --dfa %s"%(inputFilePath,"mdfa%s"%(outputFilePath,),mDfaFilePath))
os.system("python P01.py --input %s --output %s --dfa %s"%(inputFilePath,"mdfa%s"%(outputFilePath,),mDfaFilePath))
print("diff %s %s"%(outputFilePath,"mdfa%s"%outputFilePath))
os.system("diff %s %s"%(outputFilePath,"mdfa%s"%outputFilePath))
