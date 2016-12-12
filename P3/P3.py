#-*- coding: utf-8 -*-

DEBUG = False # flag for debug printing.
import sys
sys.path.append("../")

codeToJamo = { 'cho':('ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'),
'jung':('ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ'),
'jong':('','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ')}
def jamoCode(position,jamo) :
    return codeToJamo[position].index(jamo)
doubleJaums={
    'ㄳ':('ㄱ','ㅅ'),'ㅄ':('ㅂ','ㅅ'),
    'ㄵ':('ㄴ','ㅈ'),'ㄶ':('ㄴ','ㅎ'),
    'ㄺ':('ㄹ','ㄱ'),'ㄻ':('ㄹ','ㅁ'),'ㄼ':('ㄹ','ㅂ'),'ㄽ':('ㄹ','ㅅ'),'ㄾ':('ㄹ','ㅌ'),'ㄿ':('ㄹ','ㅌ'),'ㄿ':('ㄹ','ㅍ'),'ㅀ':('ㄹ','ㅎ')
}
nextCases={
  'ㄱ':'ㅋ', 'ㅋ':'ㄲ', 'ㄲ':'ㄱ',
  'ㄴ':'ㄹ', 'ㄹ':'ㄴ',
  'ㅣ':'ㅡ', 'ㅡ':'ㅢ','ㅢ':'ㅣ',
  'ㅏ':'ㅑ', 'ㅑ':'ㅏ','ㅓ':'ㅕ','ㅕ':'ㅓ',
  'ㄷ':'ㅌ','ㅌ':'ㄸ','ㄸ':'ㄷ',
  'ㅁ':'ㅅ','ㅅ':'ㅆ','ㅆ':'ㅁ',
  'ㅂ':'ㅍ','ㅍ':'ㅃ','ㅃ':'ㅂ',
  'ㅗ':'ㅛ','ㅛ':'ㅗ','ㅜ':'ㅠ','ㅠ':'ㅜ',
  'ㅈ':'ㅊ','ㅊ':'ㅉ','ㅉ':'ㅊ',
  'ㅇ':'ㅎ','ㅎ':'ㅇ'
}
insertEeCases={
  'ㅏ':'ㅐ','ㅓ':'ㅔ','ㅑ':'ㅒ','ㅕ':'ㅖ','ㅘ':'ㅙ','ㅝ':'ㅞ'
}
delCases={
    'ㄲ':'ㄱ','ㄸ':'ㄷ','ㅃ':'ㅂ','ㅆ':'ㅅ','ㅉ':'ㅈ','ㅐ':'ㅏ','ㅒ':'ㅑ'
}
# Build a hangul unicode string, with combination method.
def buildCombHangul(t) :
  if len(t)==2 :
    t=(t[0],t[1],'')
  assert(len(t)==3)
  output  = 0xac00
  output += jamoCode('cho',t[0])*21*28
  output += jamoCode('jung',t[1])*28
  output += jamoCode('jong',t[2])
  return chr(output)

# create korean chars' list from pulleossugi
def hangul(pulleossugi) :
  def pushHangul(stack) :
    if len(stack) == 1 :
      assert(stack[0][0]=='cho')
      output.append(chr(ord(codeToJamo['cho'][jamoCode('cho',stack[0][1])])))
    if len(stack) == 2 :
      stack.append(('jong',''))
    if len(stack) == 3 :
      char = (stack[0][1],stack[1][1],stack[2][1])
      output.append(buildCombHangul(char))
  output = []
  stack = []
  for c in pulleossugi :
    if c[0]=='cho' :
      pushHangul(stack)
      stack.clear()
    stack.append(c)
  pushHangul(stack)
  return output

############################################
# File paths definition

mealyFilePath=""
inputFilePath=""

# flag for path of hangulMealy machine file
if '--hangulMealy' in sys.argv : mealyFilePath=sys.argv[sys.argv.index('--hangulMealy')+1]
else : print("The path of the hangulMealy machine description file not found"); quit(-1) 

# flags for paths of input and output files
if '--input' in sys.argv : inputFilePath=sys.argv[sys.argv.index('--input')+1]
else : print("The path of input file not found"); quit(-1)
#if '--output' in sys.argv : outputFilePath=sys.argv[sys.argv.index('--output')+1]
#else : print("The path of output file not found"); quit(-1)

# flag for debug printing option. 0 for off, 1 for on
if '--debug' in sys.argv :
  if sys.argv[sys.argv.index('--debug')+1] == '1' :
    DEBUG=True
  else :
    DEBUG=False

