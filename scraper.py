import scrapy
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field

import time

class Book(Item):
    title = Field()
    subtitle = Field()
    author = Field()
    read_time = Field()
    synopsis = Field()
    who_should_read = Field()
    about_the_author = Field()
    content = Field()

class MySpider(Spider):

    name = 'blinkist.com'
    allowed_domains = ['blinkist.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2.0,
    }

    start_urls = ['https://www.blinkist.com/en/nc/login']

    def parse(self, response):
        formdata = {
            'login[email]': 'your.email@whatever.com', 
            'login[password]': 'your password'
        }

        return scrapy.FormRequest.from_response(response, formdata=formdata, callback=self.after_login)

    def after_login(self, response):
        if b'The password or email is invalid.' in response.body:
            self.logger.error('Login failed!')
            return

        category_links = response.css('a.category-list-item__link')
        for category_link in category_links:
            category_href = response.urljoin(category_link.xpath('@href').extract_first())
            yield scrapy.Request(category_href, self.parse_high_level_category)
        
    def parse_high_level_category(self, response):
        all_blinks_href = response.urljoin(response.css('a.buttonV2').xpath('@href').extract_first())
        yield scrapy.Request(all_blinks_href, self.parse_all_blinks_in_category)
        
    def parse_all_blinks_in_category(self, response):
        books = response.css('a.letter-book-list__item')

        for book in books:
            book_href = response.urljoin(book.xpath('@href').extract_first())
            yield scrapy.Request(book_href, self.parse_book)

    def parse_book(self, response):
        item = Book()
        item['title'] = response.css('h1.book__header__title').extract()
        item['subtitle'] = response.css('h2.book__header__subtitle').extract()
        item['author'] = response.css('div.book__header__author').extract()
        item['read_time'] = response.css('.book__header__info .book__header__info-item-body').extract()
        item['synopsis'] = response.css('.book__tab-content[ref="synopsis"]').extract()
        item['who_should_read'] = response.css('.book__tab-content[ref="who_should_read"]').extract()
        item['about_the_author'] = response.css('.book__tab-content[ref="about_the_author"]').extract()

        reader_link = response.css('.button-greenV2[data-read-now="Read now"]')
        reader_href = response.urljoin(reader_link.xpath('@href').extract_first())

        request = scrapy.Request(reader_href, self.parse_reader)
        request.meta['item'] = item

        yield request

    def parse_reader(self, response):
        item = response.meta['item']

        chapters = response.css('.reader__container__content > .chapter')

        content = ""
        for chapter in chapters:
            chapter_title = chapter.css('h1').extract_first()
            content += chapter_title

            chapter_contents = chapter.css('.chapter__content')
            for chapter_content in chapter_contents:
                content += chapter_content.extract()

        item['content'] = content

        yield item
