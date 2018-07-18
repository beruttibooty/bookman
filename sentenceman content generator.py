import random
doc = open('words.txt','r')
prepositional_phrases = doc.readline()[:-2].split('$')
base_verbs = doc.readline().split('$')[:-2]
past_verbs = doc.readline().split('$')[:-2]
translational_verbs = doc.readline()[:-2].split('$')
nouns = doc.readline()[:-2].split('$')
adjectives = doc.readline()[:-2].split('$')
adverbs = doc.readline()[:-2].split('$')

def prepositional_phrase(seed):
    random.seed(seed)
    phrase = random.choice(prepositional_phrases)
    return phrase + ','

def article(seed, plural, person):
    random.seed(seed)
    if plural: art = 'the'
    else: art = random.choice(['a/an','the'])
    return art

def adjective(seed):
    random.seed(seed)
    if random.choice([True, True, True, False]):
        adj = random.choice(adjectives)
    else:
        adj = random.choice(base_verbs) + 'ing'
    return adj

def verb(seed, person, transformative):
    random.seed(seed)
    if transformative: vrb = random.choice(translational_verbs)
    elif person == 2: vrb = random.choice(base_verbs)
    else: vrb = random.choice(past_verbs)
    return vrb

def subject(seed, plural, person, pronoun):
    random.seed(seed)
    if person == 1 and plural: sub = 'we'
    elif person == 1: sub = 'I'
    elif person == 2: sub = 'you'
    elif person == 3 and pronoun: sub = random.choice(['he','she','it'])
    elif person == 3: sub = random.choice(nouns)
    if plural and person == 3: sub += 's'
    return sub

def preposition(seed):
    random.seed(seed)
    prep = random.choice(['with','at','from','into','against','among','despite','of','to','at','in','for','on','by','about','like','through'])
    return prep

def dobject(seed, person, transformative):
    random.seed(seed)
    obj = random.choice(nouns)
    return obj

def adverb(seed):
    random.seed(seed)
    adv = random.choice(adverbs)
    return adv

def sentenceman(seed=0):
    if seed == 0: seed = random.randint(1,10000000)
    eseed = seed
    random.seed(seed)
    plural = random.choice([True,False])
    transformative = random.choice([True,False,False])
    pronoun = random.choice([True,False,False,False])
    random.seed(seed)
    person = random.randint(1,5)
    if person >= 3: person = 3
    try:
        #print(seed)

        out = []
        seed += 1
        #print((plural, transformative, pronoun, person))
        
        random.seed(seed)
        a = random.randint(0,4)
        seed += 1
        random.seed(seed)
        if a == 0: out.append(prepositional_phrase(seed))
        elif a == 4 and person == 3 and pronoun == False: out.append(article(seed, plural, person))
        elif a == 2 and plural == True and person == 3 and pronoun == False:
            out.append(adjective(seed))
        elif a == 3 and person == 2:
            transformative = True
            out.append(verb(seed, person, transformative))
        else:
            if person == 3 and pronoun == False:
                out.append(article(seed, plural, person))
                seed += 1
                random.seed(seed)
            out.append(subject(seed, plural, person, pronoun))
            a = 1
        #print(a)
        #print(out)
        seed += 1
        random.seed(seed)
        b = random.randint(0,2)
        seed += 1
        random.seed(seed)


        if a == 0:
            if b == 0 and person == 3 and pronoun == False: out.append(article(seed, plural, person))
            elif b == 1 and plural == True and person == 3:
                out.append(adjective(seed))
            seed += 1
            random.seed(seed)
            out.append(subject(seed, plural, person, pronoun))
            seed += 1
            random.seed(seed)
            if random.choice([True,False,False]): out.append(adverb(seed))
            out.append(verb(seed, person, transformative))
        elif a == 1:
            if random.choice([True,False,False]): out.append(adverb(seed))
            out.append(verb(seed, person, transformative))
        elif a == 2 or a == 4:
            out.append(subject(seed, plural, person, pronoun))
            seed += 1
            random.seed(seed)
            if random.choice([True,False,False]): out.append(adverb(seed))
            out.append(verb(seed, person, transformative))
        elif a != 3:
            if b != 0 and person == 3 and pronoun == False:
                out.append(adjective(seed))
                seed += 1
                random.seed(seed)
            out.append(subject(seed, plural, person, pronoun))
            seed += 1
            random.seed(seed)
            if random.choice([True,False,False]): out.append(adverb(seed))
            out.append(verb(seed, person, transformative))
        #print(b)
        #print(out)
        seed += 1
        random.seed(seed)
        b = random.randint(0,2)
        seed += 1
        random.seed(seed)

        if transformative:
            out.append(preposition(seed))
            seed += 1
            random.seed(seed)
        out.append(article(seed, False, person))
        seed += 1
        random.seed(seed)
        if random.choice([True,False]):
            out.append(adjective(seed))
            seed += 1
            random.seed(seed)
        out.append(dobject(seed, person, transformative))

        for i,j in enumerate(out):
            if j == 'a/an':
                if out[i+1][0] in 'aeiou': out[i] = 'an'
                else: out[i] = 'a'
            elif '/' in j:
                try:
                    k = j.split(' ')
                    index = k.index('/')
                    del k[index]
                    del k[index + random.choice([-1,1])]
                    out[i] = ' '.join(k)
                except:
                    index = j.find('/')
                    if ' ' in j: choices = [j[:j[:index].rfind(' ')]+j[index+1:],j[:index]+j[j[index+1:].find(' '):]]
                    else: choices = [j[:index],j[index+1:]]
                    out[i] = random.choice(choices)
        out[0] = out[0][0].upper() + out[0][1:]
        return ' '.join(out) + '.'
    except: return str((eseed, plural, person, pronoun, transformative))

