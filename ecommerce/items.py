
import scrapy

class ShopifyRawItem(scrapy.Item):
    shop_name = scrapy.Field()
    shop_url = scrapy.Field()
    page_number = scrapy.Field()  
    scraped_at = scrapy.Field()  
    products_info = scrapy.Field()
      