import hangulMealy
# read hangulMealy machine from file
hangulMealy.read(mealyFilePath)
########################################

outputLine=[]

inputFile=open(inputFilePath,'r',-1,'utf-8')
for line in inputFile.readlines() :
    if DEBUG : print("========="); sys.stdout.write(line)
    outputLine = []
    currentState=hangulMealy.initState
    if DEBUG : print("current State : " + hangulMealy.initState)
    stack=[]
    pulleossugi=[]
    for char in line :
        if char == '\n' :
            break
        if char == '<' :
            #####################################
            continue
        if (currentState, char) in hangulMealy.delta :
            #transition exists
            def newHandler(result,lamb) : result.append((lamb[1],lamb[2]))
            def newWithPrevJong(result,lamb) :
              assert(result[-1][0]=='jong')
              result[-1]=('cho',result[-1][1])
              result.append(('jung',lamb[1]))
            def newWithPrevSplitJong(result,lamb) :
              print(result)
              assert(result[-1][0]=='jong')
              assert(result[-1][1] in doubleJaums.keys())
              temp = doubleJaums[result[-1][1]][1]
              result[-1]=('jong',doubleJaums[result[-1][1]][0])
              result.append(('cho',temp))
              result.append(('jung',lamb[1])) 
            def catHandler(result,lamb) : result.append((lamb[1],lamb[2]))
            def editHandler(result,lamb) : assert(result[-1][0]==lamb[1]); result[-1]=(lamb[1],lamb[2])
            def nextHandler(result,lamb) :
              assert(result[-1][1] in nextCases.keys())
              assert(lamb[2] in nextCases.keys())
              assert(result[-1][0]==lamb[1])
              result[-1]=(lamb[1],nextCases[result[-1][1]])
            def insertHandler(result,lamb) :
              assert(result[-1][1] in insertEeCases.keys())
              result[-1] = (result[-1][0],insertEeCases[result[-1][1]])
            def deleteJongNewChoHandler(result,lamb) :
              # print("deleteJongNewCho : " + lamb[1])
              assert(result[-1][0]=='jong')
              result[-1]=('cho',lamb[1])
            def deleteChoAddToJongHander(result,lamb) :
                assert(result[-1][0]=='cho')
                assert(result[-2][0]=='jong')
                result.pop()
                newPair = (result[-1][1],lamb[1])
                                # print(newPair)
                assert(newPair in doubleJaums.values())
                for dj in doubleJaums :
                    if doubleJaums[dj]==newPair :
                        result[-1]=('jong',dj)
            def deleteChoEditJongHandler(result, lamb) :
                assert(result[-1][0]=='cho')
                assert(result[-2][0]=='jong')
                result.pop()
                result[-1]=('jong',lamb[1])
            def reduceJongNewChoHandler(result, lamb) :
                assert(result[-1][0]=='jong')
                assert( result[-1][1] in doubleJaums.keys() )
                pair = doubleJaums[result[-1][1]]
                result[-1]=('jong',pair[0])
                result.append(('cho',lamb[1]))

            currentLamb = hangulMealy.lamb[currentState,char]
            if DEBUG : print(currentLamb,end=' ')
            handler={
              'new':newHandler, 'cat':catHandler, 'edit':editHandler,
              'delete prev jong and new cho':deleteJongNewChoHandler,
              'new with prev jong':newWithPrevJong,
              'new with prev split jong':newWithPrevSplitJong,
              'next':nextHandler,
              'insert':insertHandler,
              'delete cho and add to prev jong':deleteChoAddToJongHander,
              'delete cho and edit prev jong':deleteChoEditJongHandler,
              'reduce prev jong and new cho':reduceJongNewChoHandler
            }
            if currentLamb[0] in handler.keys() :
              handler[currentLamb[0]](pulleossugi,currentLamb)
            if DEBUG :
                print("%3s to %3s by %s"%(currentState,hangulMealy.delta[currentState,char],char))

            #state transition
            currentState=hangulMealy.delta[currentState,char]
        else :
            # no transition
            outputLine=["No path exists!"]
            break
    if DEBUG : print(outputLine)
    if DEBUG : print(pulleossugi)
    print("(입력) $ ",end='')
    print(line[:-1], end="")
    if not line[-1] is '\n' : print(line[-1],end='')
    print('',end='\n(출력) $ ')
    print(''.join(hangul(pulleossugi)))
inputFile.close()