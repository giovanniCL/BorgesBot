require('dotenv').config()
const Twitter = require('twitter');
const generator = require('./generate')
 
const client = new Twitter({
  consumer_key: process.env.API_KEY,
  consumer_secret: process.env.API_SECRET_KEY,
  access_token_key: process.env.TOKEN,
  access_token_secret: process.env.SECRET
});
console.log(client)

function post(){
    let status = generator.trigram_generate(generator.ngram_model)
    while(status.length > 280) status = generator.trigram_generate(generator.ngram_model)
    client.post('statuses/update',{status:status}, (error,tweet, response)=>{
        if(error) console.log(error)
        else console.log(tweet)
    })
}

setInterval(()=>{
    post()
},60000)

