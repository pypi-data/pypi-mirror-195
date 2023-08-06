import json
import pandas as pd
import emoji
import wordfreq
import string
import re

def replace_contraction(string):
    contractions_dict=contractions()
    string=string.lower()
    for s in string.split(' '):
        if s in contractions_dict.keys():
            string=string.replace(s,contractions_dict[s])
    return string

def replace_abbreviations(string):
    abbreviations_dict=abbreviations()
    string=string.lower()
    for s in string.split(' '):
        if s in abbreviations_dict.keys():
            string=string.replace(s,abbreviations_dict[s])
    return string

def remove_emoji(string):
    emoji_list=[c for c in string if c in emoji.EMOJI_DATA]
    for e in emoji_list:
        string=string.replace(e,'')
    return string

def replace_emoji(string):
    emoji_dict=emojis()
    emoji_list=[c for c in string if c in emoji.EMOJI_DATA]
    for e in emoji_list:
        if e in string and e in emoji_dict.keys():
            string=string.replace(e,emoji_dict[e])
    return string

def abbreviations():
    abb={"$": "dollar", "4ao": "for adults only", "a.m": "before midday", "a3": "anytime anywhere anyplace", "aamof": "as a matter of fact", "acct": "account", "adih": "another day in hell", "afaic": "as far as i am concerned", "afaict": "as far as i can tell", "afaik": "as far as i know", "afair": "as far as i remember", "afk": "away from keyboard", "app": "application", "approx": "approximately", "apps": "applications", "asap": "as soon as possible", "asl": "age, sex, location", "atk": "at the keyboard", "ave.": "avenue", "aymm": "are you my mother", "ayor": "at your own risk", "b&b": "bed and breakfast", "b+b": "bed and breakfast", "b.c": "before christ", "b2b": "business to business", "b2c": "business to customer", "b4": "before", "b4n": "bye for now", "b@u": "back at you", "bae": "before anyone else", "bak": "back at keyboard", "bbbg": "bye bye be good", "bbc": "british broadcasting corporation", "bbias": "be back in a second", "bbl": "be back later", "bbs": "be back soon", "be4": "before", "bfn": "bye for now", "blvd": "boulevard", "bout": "about", "brb": "be right back", "bros": "brothers", "brt": "be right there", "bsaaw": "big smile and a wink", "btw": "by the way", "bwl": "bursting with laughter", "c/o": "care of", "cet": "central european time", "cf": "compare", "cia": "central intelligence agency", "csl": "can not stop laughing", "cu": "see you", "cul8r": "see you later", "cv": "curriculum vitae", "cwot": "complete waste of time", "cya": "see you", "cyt": "see you tomorrow", "dae": "does anyone else", "dbmib": "do not bother me i am busy", "diy": "do it yourself", "dm": "direct message", "dwh": "during work hours", "e123": "easy as one two three", "eet": "eastern european time", "eg": "example", "embm": "early morning business meeting", "encl": "enclosed", "encl.": "enclosed", "etc": "and so on", "faq": "frequently asked questions", "fawc": "for anyone who cares", "fb": "facebook", "fc": "fingers crossed", "fig": "figure", "fimh": "forever in my heart", "ft.": "feet", "ft": "featuring", "ftl": "for the loss", "ftw": "for the win", "fwiw": "for what it is worth", "fyi": "for your information", "g9": "genius", "gahoy": "get a hold of yourself", "gal": "get a life", "gcse": "general certificate of secondary education", "gfn": "gone for now", "gg": "good game", "gl": "good luck", "glhf": "good luck have fun", "gmt": "greenwich mean time", "gmta": "great minds think alike", "gn": "good night", "g.o.a.t": "greatest of all time", "goat": "greatest of all time", "goi": "get over it", "gps": "global positioning system", "gr8": "great", "gratz": "congratulations", "gyal": "girl", "h&c": "hot and cold", "hp": "horsepower", "hr": "hour", "hrh": "his royal highness", "ht": "height", "ibrb": "i will be right back", "ic": "i see", "icq": "i seek you", "icymi": "in case you missed it", "idc": "i do not care", "idgadf": "i do not give a damn fuck", "idgaf": "i do not give a fuck", "idk": "i do not know", "ie": "that is", "i.e": "that is", "ifyp": "i feel your pain", "IG": "instagram", "iirc": "if i remember correctly", "ilu": "i love you", "ily": "i love you", "imho": "in my humble opinion", "imo": "in my opinion", "imu": "i miss you", "iow": "in other words", "irl": "in real life", "j4f": "just for fun", "jic": "just in case", "jk": "just kidding", "jsyk": "just so you know", "l8r": "later", "lb": "pound", "lbs": "pounds", "ldr": "long distance relationship", "lmao": "laugh my ass off", "lmfao": "laugh my fucking ass off", "lol": "laughing out loud", "ltd": "limited", "ltns": "long time no see", "m8": "mate", "mf": "motherfucker", "mfs": "motherfuckers", "mfw": "my face when", "mofo": "motherfucker", "mph": "miles per hour", "mr": "mister", "mrw": "my reaction when", "ms": "miss", "mte": "my thoughts exactly", "nagi": "not a good idea", "nbc": "national broadcasting company", "nbd": "not big deal", "nfs": "not for sale", "ngl": "not going to lie", "nhs": "national health service", "nrn": "no reply necessary", "nsfl": "not safe for life", "nsfw": "not safe for work", "nth": "nice to have", "nvr": "never", "nyc": "new york city", "oc": "original content", "og": "original", "ohp": "overhead projector", "oic": "oh i see", "omdb": "over my dead body", "omg": "oh my god", "omw": "on my way", "p.a": "per annum", "p.m": "after midday", "pm": "prime minister", "poc": "people of color", "pov": "point of view", "pp": "pages", "ppl": "people", "prw": "parents are watching", "ps": "postscript", "pt": "point", "ptb": "please text back", "pto": "please turn over", "qpsa": "what happens", "ratchet": "rude", "rbtl": "read between the lines", "rlrt": "real life retweet", "rofl": "rolling on the floor laughing", "roflol": "rolling on the floor laughing out loud", "rotflmao": "rolling on the floor laughing my ass off", "rt": "retweet", "ruok": "are you ok", "sfw": "safe for work", "sk8": "skate", "smh": "shake my head", "sq": "square", "srsly": "seriously", "ssdd": "same stuff different day", "tbh": "to be honest", "tbs": "tablespooful", "tbsp": "tablespooful", "tfw": "that feeling when", "thks": "thank you", "tho": "though", "thx": "thank you", "tia": "thanks in advance", "til": "today i learned", "tl;dr": "too long i did not read", "tldr": "too long i did not read", "tmb": "tweet me back", "tntl": "trying not to laugh", "ttyl": "talk to you later", "u": "you", "u2": "you too", "u4e": "yours for ever", "utc": "coordinated universal time", "w/": "with", "w/o": "without", "w8": "wait", "wassup": "what is up", "wb": "welcome back", "wtf": "what the fuck", "wtg": "way to go", "wtpa": "where the party at", "wuf": "where are you from", "wuzup": "what is up", "wywh": "wish you were here", "yd": "yard", "ygtr": "you got that right", "ynk": "you never know", "zzz": "sleeping bored and tired"}
    return abb

