import random
import math
doc = open('words.txt','r')
prepositional_phrases = doc.readline()[:-2].split('$')
base_verbs = doc.readline().split('$')[:-2]
past_verbs = doc.readline().split('$')[:-2]
translational_verbs = doc.readline()[:-2].split('$')
nouns = doc.readline()[:-2].split('$')
people = doc.readline()[:-2].split('$')
adjectives = doc.readline()[:-2].split('$')
adverbs = doc.readline()[:-2].split('$')
names = doc.readline()[:-2].split('$')
doc.close()
words = open('words.txt','r')
words = words.read()
words = words.replace('\n',' ').replace(',','').replace('$',' ').replace('!','').replace('@','').split(' ')
interjections = ['kachow','aha','ahem','ahh','ahoy','alas','arg','aw','bam','bada bing','bada boom','bingo','blah','boo','dang','drat','duh','eek','eureka','fiddlesticks','gadzooks','gee whiz','golly','goodness','good grief','gosh','hallelujah','hey','hmm','holy smokes','holy cow','holy Toldeo','hot dog','oh dear','oh well','ouch','oops','phooey','rats','RATS','thanks','wahoo','WAHOO']

def prepositional_phrase(seed=0):
    if seed == 0: seed = random.randint(1,10000000)
    random.seed(seed)
    phrase = random.choice(prepositional_phrases)
    return phrase

def name(seed=0):
    if seed == 0: seed = random.randint(1,10000000)
    random.seed(seed)
    pro = 'he'
    if random.choice([True,True,True,True,False]):
        fname = random.choice(names)
        if '@' in fname:
            pro = 'she'
            fname = fname.replace('@','')
        if random.choice([True,True,True,False]): lname = random.choice(random.choice([nouns,adjectives])).replace(' ','')
        elif random.choice([True,False]): lname = random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')) + '.'
        else: return [fname[0].upper() + fname[1:],pro,True,False,'the']
        name = fname[0].upper() + fname[1:] + ' ' + lname[0].upper() + lname[1:]
    else:
        name = random.choice(people)
        if '@' in name:
            pro = 'she'
            name = name.replace('@','')
    return [name,pro,True,False,'the']

def noun(seed=0,plural=False,proper=False):
    if seed == 0: seed = random.randint(1,10000000)
    random.seed(seed)
    nounn = random.choice([random.choice(nouns[:100]),random.choice(nouns)])
    if proper: article = 'the'
    else: article = 'a'
    if plural:
        return [nounn+'s','they',False,proper,random.choice(['the flock of','the herd of','the','the pod of','a cluster of','a group of','an abundance of'])]
    else: return [nounn,'it',False,proper,article]

def character(seed=0,proper=None,person=None):
    if seed == 0: random.seed()
    random.seed(seed)
    character = []
    if proper == None: proper = random.choice([True, True, True, False])
    if person == None: person = random.choice([True, True, True, True, True, False])
    if proper:
        if person:
            character = name(seed)
        else:
            character = noun(seed,False,True)
    else:
        plural = random.choice([True, False, False])
        character = noun(seed,plural)
    if person: character.append(random.choice([' the '+adjective(),' of '+noun()[0]]))
    else: character.append(random.choice(adjective(seed)))
    return character

def adjective(seed=0):
    if seed == 0: seed = random.randint(1,10000000)
    random.seed(seed)
    if random.choice([True, True, True, False]):
        adj = random.choice(adjectives)
    else:
        adj = random.choice(base_verbs) + 'ing'
    return adj
    
def adverb(seed=0):
    if seed == 0: seed = random.randint(1,10000000)
    random.seed(seed)
    adv = random.choice(adverbs)
    return adv

def preposition(seed=0):
    if seed == 0: seed = random.randint(1,10000000)
    random.seed(seed)
    prep = random.choice(['at','from','into','against','despite','to','at','in','for','on','by','about','through'])
    return prep

def verb(data=None,seed=0):
    #print(data)
    if seed == 0: seed = random.randint(1,10000000)
    random.seed(seed)
    advb = random.choice([True,True,True,False])
    adv = ''
    if advb:
        adv = adverb(seed) + ' '
    if data == None: verb = random.choice(past_verbs)
    elif 'targeted' in data: verb = random.choice(['high-fived','slam-dunked','balled','talked up','amazed','astonished','intrigued','bored','discussed with'])
    elif 'dialogue' in data: verb = random.choice(['whispered','shouted','yelled','said','chanted'])
    elif 'sec' in data: verb = random.choice(['run','go','walk','carry'])
    elif 'trans' in data:
        verb = random.choice(['became','was','is no longer'])
        adv = ''
    elif 'loc' in data: verb = random.choice(translational_verbs)
    elif 'exchange' in data: verb = random.choice(['gave','handed','slid','delivered to'])
    else: verb = random.choice(past_verbs)
    return adv + verb

