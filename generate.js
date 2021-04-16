const fs = require('fs')
const model = JSON.parse(fs.readFileSync('model.json', 'latin1'))

function getWord(words, probability){
    if(words.length == 1) return words[0][0]
    let possible_words = []
    //console.log(words)
    for(let i = (words.length) - 1; i > 0; i--){
        let word = words[i][0]
        if(probability > words[i-1][1]) {
            possible_words.push(word)
            continue
        }
    }
    let rand = Math.floor(Math.random() * possible_words.length)
    //console.log(rand)
    //console.log(possible_words[rand])
    if(possible_words.length == 0) return words[0][0]
    return possible_words[rand]
}

function generate(model){
    sentence = ""
    nextWord = getWord(model["<START>"],Math.random())
    while(nextWord != "<END>"){
        let space = (nextWord == "." || nextWord == ",") ? "" : " "
        sentence += space + nextWord
        nextWord = getWord(model[nextWord],Math.random())

    }
    return sentence.trim()
}

let output = generate(model)
console.log(output)
