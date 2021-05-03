from nltk import word_tokenize
import stanza
nlp = stanza.Pipeline(lang = "es", processors='tokenize,pos')
import json

in_file = open("corpus.txt", 'r', encoding = "utf-8")
corpus = in_file.read()

sentences = []
new_sent = ""
for char in corpus:
    new_sent += char
    if char == "." or char == "?" or char == "!":
        sentences.append(new_sent)
        new_sent = ""

tokens_list = []
pos_list = []
for sentence in sentences:
    doc = nlp(sentence)
    pos_list.append([word.xpos for sent in doc.sentences for word in sent.words])
    tokens_list.append([word.text for sent in doc.sentences for word in sent.words])

def addToDict(key, dict):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1

def addToDictofDicts(key, value, dict):
    if key in dict:
        entry =dict[key]
        if value not in entry:
            entry[value] = 0
        entry[value] += 1
    else:
        dict[key] = {value:1}

def probabilize(bigram_dict, unigram_dict):
    new_dict = {}
    for key, value in bigram_dict.items():
        denominator = unigram_dict[key]
        for word,freq in value.items():
            probability = freq/denominator
            if key in new_dict:
                new_dict[key].append([word,probability])
            else:
                new_dict[key] = []
                new_dict[key].append([word,probability])
    return new_dict

unigram_freq = {}
unigram_prob = {}
unigram_pos_freq = {}
bigram_freq = {}
bigram_prob = {}
bigram_pos_freq = {}
word_sum = 0
unigram_freq["<START>"] = len(sentences)
unigram_freq["<END>"] = len(sentences)
unigram_pos_freq["<START>"] = len(sentences)
unigram_pos_freq["<END>"] = len(sentences)
pos_dict = {}
for i in range(len(tokens_list)):
    addToDictofDicts("<START>", tokens_list[i][0], bigram_freq)
    addToDictofDicts("<START>", pos_list[i][0], bigram_pos_freq)
    for j in range(len(tokens_list[i]) - 1):
        word_sum +=1
        token = tokens_list[i][j]
        pos = pos_list[i][j]
        addToDict(token, unigram_freq)
        addToDict(pos, unigram_pos_freq)
        addToDictofDicts(token, tokens_list[i][j + 1], bigram_freq)
        addToDictofDicts(pos, pos_list[i][j + 1], bigram_pos_freq)
        addToDictofDicts(pos, token, pos_dict)
    addToDict(tokens_list[i][len(tokens_list[i]) - 1], unigram_freq)
    addToDict(pos_list[i][len(pos_list[i]) - 1], unigram_pos_freq)
    addToDictofDicts(tokens_list[i][len(tokens_list[i]) - 1], "<END>", bigram_freq)
    addToDictofDicts(pos_list[i][len(pos_list[i]) - 1], "<END>", bigram_pos_freq)
    addToDictofDicts(pos_list[i][len(pos_list[i])-1], tokens_list[i][len(tokens_list[i]) - 1], pos_dict)

bigram_prob = probabilize(bigram_freq, unigram_freq)
bigram_pos_prob = probabilize(bigram_pos_freq,unigram_pos_freq)
pos_prob = probabilize(pos_dict, unigram_pos_freq)

print(bigram_pos_prob["<START>"])



def sortFunc(x):
    return x[1]

for key, value in bigram_prob.items():
    value.sort(key = sortFunc)

for key, value in bigram_pos_prob.items():
    value.sort(key = sortFunc)
for key, value in pos_prob.items():
    value.sort(key = sortFunc)
model = {
    "bigram_prob" : bigram_prob,
    "bigram_pos_prob" : bigram_pos_prob,
    "pos_prob" : pos_prob
}

j = json.dumps(model, ensure_ascii=False)
with open("model.json",'w') as f:
    f.write(j)
    f.close()