def L():
    return

def sentencewoman(seed=0,stype=0,characters=None,context=[]):
    if seed == 0: seed = random.randint(1,10000000)
    #print(seed)
    eseed = seed
    random.seed(seed)
    
    # generate word order #
    sentence = []
    if stype == 0: stype = random.choice([1,2,2,2,3,4,4,5,5])
    if stype == 1: #quote
        sentence = random.choice([
            [['quote'],['sub'],['verb','dialogue']],
            [['sub'],['verb','dialogue'],['quote']]
            ])
    elif stype == 2: #reg
        sentence = random.choice([
            [['depcl'],['prepphrase','sub'],['art','sub'],['adj','sub'],['sub'],['verb','targeted'],['art','obj'],['adj','obj'],['obj'],['prepphrase','obj']],
            [['depcl'],['art','sub'],['adj','sub'],['sub'],['verb','loc'],['prepphrase','sub']]
            ])
    elif stype == 3: #exchange
        sentence = ['depcl'],['prepphrase','sub'],['art','sub'],['adj','sub'],['sub'],['verb','exchange'],['art','obj'],['adj','obj'],['obj'],['art','dobj'],['adj','dobj'],['dobj'],['prepphrase','obj']
    elif stype == 4: #description
        sentence = random.choice([
            [['art','sub'],['sub'],['verb','trans'],['adj','desc']],
            [['depcl'],['prepphrase','sub'],['art','sub'],['sub'],['verb','trans'],['adj','desc'],['prepphrase','sub']]
            ])
    elif stype == 5: #transitive
        sentence = random.choice([
            [['art','sub'],['sub'],['conj'],['art','obj'],['obj'],['verb','loc'],['prepphrase','sub']],
            [['art','sub'],['sub'],['verb','loc'],['prep','loc'],['art'],['adj'],['noun'],['prep','conj'],['art','obj'],['obj']]
            ])
    elif stype == 6: #interjection
        sentence = random.choice([['verb'],['noun'],['name'],['interjection'],['interjection'],['interjection']])
    elif stype == 7: #command
        sentence = random.choice([[['verb','sec','trans'],['prepphrase','obj']],[['verb','sec'],['art','obj'],['obj']]])
    #print(sentence)
    #print((seed,stype))

    # add words #
    if characters == None: characters = [character(seed,True,True),character(seed,True,True),character(seed,False),character(seed)]
    if ['obj'] in sentence and ['sub'] in sentence and len(characters) == 1: characters.append(character(seed+1))
    objectitem = []
    subjectitem = []
    intersentence = [None]*len(sentence)
    #print(characters)

    subjectitem = []
    objectitem = []
    for i,j in enumerate(sentence):
        seed += 1
        try:
            if j[0] == 'depcl':
                if random.choice([True,False,False,False]):
                    randomchar = name()
                    intersentence[i] = random.choice([
                        ['Ever since the {} invaded,'.format(noun()[0])],
                        ['Ever since the {} became involved with the investigation,'.format(noun()[0])],
                        ['On the eve of {} day,'.format(noun()[0])],
                        ['Having not been able to stand up alone,'.format(noun()[0])],
                        ['With a great consideration of the law,'.format(noun()[0])],
                        ['Based on a popular novel,'.format(noun()[0])],
                        ["{} really couldn't believe what {} saw:".format(randomchar[0],randomchar[1])]
                        ])
                else:
                    intersentence[i] = ['']
            elif j[0] == 'prepphrase':
                if 1==1:#random.choice([True,False,False,False]):
                    intersentence[i] = [prepositional_phrase(seed).replace('@',str(noun(seed)[0])).replace('!',adjective(seed)).replace('#',str(random.randint(1,10000000)))]#['by land, air, and sea,']
                else:
                    intersentence[i] = ['']
            elif j[0] == 'sub' or j[0] == 'obj':
                #print(characters)
                item = random.choice(characters)
                if item[2]:
                    intersentence[i] = ['named']
                if (item == subjectitem or item == objectitem) and stype != 5:
                    if item[1] == 'he':
                        intersentence[i] = ['himself']
                    elif item[1] == 'she':
                        intersentence[i] = ['herself']
                    else: intersentence[i] = ['itself']
                elif item == subjectitem or item == objectitem:
                    while item == subjectitem or item == objectitem:
                        item = random.choice(characters)
                    if item[2]: intersentence[i] = random.choice([item,item,item,[item[0]+item[-1]]])
                    else: intersentence[i] = item
                else:
                    if item[2]: intersentence[i] = random.choice([item,item,item,[item[0]+item[-1]]])
                    else: intersentence[i] = item
                if j[0] == 'sub': subjectitem = item
                else: objectitem = item
        except Exception as e: print(e)
    
    for k,m in enumerate(sentence):
        seed += 1
        try:
            if m[0] == 'art':
                if sentence[k+1] == ['name'] or sentence[k+1] == ['named']:
                    intersentence[k] = ['']
                    continue
                try:
                    if subjectitem[2] and not objectitem[2]:
                        intersentence[k] = ['its']
                        if subjectitem[1] == 'he':
                            intersentence[k] = ['his']
                        else:
                            intersentence[k] = ['her']
                        continue
                except:
                    L()
                if len(m) == 1:
                    intersentence[k] = ['the']
                    continue
                elif m[1] == 'sub':
                    n = subjectitem
                elif m[1] == 'obj':
                    n = objectitem
                    if objectitem == subjectitem:
                        intersentence[k] = ['']
                        continue
                else:
                    n = [None,None,False,False,'the']
                if n[3] or (n[2] and random.choice([False,False,False,False,True])) or (not n[2] and random.choice([False,True,True])):
                    intersentence[k] = [n[4]]
                    continue
                intersentence[k] = ['']
                if intersentence[k] == None: intersentence[k] = ['']
            elif m[0] == 'adj':
                if len(m) == 1:
                    intersentence[k] = [adjective(seed)]
                    if intersentence[k-1] == 'a' and intersentence[k][0] in 'aeiouy': intersentence[k-1] = 'an'
                    continue
                elif m[1] == 'sub': n = subjectitem
                elif m[1] == 'obj': n = objectitem
                else:
                    intersentence[k] = [adjective(seed)]
                    if intersentence[k-1] == 'a' and intersentence[k][0] in 'aeiouy': intersentence[k-1] = 'an'
                    continue
                if (intersentence[k-1] != [''] and intersentence[k-1] != None):
                    if not n[2] or random.choice([False,False,True]): intersentence[k] = [adjective(seed)]
                    else:
                        intersentence[k] = ['']
                else:
                    intersentence[k] = ['']
                if intersentence[k-1] == 'a' and intersentence[k][0] in 'aeiouy': intersentence[k-1] = 'an'
            elif m[0] == 'verb':
                intersentence[k] = [verb(m)]
            elif m[0] == 'dobj':
                intersentence[k] = noun()
            elif m[0] == 'quote':
                length = random.randint(1,5)
                quote = []
                qchars = characters + character(seed) + character(seed) + character(seed)
                for n in range(length):
                    qtype = random.randint(2,6)
                    qsent = sentencewoman(seed,qtype,None)
                    quote.append(qsent)
                    #print(qsent)
                    seed += 1
                intersentence[k] = ['"{}"'.format(' '.join(quote))]
            elif m[0] == 'name':
                intersentence[k] = [name(seed)[0]]
            elif m[0] == 'noun':
                intersentence[k] = [noun(seed)[0]]
                if intersentence[k-1] == 'a' and intersentence[k][0] in 'aeiouy': intersentence[k-1] = 'an'
            elif m[0] == 'conj':
                intersentence[k] = ['and']
            elif m[0] == 'prep':
                if m[1] == 'loc': intersentence[k] = [preposition(seed)]
                elif m[1] == 'conj': intersentence[k] = [random.choice(['with','along with','by the side of','hand-in-hand with','with','with','by way of'])]
                else: intersentence[k] = ['']
            elif m[0] == 'interjection':
                intersentence[k] = random.choice(interjections)
            elif m[0] == 'named':
                continue
        except Exception as e: print(e)
    #print(intersentence)
    out = []
    for z in intersentence:
        try:
            if z == None: out.append(random.choice(interjections))
            elif z != ['']: out.append(str(z[0]))
        except: continue
    sent = ' '.join(out).replace('â€™',"'")
    if sent[-1] == ',':
        sent = sent[:-1]
    if random.choice([False,False,False,False,True]) and ';' not in sent:
        nsent = str(sentencewoman(seed,0,characters))
        sent += '; ' + nsent#[0].lower() + nsent[1:]
    elif sent[-1] != '"':
        sent += random.choice(['.','.','.','.','.','.','.','.','.','.','.','!'])
    sent = sent.replace(' a a',' an a').replace(' a e',' an e').replace(' a i',' an i').replace(' a o',' an o').replace(' a u',' an u').replace(' a y',' an y')
        
    return sent[0].upper() + sent[1:]

