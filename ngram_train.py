from nltk import word_tokenize
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
for sentence in sentences:
    tokens = word_tokenize(sentence)
    if tokens[0] == "FIN":
        tokens = tokens[1:]
    tokens_list.append(tokens)

##UNIGRAM
unigram_freq = {}
unigram_prob = {}
word_sum = 0
for tokens in tokens_list:
    for token in tokens:
        word_sum += 1
        if token in unigram_freq:
            unigram_freq[token] += 1
        else:
            unigram_freq[token] = 1

for tokens in tokens_list:
    for token in tokens:
        freq = unigram_freq[token]
        unigram_prob[token] = freq/word_sum

unigram_freq["<START>"] = len(sentences)
unigram_freq["<END>"] = len(sentences)

##BIGRAM
bigram_freq = {}
bigram_prob = {}
def addToDict(key, value, dict):
    if key in dict:
        entry =dict[key]
        if value not in entry:
            entry[value] = 0
        entry[value] += 1
    else:
        dict[key] = {value:1}

for tokens in tokens_list:
    addToDict("<START>", tokens[0], bigram_freq )
    for i in range(len(tokens)-1):
        addToDict(tokens[i],tokens[i+1],bigram_freq)
    addToDict(tokens[len(tokens)-1],"<END>",bigram_freq)

for key, value in bigram_freq.items():
    denominator = unigram_freq[key]
    for word,freq in value.items():
        probability = freq/denominator
        if key in bigram_prob:
            bigram_prob[key].append([word,probability])
        else:
            bigram_prob[key] = []
            bigram_prob[key].append([word,probability])


bigram_freq["<START>"]["<START>"] = len(sentences)
bigram_freq["<END>"] = {}
bigram_freq["<END>"]["<END>"] = len(sentences)

##TRIGRAM
def addToTriDict(pkey, skey, value, dict):
    if pkey not in dict:
        dict[pkey] = {}
    if skey not in dict[pkey]:
        dict[pkey][skey] = {}
    addToDict(skey, value, dict[pkey])
    

trigram_freq = {}
trigram_prob = {}
for tokens in tokens_list:
    addToTriDict("<START>", "<START>",tokens[0], trigram_freq)
    addToTriDict("<START>", tokens[0], tokens[1], trigram_freq)
    for i in range(len(tokens) -2):
        addToTriDict(tokens[i], tokens[i+1], tokens[i+2], trigram_freq)
    addToTriDict(tokens[len(tokens)-2], tokens[len(tokens)-1], "<END>", trigram_freq)
    addToTriDict(tokens[len(tokens)-1], "<END>", "<END>", trigram_freq)

for pkey, pdict in trigram_freq.items():
    if pkey not in trigram_prob:
        trigram_prob[pkey] = {}
    for skey, value in pdict.items():
        if skey not in trigram_prob[pkey]:
            trigram_prob[pkey][skey] = []
        denominator = bigram_freq[pkey][skey]
        for word, freq in value.items():
            probability = freq/denominator
            trigram_prob[pkey][skey].append([word, probability])


def sortFunc(x):
    return x[1]

for key, value in bigram_prob.items():
    value.sort(key = sortFunc)

for pkey, pdict in trigram_prob.items():
    for skey, value in pdict.items():
        value.sort(key = sortFunc)

model = {
    "bigram_prob" : bigram_prob,
    "trigram_prob": trigram_prob
}

j = json.dumps(model, ensure_ascii=False)
with open("ngram_model.json",'w') as f:
    f.write(j)
    f.close()
