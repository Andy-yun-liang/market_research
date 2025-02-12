import scrapy
import logging
import csv
import orjson
from urllib.parse import urlparse
from datetime import datetime
from ..items import ShopifyRawItem

class ShopifySpider(scrapy.Spider):
    name = "shopify_spider"

    def start_requests(self):
        csv_path = "urls.csv"
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if not row or not row[0].strip():
                    self.log("Skipping empty row", level=logging.WARNING)
                    continue  

                url = row[0].strip()  
                parsed_url = urlparse(url)

                
                if not parsed_url.netloc or "." not in parsed_url.netloc:
                    self.log(f"Invalid url: {url}", level=logging.ERROR)
                    continue  

               
                domain_parts = parsed_url.netloc.split(".")
                shop_name = domain_parts[-2] if len(domain_parts) > 2 else domain_parts[0]

                product_url = f"{url}/products.json"

                
                yield scrapy.Request(
                    url=product_url,
                    callback=self.parse,
                    meta={'shop_name': shop_name, 'shop_url': url, 'page_number': 1}  
                )

    def parse(self, response):
        shop_name = response.meta['shop_name']
        shop_url = response.meta['shop_url']
        page_number = response.meta.get("page_number", 1)
        self.log(f"Parsing data from: {shop_name} (Page {page_number})", level=logging.INFO)
        scraped_at = datetime.now()

        try:
            data = orjson.loads(response.text)

            item = ShopifyRawItem(
                shop_name=shop_name,
                shop_url=shop_url,
                page_number=page_number,
                scraped_at=scraped_at,
                products_info=data  
            )
            yield item  

            
            if "products" in data and len(data["products"]) > 0:
                if "next_page_info" in data:  #dealing with next_page_info pagination
                    next_page_info = data["next_page_info"]
                    next_url = response.urljoin(f"?page_info={next_page_info}")
                    self.log(f"Fetching next page using next_page_info: {next_page_info}", level=logging.INFO)
                    yield scrapy.Request(
                        url=next_url,
                        callback=self.parse,
                        meta={'shop_name': shop_name, 'shop_url': shop_url, 'page_number': page_number + 1}
                    )
                else:  # normal page pagination
                    next_page = page_number + 1
                    next_url = response.urljoin(f"?page={next_page}")
                    self.log(f"Fetching next page: {next_page}", level=logging.INFO)
                    yield scrapy.Request(
                        url=next_url,
                        callback=self.parse,
                        meta={'shop_name': shop_name, 'shop_url': shop_url, 'page_number': next_page}
                    )

        except orjson.JSONDecodeError:
            self.log(f'Failed to parse JSON from {shop_name}', level=logging.ERROR)