def paragraphwoman(seed=0,chars=None):
    if seed == 0: seed = random.randint(1,10000000)
    random.seed(seed)
    if chars == None:
        characterlist = []
        for i in range(4):
            seed += 1
            characterlist.append(character(seed,True,True))
    else: characterlist = chars
    paragraph = []
    for j in range(10):
        c = characterlist
        seed += 1
        paragraph.append(sentencewoman(seed,0,c))
    return ' '.join(paragraph)

def chapterwoman(seed=0,chars=None,chapnum=1):
    chapter = []
    title = ' '.join(['Chapter {}: '.format(chapnum),random.choice(['the','a']),random.choice(adjectives),random.choice(nouns),'\n\n'])
    chapter.append(title)
    for i in range(random.randint(1,20)):
        seed += 1
        chapter.append('\n\n\t'+paragraphwoman(seed,chars))
    return ' '.join(chapter)

def bookwoman(seed=0,chapters=10,characters=4):
    if seed == 0: seed = random.randint(1,10000000)
    eseed = seed
    random.seed(seed)
    if chapters == 0:
        chapters = random.randint(5,30)
    characterlist = []
    for i in range(characters):
        seed += 1
        characterlist.append(character(seed,True,True))
    book = []
    for j in range(chapters):
        seed += 1
        book.append('\n\n\n'+chapterwoman(seed,random.choice([characterlist,characterlist,characterlist,characterlist,None]),j+1))
    title = characterlist[0][0] + "'s " + random.choice(adjectives) + ' ' + random.choice(nouns)
    file = open('{}.txt'.format(title.replace('/','')),'w+')
    file.write(title + '\n\n' + '\n\t'.join(book) + ' Thank You.')
    file.close()
    return title + ', by Bookwoman'

