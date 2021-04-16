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
    tokens_list.append(tokens)

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

def sortFunc(x):
    return x[1]

for key, value in bigram_prob.items():
    value.sort(key = sortFunc)

j = json.dumps(bigram_prob, ensure_ascii=False)
with open("model.json",'w') as f:
    f.write(j)
    f.close()



