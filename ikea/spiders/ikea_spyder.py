from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from ikea.items import IkeaItem


class IkeaSpider(CrawlSpider):
    name = "ikea"
    allowed_domains = ["ikea.com"]
    start_urls = [
        "https://www.ikea.com/us/en/catalog/allproducts/department/",
        #"http://www.ikea.com/es/es/catalog/categories/departments/workspaces/16195/",
        #"http://www.ikea.com/es/es/catalog/products/S19903730/index.html/"
    ]
    extractor = LxmlLinkExtractor()

#    rules = (
#        Rule(extractor, callback='parse_links', follow=True),
#    )

    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LxmlLinkExtractor(allow=('catalog/products/.*', )), callback='parse_item'),

        # and follow links from them (since no callback means follow=True by default).
        Rule(LxmlLinkExtractor()),
    )

    def parse_item(self, response):
        #self.log('Hi, this is an item page! %s' % response.url)
        sel = Selector(response)
        print('\nFound product URL-> %s' % response.url)
        item = IkeaItem()
        item['description'] = sel.xpath('/html/head/meta[@name="description"]/@content').extract()
        item['keywords'] = sel.xpath('/html/head/meta[@name="keywords"]/@content').extract()
        item['country'] = sel.xpath('/html/head/meta[@name="country"]/@content').extract()
        item['language'] = sel.xpath('/html/head/meta[@name="language"]/@content').extract()
        item['store_id'] = sel.xpath('/html/head/meta[@name="store_id"]/@content').extract()
        item['title'] = sel.xpath('/html/head/meta[@name="title"]/@content').extract()
        item['product_name'] = sel.xpath('/html/head/meta[@name="product_name"]/@content').extract()
        item['category_name'] = sel.xpath('/html/head/meta[@name="category_name"]/@content').extract()
        item['subcategory_if'] = sel.xpath('/html/head/meta[@name="subcategory_if"]/@content').extract()
        item['price'] = sel.xpath('/html/head/meta[@name="price"]/@content').extract()
        item['price_other'] = sel.xpath('/html/head/meta[@name="price_other"]/@content').extract()
        item['changed_family_price'] = sel.xpath('/html/head/meta[@name="changed_family_price"]/@content').extract()
        item['item_id'] = sel.xpath('/html/head/meta[@name="item_id"]/@content').extract()
        item['partnumber'] = sel.xpath('/html/head/meta[@name="partnumber"]/@content').extract()
        item['url'] = response.url
        item['image'] = sel.xpath('/html/head/link[@rel="image_src"]/@href').extract()
        #print item
        return item

    def _page(self, response):
        sel= Selector(response)
        #Products selection
        #products = sel.xpath("//div[@class='productInformation']")
        productName = sel.xpath("div[@id='schemaProductPrice']").extract()
        print("holaaaaa")
        print(productName)
        #item["link"] = post.select("div[@class='bodytext']/h2/a/@href").extract()
        #item["content"] = post.select("div[@class='bodytext']/p/text()").extract()
        #items.append(item)
        #for item in items:
        #yield item