def wordmaster(duration=600,minimum=1,maximum=15,seed=0,prin=True):
    import time
    import math
    dic = open('dictionary.txt','r+')
    dicdata = dic.read()
    dic.close()
    if seed == 0: random.seed()
    else: random.seed(seed)
    iterations = 0
    start = time.time()
    words = []
    key = ['a']*8+['b']*1+['c']*3+['d']*4+['e']*12+['f']*2+['g']*2+['h']*6+['i']*7+['j']*1+['k']*1+['l']*4+['m']*2+['n']*7+['o']*8+['p']*2+['q']*1+['r']*6+['s']*6+['t']*9+['u']*3+['v']*1+['w']+['x']*1+['y']*2+['z']*1
    key = key * 4 + list('1234567890-. ')
    while time.time()-start < duration:
        iterations += 1
        word = ''
        length = random.randint(minimum,maximum)
        for i in range(length):
            word += random.choice(key)
        if '\n{}\n'.format(word) in dicdata.lower():
            if prin:
                space = int(20*math.sin(iterations/27)**2+50*math.cos(iterations/100)**2)
                print('█'*space+'▒'*int(1+3*math.sin(iterations/45)**2)+'░'*int(8*math.sin(iterations/35)**2)+'▒'*int(1+3*math.sin(iterations/45)**2)+'█'*(80-space-int(8*math.sin(iterations/35)**2)-2*int(1+3*math.sin(iterations/45)**2))+str(iterations)+' '+word)
            word = dicdata[dicdata.lower().find('\n{}\n'.format(word).lower())+1:dicdata.lower().find('\n{}\n'.format(word).lower())+len(word)+1]
            doc = open('wordmaster.txt','r+')
            data = doc.read()
            doc.close()
            if word not in data:
                data += word + '\n'
                doc = open('wordmaster.txt','w')
                doc.write(data)
                doc.close()
                words.append(word)
        elif prin:
            space = int(20*math.sin(iterations/27)**2+50*math.cos(iterations/100)**2)
            print('░'*space+'▒'*int(1+3*math.sin(iterations/45)**2)+'█'*int(8*math.sin(iterations/35)**2)+'▒'*int(1+3*math.sin(iterations/45)**2)+'░'*(80-space-int(8*math.sin(iterations/35)**2)-2*int(1+3*math.sin(iterations/45)**2))+str(iterations)+' '+word)
    return print('{} new words: {}'.format(iterations,str(words)))

