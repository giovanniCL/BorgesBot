const fs = require('fs')
const model = JSON.parse(fs.readFileSync('model.json', 'latin1'))

function getWord(words, probability){
    
    if(words.length == 1) return words[0][0]
    let possible_words = []
    for(let i = (words.length) - 1; i > 0; i--){
        let word = words[i][0]
        if(probability > words[i-1][1]) {
            possible_words.push(word)
            continue
        }
    }
    let rand = Math.floor(Math.random() * possible_words.length)
    if(possible_words.length == 0) return words[0][0]
    return possible_words[rand]
    
}

function altGetWord(words, probability){
    if(words.length == 1) return words[0][0]
    let cumulative = 0
    for(let i = 0; i < words.length -1; i++){
        cumulative += words[i][1]
        if(cumulative > probability)return words[i][0]
    }
    return words[words.length -1][0]
}

function word_generate(model){
    let bigram_prob = model.bigram_prob
    let sentence = ""
    nextWord = altGetWord(bigram_prob["<START>"],Math.random())
    while(nextWord != "<END>"){
        let space = (nextWord == "." || nextWord == ",") ? "" : " "
        sentence += space + nextWord
        nextWord = altGetWord(bigram_prob[nextWord],Math.random())

    }
    return sentence.trim()
}

function pos_generate(model){
    let bigram_pos_prob = model.bigram_pos_prob
    let pos_prob = model.pos_prob
    pos_list = []
    nextPOS = altGetWord(bigram_pos_prob["<START>"], Math.random())
    while(nextPOS != "<END>"){
        pos_list.push(nextPOS)
        nextPOS = altGetWord(bigram_pos_prob[nextPOS], Math.random())
    }
    let sentence = ""
    pos_list.forEach(pos=>{
        let nextWord = altGetWord(pos_prob[pos], Math.random())
        let space = (nextWord == "." || nextWord == ",") ? "" : " "
        sentence += space + nextWord
    })
    return sentence.trim()
}

function hybrid_generate(model){
    let bigram_prob = model.bigram_prob
    let bigram_pos_prob = model.bigram_pos_prob
    let pos_prob = model.pos_prob
    pos_list = []
    nextPOS = altGetWord(bigram_pos_prob["<START>"], Math.random())
    while(nextPOS != "<END>"){
        pos_list.push(nextPOS)
        nextPOS = altGetWord(bigram_pos_prob[nextPOS], Math.random())
    }
    let sentence = ""
    let currentWord = "<START>"
    pos_list.forEach(pos=>{
        
        let nextWord = altGetWord(pos_prob[pos], Math.random())
        while(bigram_prob[currentWord].map(word=>word[0]).includes(nextWord)){
           nextWord = altGetWord(pos_prob[pos], Math.random())

        }
        currentWord = nextWord
        let space = (nextWord == "." || nextWord == ",") ? "" : " "
        sentence += space + nextWord
    })
    return sentence.trim()
}

let output = word_generate(model)
console.log(output)