def contractions():
    contrac={"aren't": "are not", "can't": "cannot", "couldn't": "could not", "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not", "he'd": "he had", "he'll": "he will", "he's": "he is", "i'd": "i had", "i'll": "i will", "i'm": "i am", "i've": "i have", "isn't": "is not", "let's": "let us", "mightn't": "might not", "mustn't": "must not", "shan't": "shall not", "she'd": "she had", "she'll": "she will", "she's": "she is", "shouldn't": "should not", "that's": "that is", "there's": "there is", "they'd": "they had", "they'll": "they will", "they're": "they are", "they've": "they have", "we'd": "we had", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what're": "what are", "what's": "what is", "what've": "what have", "where's": "where is", "who'd": "who had", "who'll": "who will", "who're": "who are", "who's": "who is", "who've": "who have", "won't": "will not", "wouldn't": "would not", "you'd": "you had", "you'll": "you will", "you're": "you are", "you've": "you have", "ain't": "has not", "wanna": "want a", "whatcha": "what are you", "kinda": "kind of", "sorta": "sort of", "outta": "out of", "alotta": "a lot of", "lotsa": "lots of", "mucha": "much of", "cuppa": "cup of", "dunno": "don't know", "lemme": "let me", "gimme": "give me", "tell'em": "tell them", "cos": "because", "innit?": "isn't it?", "i'mma": "i'm going to", "gonna": "going to", "needa": "need to", "oughta": "ought to", "hafta": "have to", "hasta": "has to", "usta": "used to", "supposta": "supposed to", "gotta": "(have) got a", "cmon": "come on", "ya": "you", "shoulda": "should have", "shouldna": "shouldn't have", "wouldna": "wouldn't have", "she'da": "she would have", "coulda": "could have", "woulda": "would have", "mighta": "might have", "mightna": "mightn't have", "musta": "must have", "mussna": "must not have", "dontcha": "don't you", "wontcha": "won't you", "betcha": "bet you", "gotcha": "got you", "d'you": "do you"}
    return contrac

def emojis():
    emoji_dict={"😂":"laughing","😍":"love","😭":"crying","😘":"kiss","😊":"smiling","😁":"grinning","😩":"weary","🙏":"thank you","😏":"smirk","😉":"wink","🙌":"celebrate","🙈":"see no evil","😄":"smiling","😒":"unamused","😃":"smiling","😔":"sad","😱":"fear","😜":"joking","😳":"flushed","😡":"angry","😎":"cool","😢":"crying","😋":"delicious","🙊":"speak no evil","😴":"sleepy","😌":"relieved","😞":"disappointed","😆":"laughing","😝":"joking","😪":"sleepy","😫":"tired","😅":"smiling","😀":"grinning","😚":"kiss","😻":"love","😥":"disappointed","😕":"confused","😤":"triumph","😈":"evil laugh","😰":"scared","😑":"expressionless","😹":"tears of joy","😠":"angry","😓":"dissapointment","😣":"helplessness","😐":"ok","😨":"fear","😖":"confound","😷":"mask","🙋":"me","😛":"joking","😬":"awkward","😙":"kiss","🙆":"ok","🙅":"no","🙉":"hear no evil","😇":"bless","😿":"crying","😲":"astonished","😶":"loss of words","😵":"dizzy","😸":"grinning","😧":"anguished","😮":"understood","😽":"kiss","🙀":"fear","🙇":"grateful","😟":"worried","😯":"hushed","😦":"frown","🙍":"frown","😺":"smiling","😾":"angry","😼":"smirk","🙎":"angry","😗":"kissing","🤩":"excited","🤗":"hugging"}
    return emoji_dict

def remove_special_char(sentence):
    st=''
    for ch in sentence:
        if ch.isalnum() or ch in string.whitespace:
            st+=ch
    return st

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    
class WordSegment:
    def __init__(self,string):
        self.text=string.lower()
        self.english_words = wordfreq.get_frequency_dict("en")
        self.__P= self.__probability(self.english_words)
        self.__result=self.__segment(self.text)
    
    def __probability(self,counter):
        N = sum(counter.values())
        return lambda x: counter.get(x,0)/N


    def segment_list(self):
        return self.__result
    
    def __Pwords(self,words):
        result=1
        for w in words:
            result*= self.__P(w)
        return result

    def __tokens(text):
        return re.findall('[a-z]+', text.lower()) 

    def __memo(f):
        cache = {}
        def fmemo(*args):
            if args not in cache:
                cache[args] = f(*args)
            return cache[args]
        fmemo.cache = cache
        return fmemo

    def __get_length(self,string):
        count = 0
        for char in string:
            count += 1
        return count

        
    def __splits(self,text, start=0, L=20):
        return [(text[:i], text[i:]) 
                for i in range(start, min(self.__get_length(text), L)+1)]

    @__memo
    def __segment(self,text):
        if not text: 
            return []
        else:
            candidates = ([first] + self.__segment(rest) 
                        for (first, rest) in self.__splits(text, 1))
            return max(candidates, key=self.__Pwords)