def sentencegod(seed=0,minimum=1,prin=True):
    import time
    import math
    if seed == 0: random.seed()
    else: random.seed(seed)
    score = 0
    iterations = 0
    start = time.time()
    sentence = ''
    while (score == None or score < 50 or score > 95) and time.time()-start < 10:
        iterations += 1
        sentence = ''
        length = random.randint(minimum,15)
        for i in range(length):
            sentence += random.choice(words) + ' '
        score = autograde(sentence)
        if prin: print(' '*int(10*math.sin(iterations/20)**2+10*math.cos(iterations/50)**2)+'0'+' '*(25-int(10*math.sin(iterations/20)**2+10*math.cos(iterations/50)**2))+str(iterations)+' '+sentence)
    end = time.time()
    time = end-start
    #if prin: return 'After {} second and {} iterations, sentencegod has produced the following sentence at the rank of {}: {}'.format(time,iterations,score,sentence)
    sentence = sentence[0].upper() + sentence[1:] + '.'
    return sentence

def sentencegodtrainer(questions=200):
    import time
    import math
    random.seed()
    sg1 = sentencegod()
    sent1 = sg1
    score1 = autograde(sg1)
    sg2 = sentencegod()
    sent2 = sg2
    score2 = autograde(sg2)
    for i in range(questions):
        print('1: ' + sent1 + '\n2: ' + sent2 + '\n - question ' + str(i))
        reset = input('Which should refresh? ')
        inputint = False
        while not inputint:
            try:
                reset = int(reset)
                assert(reset in [1,2])
                inputint = True
            except: reset = input('Which should refresh? (1 or 2) ')
        score = input('What would you score the sentence? ')
        doc = open('fitnessdata.txt','r+')
        data = doc.read()
        doc.close()
        if reset == 1:
            data += '{}@{}$'.format(sent1,score)
            input('We predicted the score to be {}'.format(score1))
            sg1 = sentencegod()
            sent1 = sg1[0]
            score1 = float(sg1[1])
        else:
            data += '{}@{}$'.format(sent2,score)
            input('We predicted the score to be {}'.format(score2))
            sg2 = sentencegod()
            sent2 = sg2[0]
            score2 = float(sg2[1])
        doc = open('fitnessdata.txt','w')
        doc.write(data)
        doc.close()
    print(sent1 + ' | ' + sent2)
    reset = input('Which should refresh? ')
    inputint = False
    while not inputint:
        try:
            reset = int(reset)
            assert(reset in [1,2])
            inputint = True
        except: continue
    score = input('What would you score the sentence? ')
    doc = open('fitnessdata.txt','r+')
    data = doc.read()
    doc.close()
    if reset == 1:
        data += '{}@{}$'.format(sent1,score)
        input('We predicted the score to be {}'.format(score1))
        score = input('What would you score the winning sentence? ')
        data += '{}@{}$'.format(sent2,score)
        input('We predicted that score to be {}'.format(score2))
    else:
        data += '{}@{}$'.format(sent2,score)
        input('We predicted the score to be {}'.format(score2))
        score = input('What would you score the winning sentence? ')
        data += '{}@{}$'.format(sent1,score)
        input('We predicted that score to be {}'.format(score1))
    return 'Complete.'

