## update April 1, 2020
this is no longer maintained

~blinkist is offering free premium for some time so now would be a good time to update this scraper~

~it's on my to-do list, but~ if I were to rewrite this I'd probably use nodejs and puppeteer

# blinkist-scraper
Scrape blinkist https://www.blinkist.com/

# Usage
1. First modify `scraper.py` with your login information
2. Then run `python run.py` to spawn the spider
3. The spider outputs a file `books.json` which is parsed by `generate-html.py`
4. `generate-html.py` outputs `.html` files into the `html` directory containing the raw book content

# Future Improvements
- Ask for login information instead of hard coding into `scraper.py`
- Output ePub instead of html
