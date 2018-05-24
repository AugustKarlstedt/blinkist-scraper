import json
import re

invalid_characters = re.compile(r'[\\/:"*?<>|\.,]+')

with open('books.json', encoding='utf-8') as input_file:
    books = json.load(input_file)

    for book in books:
        cleaned_title = book['title'][0].replace('<h1 class="book__header__title">', '')
        cleaned_title = cleaned_title.replace('</h1>', '')
        cleaned_title = cleaned_title.lower()
        cleaned_title = cleaned_title.strip()
        cleaned_title = invalid_characters.sub('', cleaned_title)
        cleaned_title = cleaned_title.replace(' ', '-')
        
        cleaned_author = book['author'][0].replace('<div class="book__header__author">', '')
        cleaned_author = cleaned_author.replace('</div>', '')
        cleaned_author = cleaned_author.lower()
        cleaned_author = cleaned_author.strip()
        cleaned_author = invalid_characters.sub('', cleaned_author)
        cleaned_author = cleaned_author.replace(' ', '-')

        with open('html/{}-{}.html'.format(cleaned_title, cleaned_author), 'w+', encoding='utf-8') as output_file:
            output_file.write(book['title'][0])
            output_file.write(book['subtitle'][0])
            output_file.write(book['author'][0])
            output_file.write(book['read_time'][0])
            output_file.write(book['synopsis'][0])
            output_file.write(book['about_the_author'][0])
            for c in book['content']:
                output_file.write(c)
            