def sentencegodtrainer2(questions=200,mutations=1):
    import time
    import math
    random.seed()
    sg = sentencegod(0,5)
    sent1 = sg
    score1 = autograde(sent1)
    sent2 = sent1.split(' ')
    sent2[random.randint(0,len(sent2)-1)] = random.choice(words)
    sent2 = ' '.join(sent2)
    score2 = autograde(sent2)
    for i in range(questions):
        print('1: ' + sent1 + '\n2: ' + sent2 + '\n - question ' + str(i))
        reset = input('Which should refresh? ')
        inputint = False
        while not inputint:
            try:
                reset = int(reset)
                assert(reset in [1,2])
                inputint = True
            except: reset = input('Which should refresh? (1 or 2) ')
        score = input('What would you score the sentence? ')
        doc = open('fitnessdata.txt','r+')
        data = doc.read()
        doc.close()
        if reset == 1:
            data += '{}@{}$'.format(sent1,score)
            input('We predicted the score to be {}'.format(score1))
            sent1 = sent2.split(' ')
            for j in range(mutations):
                sent1[random.randint(0,len(sent1)-1)] = random.choice(words)
            sent1 = ' '.join(sent1)
            score1 = autograde(sent1)
        else:
            data += '{}@{}$'.format(sent2,score)
            input('We predicted the score to be {}'.format(score2))
            sent2 = sent1.split(' ')
            for j in range(mutations):
                sent2[random.randint(0,len(sent2)-1)] = random.choice(words)
            sent2 = ' '.join(sent2)
            score2 = autograde(sent2)
        doc = open('fitnessdata.txt','w')
        doc.write(data)
        doc.close()
    print('1: ' + sent1 + '\n2: ' + sent2 + '\n - question ' + str(i + 1))
    reset = input('Which should refresh? ')
    inputint = False
    while not inputint:
        try:
            reset = int(reset)
            assert(reset in [1,2])
            inputint = True
        except: continue
    score = input('What would you score the sentence? ')
    doc = open('fitnessdata.txt','r+')
    data = doc.read()
    doc.close()
    if reset == 1:
        data += '{}@{}$'.format(sent1,score)
        input('We predicted the score to be {}'.format(score1))
        score = input('What would you score the winning sentence? ')
        data += '{}@{}$'.format(sent2,score)
        input('We predicted that score to be {}'.format(score2))
    else:
        data += '{}@{}$'.format(sent2,score)
        input('We predicted the score to be {}'.format(score2))
        score = input('What would you score the winning sentence? ')
        data += '{}@{}$'.format(sent1,score)
        input('We predicted that score to be {}'.format(score1))
    return 'Complete.'

def mutatesentence(sent):
    sent = sent.split(' ')
    if random.choice([True,True,True,True,False]):
        try: sent[random.randint(0,len(sent)-1)] = random.choice(words)
        except: sent[random.randint(0,len(sent)-2)] = random.choice(words)
    else:
        if random.choice([True,False,False]) and len(sent) > 5:
            print('r')
            try: sent[random.randint(0,len(sent)-1)] = ''
            except: sent[random.randint(0,len(sent)-2)] = ''
        elif len(sent) < 15:
            n = random.randint(0,len(sent)-1)
            try: sent = sent[:n] + [random.choice(words)] + sent[n:]
            except: sent += random.choice(words)
    return ' '.join(sent)

def autosentencegodtrainer2(duration=300,mutations=1):
    import time
    import math
    random.seed()
    sg = sentencegod(0,5)
    sent1 = sg
    score1 = autograde(sent1)
    sent2 = sent1.split(' ')
    sent2[random.randint(0,len(sent2)-1)] = random.choice(words)
    sent2 = mutatesentence(sent1)
    score2 = autograde(sent2)
    start = time.time()
    iterations = 0
    lastwinner = 1
    win_count = 0
    doc = open('autofitnessdata.txt','r+')
    data = doc.read()
    doc.close()
    while time.time()-start < duration:
        iterations += 1
        curwinner = 0
        space = int(5*math.sin(iterations/27)**2+10*math.cos(iterations/100)**2)
        if score1 == score2:
            if random.choice([True,False]):
                curwinner = 2
                data += '{}@{}$'.format(sent1,score1)
                sent1 = mutatesentence(sent2)
                while score1 == None:
                    sent1 = mutatesentence(sent2)
                    score1 = autograde(sent1)
                print('|' + '='*space + '#'*int(1+4*math.sin(iterations/35)**2) + '='*(20-int(space+1+4*math.sin(iterations/35)**2)) + '| ' + str(iterations) + ' ' + sent2 + ' ' + str(score2))
            else:
                curwinner = 1
                data += '{}@{}$'.format(sent2,score2)
                sent2 = mutatesentence(sent1)
                while score2 == None:
                    sent2 = mutatesentence(sent1)
                    score2 = autograde(sent2)
                print('|' + '+'*space + '-'*int(1+4*math.sin(iterations/35)**2) + '+'*(20-int(space+1+4*math.sin(iterations/35)**2)) + '| ' + str(iterations) + ' ' + sent1 + ' ' + str(score1))
        elif score2*10 > score1*10:
            curwinner = 2
            data += '{}@{}$'.format(sent1,score1)
            sent1 = mutatesentence(sent2)
            while score1 == None:
                sent1 = mutatesentence(sent2)
                score1 = autograde(sent1)
            print('|' + '-'*space + '+'*int(1+4*math.sin(iterations/35)**2) + '-'*(20-int(space+1+4*math.sin(iterations/35)**2)) + '| ' + str(iterations) + ' ' + sent2 + ' ' + str(score2))
        else:
            curwinner = 1
            data += '{}@{}$'.format(sent2,score2)
            sent2 = mutatesentence(sent1)
            while score2 == None:
                sent2 = mutatesentence(sent1)
                score2 = autograde(sent2)
            print('|' + '+'*space + '-'*int(1+4*math.sin(iterations/35)**2) + '+'*(20-int(space+1+4*math.sin(iterations/35)**2)) + '| ' + str(iterations) + ' ' + sent1 + ' ' + str(score1))
        if curwinner == lastwinner:
            win_count += 1
        else:
            win_count = 0
        if win_count > 50:
            if curwinner == 1:
                data += '{}@{}$'.format(sent1,score1)
                sent1 = mutatesentence(sent2)
                while score1 == None:
                    sent1 = mutatesentence(sent2)
                    score1 = autograde(sent1)
            else:
                data += '{}@{}$'.format(sent2,score2)
                sent2 = mutatesentence(sent1)
                while score2 == None:
                    sent2 = mutatesentence(sent1)
                    score2 = autograde(sent2)
            win_count = 0
    data += '{}@{}$'.format(sent1,score1)
    data += '{}@{}$'.format(sent2,score2)
    doc = open('autofitnessdata.txt','w')
    doc.write(data)
    doc.close()
    if score2 > score1:
        print(sent2+' wins with a score of '+str(score2))
    else:
        print(sent1+' wins with a score of '+str(score1))
    return 'Complete.'

