# need pip install jamo
import sys, re
from jamo import h2j, j2hcj
from seq2seq.merger.unicode import join_jamos

def isHangul(text):
    #Check the Python Version
    pyVer3 =  sys.version_info >= (3, 0)

    if pyVer3 : # for Ver 3 or later
        encText = text
    else: # for Ver 2.x
        if type(text) is not unicode:
            encText = text.decode('utf-8')
        else:
            encText = text

    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0

# jamo-level
def decomposition(sentence):
    sentence = j2hcj(h2j(sentence))
    index = []
    for item in sentence:
      if(not isHangul(item) and item.isalpha()):
        index.insert(-1, sentence.find(item))
        break
    if(len(index)):
      part1 = list(sentence[:index[0]-1])
      part2 = sentence[index[0]:].split()
      return ''.join((part1 + part2))
    else:
      return sentence
    
def reconstructor(decom):
  return join_jamos(''.join(decom))

'''
 Here is the cell about rules.
 Each return values have 2 values.
 And the second values are intended to generate complete 한글
 because the second value will become the first value next for-loop(in below 'composer' function).
'''

# rule about '었'
def ruleOfEot(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3:
    # 어떻었다 ㄸㅓㅎ ㅇㅓㅆ => 어땠다
    if deFront[1] == 'ㅓ' and deFront[2] == 'ㅎ':
      return '', deFront[0] + 'ㅐ' + deBack[-1]
    # Irregular about 'ㄷ' badchim of '듣'
    elif deFront[-3] == 'ㄷ' and deFront[-2] == 'ㅡ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # Irregular about 'ㄷ' badchim of '싣', '긷'
    elif (deFront[-3] == 'ㅅ' or deFront[-3] == 'ㄱ') and deFront[-2] == 'ㅣ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # Irregular about 'ㄷ' badchim of '눋', '붇', '묻'
    elif (deFront[-3] == 'ㄴ' or deFront[-3] == 'ㅂ' or deFront[-3] == 'ㅁ') and deFront[-2] == 'ㅜ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # '업', '접' have no tallak
    elif (deFront[-3] == 'ㅇ' or deFront[-3] == 'ㅈ') and deFront[-2] == 'ㅓ' and deFront[-1] == 'ㅂ':
      return deFront, deBack
    # 뜨겁었다 ㄱㅓㅂ ㅇㅓㅆ
    elif deFront[2] == 'ㅂ':
      return deFront[:2], deBack[0] + 'ㅝ' + deBack[-1]
    # Irregular about 'ㅅ' badchim of '긋'
    elif deFront[-3] == 'ㄱ' and deFront[-2] == 'ㅡ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    # Irregular about 'ㅅ' badchim of '젓'
    elif deFront[-3] == 'ㅈ' and deFront[-2] == 'ㅓ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    # Irregular about 'ㅅ' badchim of '잇', '짓'
    elif (deFront[-3] == 'ㅇ' or deFront[-3] == 'ㅈ') and deFront[-2] == 'ㅣ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    else:
      return deFront, deBack
  else:
    if deFront[1] == 'ㅜ':
      return '', deFront[0] + 'ㅝ' + deBack[-1]
    elif deFront[1] == 'ㅣ':
      return '', deFront[0] + 'ㅕ' + deBack[-1]
    elif deFront[1] == 'ㅐ':
      return '', deFront + deBack[-1]
    elif deFront[-2] == 'ㄹ' and deFront[-1] == 'ㅡ':
      return deFront[-2], 'ㄹ' + deBack[1:]
    elif deFront[-2] == 'ㄹ' and deFront[-1] == 'ㅓ':
      return '', 'ㄹㅐ' + deBack[-1]
    elif deFront[-1] == 'ㅡ':
      return '', deFront[-2] + deBack[1:]
    else:
      return deFront, deBack

# rule about '았'
def ruleOfAt(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3:
     # Irregular about 'ㅅ' badchim of '낫', '잣'
    if (deFront[-3] == 'ㄴ' or deFront[-3] == 'ㅈ') and deFront[-2] == 'ㅏ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    else:
      return deFront, deBack
  else:
    if deFront[1] == 'ㅏ':
      return '', deFront + deBack[-1]
    elif deFront[-1] == 'ㅗ':
      return '', deFront[-2] + 'ㅘ' + deBack[-1]
    elif deFront[-2] == 'ㄹ' and deFront[-1] == 'ㅡ':
      return deFront[-2], 'ㄹ'+deBack[1:]
    elif deFront[-1] == 'ㅡ':
      return '', deFront[-2] + deBack[1:]
    else:
      return deFront, deBack

# rule about '시'
def ruleOfSi(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3:
    if deFront[-1] == 'ㅎ'or deFront[-1] == 'ㄹ':
      return deFront[:2], deBack
    else:
      return deFront, deBack
  else:
    return deFront, deBack

# rule about '였'
def ruleOfYeot(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if deFront[-2] == 'ㅎ' and deFront[-1] == 'ㅏ':
    return '', deFront[-2] + 'ㅐ' + deBack[-1]
  elif deFront[-2] == 'ㄷ' and deFront[-1] == 'ㅐ':
    return 'ㄷㅏ', 'ㅎㅐㅆ'
  else:
    return deFront, deBack

# rule about '아' 
def ruleOfAh(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3:
    if deFront[-3] == 'ㄷ' and deFront[-2] == 'ㅗ' and deFront[-1] == 'ㅂ':
      return deFront[:-1], deBack[0] + 'ㅘ'
    # Irregular about 'ㅅ' badchim of '낫', '잣'
    elif (deFront[-3] == 'ㄴ' or deFront[-3] == 'ㅈ') and deFront[-2] == 'ㅏ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    else:
      return deFront, deBack
  else:
    if deFront[-2] == 'ㅎ' and deFront[-1] == 'ㅏ':
      return '', deFront[0] + 'ㅐ'
    elif deFront[-1] == 'ㅏ':
      return '', deFront
    elif deFront[-1] == 'ㅐ':
      return '', deFront
    elif deFront[-2] == 'ㄹ' and deFront[-1] == 'ㅡ':
      return deFront[0], 'ㄹ'+deBack[-1]
    elif deFront[-2] == 'ㄷ' and deFront[-1] == 'ㅗ':
      return deFront, deBack[0] + 'ㅘ'
    elif deFront[-1] == 'ㅗ':
      return '', deFront[-2] + 'ㅘ'
    else:
      return deFront, deBack

# rule about '어'
def ruleOfEo(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3:
    # '업', '접' have no tallak
    if (deFront[-3] == 'ㅇ' or deFront[-3] == 'ㅈ') and deFront[-2] == 'ㅓ' and deFront[-1] == 'ㅂ':
      return deFront, deBack
    elif deFront[-1] == 'ㅂ':
      return deFront[:2], deBack[0] + 'ㅝ'
    elif deFront[-1] == 'ㅎ':
      return '', deFront[-3] + 'ㅐ'
    # Irregular about 'ㄷ' badchim of '듣'
    elif deFront[-3] == 'ㄷ' and deFront[-2] == 'ㅡ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # Irregular about 'ㄷ' badchim of '싣', '긷'
    elif (deFront[-3] == 'ㅅ' or deFront[-3] == 'ㄱ') and deFront[-2] == 'ㅣ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # Irregular about 'ㄷ' badchim of '눋', '붇', '묻'
    elif (deFront[-3] == 'ㄴ' or deFront[-3] == 'ㅂ' or deFront[-3] == 'ㅁ') and deFront[-2] == 'ㅜ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # Irregular about 'ㅅ' badchim of '긋'
    elif deFront[-3] == 'ㄱ' and deFront[-2] == 'ㅡ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    # Irregular about 'ㅅ' badchim of '젓'
    elif deFront[-3] == 'ㅈ' and deFront[-2] == 'ㅓ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    # Irregular about 'ㅅ' badchim of '잇', '짓'
    elif (deFront[-3] == 'ㅇ' or deFront[-3] == 'ㅈ') and deFront[-2] == 'ㅣ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    else:
      return deFront, deBack
  else:
    if deFront[-1] == 'ㅜ':
      return '', deFront[0] + 'ㅝ'
    elif deFront[-2] == 'ㅂ' and deFront[-1] == 'ㅣ':
      return deFront, deBack
    elif deFront[1] == 'ㅣ':
      return '', deFront[0] + 'ㅕ'
    elif deFront[-2] == 'ㄹ' and deFront[-1] == 'ㅓ':
      return '', deFront[-2] + 'ㅐ'
    elif deFront[-2] == 'ㄹ' and deFront[-1] == 'ㅡ':
      return deFront[-2], deFront[-2] + deBack[-1]
    elif deFront[-1] == 'ㅡ':
      return '', deFront[-2] + deBack[-1]
    else:
      return deFront, deBack
  
# rule about '여'
def ruleOfYeo(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if front == '하':
    return '', deFront[0] + 'ㅐ'
  else:
    return deFront, deBack

# rule about 'ㄴ', 'ㄹ', 'ㅂ'
def ruleOfConnectedBadchim(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3:
    return deFront[:-1], deBack
  else:
    return deFront, deBack

# rule about '은' 
def ruleOfEun(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3:
    if deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    elif deFront[-1] == 'ㅂ':
      return deFront[:-1], deBack[0] + 'ㅜ' + deBack[-1]
    # Irregular about 'ㄷ' badchim of '듣'
    elif deFront[-3] == 'ㄷ' and deFront[-2] == 'ㅡ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # Irregular about 'ㄷ' badchim of '싣', '긷'
    elif (deFront[-3] == 'ㅅ' or deFront[-3] == 'ㄱ') and deFront[-2] == 'ㅣ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # Irregular about 'ㄷ' badchim of '눋', '붇', '묻'
    elif (deFront[-3] == 'ㄴ' or deFront[-3] == 'ㅂ' or deFront[-3] == 'ㅁ') and deFront[-2] == 'ㅜ' and deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    else:
      return deFront, deBack
  else:
    return deFront, deBack

# rule about '는'
def ruleOfNeun(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3 and deFront[-1] == 'ㄹ':
    return deFront[:-1], deBack
  else:
    return deFront, deBack

# rule about '으'
def ruleOfNEu(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if len(deFront) == 3:
    if deFront[-1] == 'ㄷ':
      return deFront[:-1] + 'ㄹ', deBack
    # Irregular about 'ㅅ' badchim of '긋'
    elif deFront[-3] == 'ㄱ' and deFront[-2] == 'ㅡ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    # Irregular about 'ㅅ' badchim of '젓'
    elif deFront[-3] == 'ㅈ' and deFront[-2] == 'ㅓ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    # Irregular about 'ㅅ' badchim of '낫', '잣'
    elif (deFront[-3] == 'ㄴ' or deFront[-3] == 'ㅈ') and deFront[-2] == 'ㅏ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    # Irregular about 'ㅅ' badchim of '잇', '짓'
    elif (deFront[-3] == 'ㅇ' or deFront[-3] == 'ㅈ') and deFront[-2] == 'ㅣ' and deFront[-1] == 'ㅅ':
      return deFront[:-1], deBack
    else:
      return deFront, deBack
  else:
    return deFront, deBack

# router of rule
def ruleSet(front, back):
  if back in ['ㄴ', 'ㄹ', 'ㅂ']:
    return ruleOfConnectedBadchim(front, back)
  elif back == '었':
    return ruleOfEot(front, back)
  elif back == '았':
    return ruleOfAt(front, back)
  elif back == '시':
    return ruleOfSi(front, back)
  elif back == '였':
    return ruleOfYeot(front, back)
  elif back == '아':
    return ruleOfAh(front, back)
  elif back == '어':
    return ruleOfEo(front, back)
  elif back == '여':
    return ruleOfYeo(front, back)
  elif back == '은':
    return ruleOfEun(front, back)
  elif back == '는':
    return ruleOfNeun(front, back)
  elif back == '으':
    return ruleOfNEu(front, back)
  else:
    deFront = decomposition(front)
    deBack = decomposition(back)
    return deFront, deBack

# special cases
fullMorpheme = ['깨닫', '따르']
backCase = ['아', '았', '으']
def isSpecial(front, back):
  if front in fullMorpheme and back in backCase:
    return True
  else:
    return False

def specialRuleSet(front, back):
  deFront = decomposition(front)
  deBack = decomposition(back)
  if front == '닫':
    return deFront[:-1] + 'ㄹ', deBack
  elif front == '르':
    return '', 'ㄹ' + deBack[1:]
  else:
    return deFront, deBack

def specialChunkToChange(sentence):
  if '셔요' in sentence:
    return sentence.replace('셔요', '세요')
  elif '시어요' in sentence:
    return sentence.replace('시어요', '세요')
  else:
    return sentence

def composer(morphemeList):
  # After it checked, its morpheme set will be seperated into jamo-level
  # So the return variables were named dF which means decomposedFront
  # So this variable checks whether it changed
  final = 1

  # morphemeList examples below
  # morphemeList = ['알리', '어드리', 'ㄹ_것이', 'ㅂ니다']
  # morphemeList = ['뜨겁', '은데요']
  


  # Basically checking connected parts between morphemes.
  for i in range(0, len(morphemeList)-1):
    front = morphemeList[i][-final:]
    back = morphemeList[i+1][0]
    lenBack = len(morphemeList[i+1])

    if i == 0 and isSpecial(morphemeList[i], back):
      dF, dB = specialRuleSet(front, back)
    else:
      dF, dB = ruleSet(front, back)

    morphemeList[i] = morphemeList[i][:-final] + dF
    morphemeList[i+1] = dB + morphemeList[i+1][1:]

    if lenBack == 1:
      final = len(dB)
    else:
      final = 1

  morphListToString = ''.join(morphemeList)
  
  construct = reconstructor(morphListToString)

  result = specialChunkToChange(construct)
  
  return reconstructor(result)
