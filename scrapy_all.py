import urllib
import scrapy

from scrapy.http import Request

class usgs(scrapy.Spider):
  name = "usgs_all"

  #allowed_domains = ["www.usgs.gov", "www.pubs.usgs.gov"] #Sometimes they use Amazon Buckets etc. so i didn't specify where the download comes from
  start_urls = ["https://www.usgs.gov/centers/national-minerals-information-center/commodity-statistics-and-information"]

  def parse(self, response):
      base_url = 'https://www.usgs.gov'
      for a in response.xpath('//a[@href]/@href'):
          link = a.extract()
          if link.endswith('statistics-and-information'):
              link = urllib.parse.urljoin(base_url, link)
              self.logger.info(link)
              yield Request(link, callback=self.parse_commodities)

  def parse_commodities(self, response):
    for a in response.xpath('//a[@href]/@href'):
        link = a.extract()
        # self.logger.info(link)

        if link.endswith('.pdf'):
            #link = urllib.parse.urljoin(base_url, link)
            self.logger.info(link)
            yield Request(link, callback=self.save_pdf)

  def save_pdf(self, response):
    path = response.url.split('/')[-1]
    self.logger.info('Saving PDF %s', path)
    with open(path, 'wb') as f:
        f.write(response.body)