def paragraphman(length=0):
    if length == 0:
        length = random.randint(5,100)
    out = ''
    for i in range(length):
        out += sentenceman() + ' '
    return out[:-1]

def chapterman(length=0):
    if length == 0:
        length = random.randint(1,80)
    out = ''
    for i in range(length):
        out += paragraphman() + ' \n\t'
    return out[:-1]

def bookman(length=0,seed=0,prnt=False):
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
    if prnt:
        return out
    else:
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


#######################################################################
g = {
    'a':'Ⰰ',
    'b':'Ⰱ',
    'c':'Ⰽ',
    'd':'Ⰴ',
    'e':'Ⰵ',
    'f':'Ⱇ',
    'g':'Ⰳ',
    'h':'Ⱈ',
    'i':'Ⰹ',
    'j':'Ⰻ',
    'k':'Ⰽ',
    'l':'Ⰾ',
    'm':'Ⰿ',
    'n':'Ⱀ',
    'o':'Ⱁ',
    'p':'Ⱂ',
    'q':'Ⰽ',
    'r':'Ⱃ',
    's':'Ⱄ',
    't':'Ⱅ',
    'u':'Ⱆ',
    'v':'Ⰲ',
    'w':'Ⱉ',
    'x':'Ⱈ',
    'y':'Ⱛ',
    'z':'Ⰸ',

    'zh':'Ⰶ',
    'dz':'Ⰷ',
    'dj':'Ⰼ',
    'oh':'Ⱏ',
    'sh':'Ⱋ',
    'ts':'Ⱌ',
    'ch':'Ⱍ',
    'sh':'Ⱎ',
    'ye':'ⰟⰉ',
    'eh':'Ⱐ',
    'ae':'Ⱑ',
    'jo':'Ⱖ',
    'ju':'Ⱓ',
    'en':'Ⱔ',
    'th':'Ⱚ',
    'iz':'Ⱛ',
    'ou':'Ⱆ',
    'on':'Ⱘ',

    'jon':'Ⱙ',
    }
h = {
    'a':'\u0001313f',
    'b':'\u000130c0',
    'c':'\u000133A1',
    'd':'\u00013193',
    'e':'\u0001313f',
    'f':'\u00013191',
    'g':'\u000133bc',
    'h':'\u0001339b',
    'i':'\u000131cb',
    'j':'\u00013193',
    'k':'\u000133A1',
    'l':'\u000130ed',
    'm':'\u00013153',
    'n':'\u00013216',
    'o':'\u00013171',
    'p':'\u000132aa',
    'q':'\u000133A1',
    'r':'\u0001308b',
    's':'\u000132f4',
    't':'\u000133cf',
    'u':'\u00013171',
    'v':'\u00013191',
    'w':'\u00013171',
    'x':'\u000133A1\u000132f4',
    'y':'\u000131cc',
    'z':'\u000132f4',

    '.':'   ',

    'ah':'\u0001309D',
    'sh':'\u00013219',
    'th':'\u0001340d',

    '1000':'\u000131bc',
    '2000':'\u000131bd',
    '3000':'\u000131be',
    '4000':'\u000131bf',
    '5000':'\u000131c0',
    '6000':'\u000131c1',
    '7000':'\u000131c2',
    '8000':'\u000131c3',
    '9000':'\u000131c4',
    '10000':'\u000130ad',
    '20000':'\u000130ae',
    '30000':'\u000130af',
    '40000':'\u000130b0',
    '50000':'\u000130b1',
    '60000':'\u000130b2',
    '70000':'\u000130b3',
    '80000':'\u000130b4',
    '90000':'\u000130b5',
    }

def glyphman(s,al=h,book=False):
    s = str(s)
    ll = ''
    for i,j in enumerate(s):
        if j is ll:
            s=s[:i]+'\u2407'+s[i+1:]
        else:
            ll=j
    s = ''.join(s.split('\u2407'))
    s = s.lower()

    scopy = ''
    dub = False

    for k in range(len(s)):
        if dub:
            dub = False
            continue
        try:
            dl=s[k:k+2]
            if dl in al.keys():
                scopy += al[dl]
                dub = True
            else:
                scopy += s[k]
        except:
            continue
    s = ''

    for l in range(len(scopy)):
        if scopy[l] in al.keys():
            s += al[scopy[l]]
        else:
            s += scopy[l]

    if book:
        title = 'glphman '+sentenceman()
        bok = open('{}.lbud'.format(title.replace('/','')),'w+',encoding='utf-8')
        bok.write(s)
        bok.close()
        return title
    else:
        return s

def gm(st):
    return glyphman(st,g)


































