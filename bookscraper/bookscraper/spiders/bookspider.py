import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            title = book.css('h3 > a::text').get()
            link = book.css('h3 > a').attrib['href']
            price = book.css('div.product_price > p.price_color::text').get()
            yield {
                'title': title,
                'link': link,
                'price': price
            }

        next_page = response.css('li.next > a::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://books.toscrape.com/'
            if not 'catalogue' in next_page:
                next_page_url += 'catalogue/'
            next_page_url += next_page
            yield response.follow(next_page_url, callback=self.parse)
