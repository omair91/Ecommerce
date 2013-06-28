from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from urlparse import urljoin
from ecommerce.items import EcommerceItem
from scrapy import log
import re


class Magicalement(BaseSpider):
    name = 'magicalement'
    start_urls = ['http://magicalement.fr/']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        all_prods_url = hxs.select(
            "//ul//div[@class='infoBoxCorpsContenu']//a[contains(@href,'allprods')]/@href").extract()
        if all_prods_url:
            url = urljoin(response.url, all_prods_url[0])
            yield Request(url, callback=self.products_list)
        else:
            self.log("Invalid Page Found", log.CRITICAL)

    def products_list(self, response):
        hxs = HtmlXPathSelector(response)
        self.log(self.get_text_from_node(hxs.select("//span[@class='productList_nb_products']//text()")), log.INFO)
        products_url = hxs.select(
            "//div[contains(@class,'productList_ProduitBox_row productListing')]//p/a/@href").extract()
        for url in products_url:
            yield Request(url, callback=self.product_page)
        next_page = hxs.select("//span[@class='productList_page_result']/b/following-sibling::a[1]/@href").extract()
        if next_page:
            yield Request(url=next_page[0], callback=self.products_list)

    def product_page(self, response):
        hxs = HtmlXPathSelector(response)
        item = EcommerceItem()
        price = self.get_text_from_node(hxs.select("//span[@class='productSpecialPrice']/text()"))
        item['price'] = re.search('\d+.\d+',price).group(0) if price else ""        
        item['name'] = self.get_text_from_node(hxs.select("//*[@class='titregrasproduct']/text()"))
        image_url = hxs.select("//div[@id='Info_Produit_Image']//img/@src").extract()
        item['image_urls'] = [urljoin(response.url, image_url[0])] if image_url else []
        item['description'] = self.get_text_from_node(
            hxs.select("//div[@id='frontpage_tab1']//div[@class='produitTABSprod']//text()"))
        item['source_url'] = response.url
        yield item

    def get_text_from_node(self, node):
        list_text = node.extract()
        text = ""
        if list_text:
            list_text = [x.replace('\r', '').replace('\n', '').replace('\t', '').replace('"\\u20ac"', '') for x in
                         list_text]
            text = " ".join([x for x in list_text if x.strip()])
        return text