def g():
    return autosentencegodtrainer2()

def create_set(string):
    string = string.lower().replace(',','').replace(';','').replace('.','').replace('"','')
    strlist = ['$']
    strlist.extend(string.split(' '))
    strlist.append('$')
    data = []
    for i in range(int(round(len(strlist)/2))):
        try: data.append(' '.join([strlist[2*i],strlist[2*i+1]]))
        except Exception as e: continue
    for i in range(int(round(len(strlist)/2))):
        try: data.append(' '.join([strlist[2*i+1],strlist[2*i+2]]))
        except Exception as e: continue
    return data

def overlap(st1, st2):
    st1 = create_set(st1)
    st2 = create_set(st2)
    intersection = 0
    for i in st1:
        if i in st2: intersection += 1
    return (intersection/max(len(st1),len(st2)))

def autograde(string):
    doc = open('fitnessdata.txt','r+')
    data = doc.read()
    doc.close()
    data = data.split('$')[:-1]
    table = []
    nset = 0.0
    dset = 0.0
    matches = 0
    for i,j in enumerate(data):
        anom = False
        if '*' in j: anom = True
        data[i] = j.replace('*','').split('@')
        if anom: ovl = overlap(string,data[i][0])**(1/2)
        else: ovl = overlap(string,data[i][0])
        if ovl <= 0.01: continue
        matches += 1
        nset += ovl*float(data[i][1])
        dset += ovl
        table.append(data[i]+[ovl])
    if matches <= 4: return None
    try: return nset/dset
    except: None
    
def fitness(length=10):
    print('time to conduct the fitness gram pacer test.')
    doc = open('fitnessdata.txt','r+')
    data = doc.read()
    doc.close()
    testdata = ''
    for i in range(length):
        sent = sentencewoman()
        predrank = autograde(sent)
        while predrank == None or predrank < 50:
            sent = sentencewoman()
            predrank = autograde(sent)
        print(sent)
        rank = input('Rating: ')
        if predrank == None: print('Anomaly: no base for predicted rank\n'.format(predrank,rank))
        elif math.fabs(float(rank)- predrank) >= 20:
            print('Anomaly: predicted score was {} and actual score was {}\n'.format(predrank,rank))
            testdata += '*'
        else: print('Submitted at {} with predicted score of {}\n'.format(rank,predrank))
        testdata += '{}@{}$'.format(sent,rank)
    doc = open('fitnessdata.txt','w')
    data += testdata
    doc.write(data)
    doc.close()
    return 'Complete'

def autofitness(assist=False, length=4096):
    print('Time to automatically conduct the fitness gram pacer test.')
    doc = open('autofitnessdata.txt','r+')
    data = doc.read()
    doc.close()
    testdata = ''
    best = ''
    bestscore = 0
    avg = 0
    for i in range(length):
        sent = sentencewoman()
        rank = autograde(sent)
        if rank == None and assist:
            print(sent)
            rank = input('score: ')
            if not rank.isalpha():
                assist = False
                continue
        elif rank == None:
            while rank == None:
                sent = sentencewoman()
                rank = autograde(sent)
        avg += rank
        if rank > bestscore:
            bestscore = rank
            best = sent
        testdata += '{}@{}$'.format(sent,rank)
    avg = avg/length
    doc = open('autofitnessdata.txt','w')
    data += testdata
    doc.write(data)
    doc.close()
    return 'Complete. Average score is {}. The best sentence was {} with a score of {}.'.format(avg,best,bestscore)




