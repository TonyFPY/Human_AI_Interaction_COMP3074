
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

import datetime as dt
import random
import re, collections 

def token_stemming(tokens):
    new_tokens = []
    sb_stemmer = SnowballStemmer('english') # using snowball stemmer
    for token in tokens:
        new_tokens.append(sb_stemmer.stem(token))
    return new_tokens

def token_lemmatisation(tokens):
    new_tokens = []
    lemmatiser = WordNetLemmatizer()
    posmap = {
        'ADJ': 'a',
        'ADV': 'r',
        'NOUN': 'n',
        'VERB': 'v'
    }
    # process the lemmatisation with tags
    post = nltk.pos_tag(tokens, tagset='universal') 
    for token in post:
        word, tag = token[0], token[1]
        if tag in posmap.keys():
            new_tokens.append(lemmatiser.lemmatize(word, posmap[tag]))
        else:
            new_tokens.append(lemmatiser.lemmatize(word))
    return new_tokens

def text_preprocessing(text, type):
    # tokenise
    text_tokens = word_tokenize(text)
    # remove stop words and special signs 
    tokens = [word.lower() for word in text_tokens if not word in stopwords.words('english') and word.isalpha()]
    # stemming or lemmatisation
    tokens = token_lemmatisation(tokens) if type == 'lemmatisation' else token_stemming(tokens)
    return (' ').join(tokens)

def time_response(str):
    date = dt.datetime.now()
    if str == 'time':
        hour = date.strftime("%H")
        minute = date.strftime("%M") 
        second = date.strftime("%S")
        print(">> Jarvis: Do you mean the current time? It's %s:%s:%s now. " %(hour,minute,second))
        if int(hour) < 6:
            print(">> Jarvis: Oh, don't wake me up! %s" %emotion())
        elif int(hour) < 11:
            print(">> Jarvis: Morning! %s" %emotion())
        elif int(hour) < 13:
            print(">> Jarvis: I am eating lunch now! %s" %emotion())
        elif int(hour) < 18:
            print(">> Jarvis: I am busy studying %s" %emotion())
        elif int(hour) < 20:
            print(">> Jarvis: I am having dinner now! %s" %emotion())
        else:
            print(">> Jarvis: I need charge now! Good night! %s" %emotion())
        
    else:
        year = date.year
        month = date.month  
        day = date.day
        print(">> Jarvis: Today is Day %s/ Month %s/ Year %s! %s" %(day, month, year, emotion()))
        
def emotion():
    e_list = ['ヽ(@ u @)ノ ','ヽ(ˋ▽ˊ)ノ','°(°ˊoˋ°) ° ','┑(￣▽ ￣)┍ ','┑(￣u ￣)┍ ',
              '╮(╯３╰)╭ ','(￣ε ￣) ','乀(ˉεˉ乀) ','ㄟ(▔皿▔ㄟ) ', '(╬▔▽▔)b ',
              '⊙﹏⊙','∩ω∩','?ω?','≧ω≦','＞ω＜',
              '(O ^ ~ ^ O)','(O ^ ~ ^ O)','o(≧ω≦)o','(￣３￣)a','(~￣▽￣)~[] ',
              '↖(^ω^)↗','~@^_^@~','\\*^o^*//','∩__∩y','★~★',
              '(^_^)∠※','(*^?^*)','<(￣︶￣)>','(#￣▽￣#) ','︿(￣︶￣)︿'
    ]
    id = random.randint(0, len(e_list)-1)
    return e_list[id]
 
import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(open("./dataset/text_check.txt", "r").read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)


if __name__ == "__main__":
    # emoji = emotion()
    # print(emoji)
    # time_response('time')
    print(correct('helllo'))