import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    my_base_url = 'https://books.toscrape.com/'

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            book_page_relative_url = book.css('h3 > a').attrib['href']
            if book_page_relative_url is not None:
                book_page_url = self.my_base_url
                if not 'catalogue' in book_page_relative_url:
                    book_page_url += 'catalogue/'
                book_page_url += book_page_relative_url
                yield response.follow(book_page_url, self.book_page_parse)


        next_page = response.css('li.next > a::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://books.toscrape.com/'
            if not 'catalogue' in next_page:
                next_page_url += 'catalogue/'
            next_page_url += next_page
            yield response.follow(next_page_url, callback=self.parse)

    def book_page_parse(self, response):
        product_summary = response.css('article.product_page > div.row > div.product_main')
        product_description = response.css('div#product_description + p::text').get()
        table_rows = response.css('table tr')
        genre = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()

        title = product_summary.css('h1::text').get()
        price = product_summary.css('p.price_color::text').get()

        product_type = table_rows[1].css('td::text').get()
        price_excl_tax = table_rows[2].css('td::text').get()
        price_incl_tax = table_rows[3].css('td::text').get()
        tax = table_rows[4].css('td::text').get()
        rating = response.css('p.star-rating').attrib['class'].split(' ')[-1]

        yield {
            'url': response.url,
            'title': title.strip(),
            'product_type': product_type.strip(),
            'price': price.strip(),
            'rating': rating.strip(),
            'genre': genre.strip(),
            'description': product_description.strip(),
            'price_excl_tax': price_excl_tax.strip(),
            'price_incl_tax': price_incl_tax.strip(),
            'tax': tax.strip(),
        }