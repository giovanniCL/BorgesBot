const axios = require('axios')
const cheerio = require('cheerio')
const fs = require('fs')

const getLinks = async () => {
	try {
		const { data } = await axios.get(
			'https://ciudadseva.com/autor/jorge-luis-borges/cuentos/'
		);
		const $ = cheerio.load(data)
		const storyLinks = [];

		$('ul.list-stories > li > a').each((_idx, el) => {
			const link = $(el).attr('href')
			storyLinks.push(link)
		})

		return storyLinks;
	} catch (error) {
		throw error
	}
};

fs.writeFileSync('./corpus.txt', "")

getLinks().then(async links => {
    links.forEach(async (link) =>{
        try{
            const { data } = await axios.get(link)
            const $ = cheerio.load(data)
            let story = ""

            $('div.text-justify > p').each((_idx, el) => {
                const paragraph = $(el).text()
                story += ` ${paragraph}`
            })
            fs.appendFileSync('corpus.txt', story)

        } catch(error){
            throw error
        }
    })
})