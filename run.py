import subprocess

subprocess.run(['scrapy', 'runspider', 'scraper.py', '-o', 'books.json'])
subprocess.run(['python', 'generate-html.py'])