def article(seed, plural, person):
    random.seed(seed)
    if plural: art = 'the'
    else: art = random.choice(['a/an','the'])
    return art

def dobject(seed, person, transformative):
    random.seed(seed)
    obj = random.choice(nouns)
    return obj

def chapterman(length=0):
    if length == 0:
        length = random.randint(1,80)
    out = ''
    for i in range(length):
        out += paragraphwoman() + ' \n\t'
    return out[:-1]

def bookman(length=0,seed=0):
    if seed == 0: seed = random.randint(1,10000000)
    eseed = seed
    random.seed(seed)
    if length == 0:
        length = random.randint(10,70)
    out = ''
    prep = random.choice(['','',random.choice(['of','from','in','by','is'])+' '+article(random.randint(2,2390), False, 3).upper()+' '+dobject(random.randint(5,92837),3,False).upper(),random.choice(['in','of'])+' '+adjective(random.randint(3,37821)).upper()])
    title = [article(random.randint(2,2390), False, 3).upper(),adjective(random.randint(3,37821)).upper(),dobject(random.randint(5,92837),3,False).upper()]
    title.extend(prep.split(' '))
    for i,j in enumerate(title):
        if j == 'A/AN':
            if title[i+1][0] in 'aeiou': title[i] = 'AN'
            else: title[i] = 'A'
    title = ' '.join(title).strip()
    for k in range(73*22):
        out += random.choice(['-','_','+','=','/','<','>','|','\\','@','#','$','%','^','&','(',')','!','?'])
        if (k + 1) % 73 == 0: out += '\n'
    out += '\n\n\n\n\t\t{}, by Bookman\n\n'.format(title)
    description = 'A {} story in {} chapters about {} {}s'.format(adjective(random.randint(3,37821)), length, adjective(random.randint(1,63421)), dobject(random.randint(5,92837),3,False))
    out += '\t\t' + description + '\n\n\n\n'
    for l in range(73*22):
        out += random.choice(['-','_','+','=','/','<','>','|','\\','@','#','$','%','^','&','(',')','!','?'])
        if (l + 1) % 73 == 0: out += '\n'
    out += '\f'
    for m in range(length):
        chapter = 'CHAPTER {}: {} {} {}'.format(m+1,article(random.randint(2,2390), False, 3),adjective(random.randint(3,37821)),dobject(random.randint(5,92837),3,False))
        out += '\n\n\n\n\n\n\n\n\n\n\n\n\n{}\n\n\n'.format(chapter)
        out += chapterman() + ' \f\t'
        print(chapter)
    book = open('{}.txt'.format(title.replace('/','')),'w+')
    book.write(out + '\f' + aboutbookman(eseed))
    book.close()
    return '{} by Bookman - {}'.format(title, description)
    
def aboutbookman(eseed=0):
    portrait = '''
@-------------------------------------------------------@
|                                                       |
|                     __,.,.,.,.,._                     |
|             .,-.,_,.__,-,.,.-_,.,-_                   |
|           :,.;,--,.'-_,'-;=,'-,.;',-',;-              |
|        ,',-;',.,,.'-=-';';;',',.',.=';-,=''-          |
|       ;',.;.,'--',;.'-;',-.;,-'.;-';,'..;;'',,        |
|       :",',.';,';,';,';,;';   ';,' ,';,' ''; ,'       |
|      ';, ',.';,'; ';,',         .   '; ,   , '        |
|      ',;,.';,';,,.                                    |
|       ,.'';,.;,.         ,';,.,.';    ';,',.          |
|        ,;'.,';                                        |
|        ';,.';,.            < 0>      |  < 0>          |
|         ,,;,;.                       |                |
|         ., ;'                        |                |
|                                   /___\               |
|                             ,./,/.,/.,/.,/,           |
|                             ,. ---------- .           |
|                             .,                        |
|                              ..  .,./,/. .            |
|                                .,,.,.,.,.             |
|                                                       |
@------------------------bookman------------------------@
    '''
    return 'ABOUT THE AUTHOR \n{}\n\nBookman likes to write books. For this book, he used the seed {}.'.format(portrait,eseed)

