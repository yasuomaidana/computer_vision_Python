import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes" #nombre del spider

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ] #arreglo de las paginas que buscara
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) #regresa lista de request de los links

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)