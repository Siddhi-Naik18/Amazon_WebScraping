import scrapy
from ..items import AmazonItem

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon"
    page_number = 2
    start_urls = ["https://www.amazon.in/Books/s?rh=n%3A976389031&page=3"]

    def parse(self, response):
        items = AmazonItem()
        product_name = response.css(".a-color-base.a-text-normal::text").extract()
        product_author = response.css(".a-color-secondary .a-size-base.s-link-style::text").extract()
        product_price = response.css(".puis-price-instructions-style .a-price-whole::text").extract()
        product_imagelink = response.css(".s-image::attr(src)").extract()

        for name, author, price, imagelink in zip(product_name, product_author, product_price, product_imagelink):
            item = AmazonItem()
            item['product_name'] = name
            item['product_author'] = author
            item['product_price'] = price
            item['product_imagelink'] = imagelink
            yield item

        next_page = "https://www.amazon.in/Books/s?i=stripbooks&rh=n%3A976389031&page=" + str(AmazonSpiderSpider.page_number) + "&qid=1708419425&ref=sr_pg_4"
        if AmazonSpiderSpider.page_number <= 10:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
