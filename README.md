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
