import json
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


Base = declarative_base()

class ShopifyRawData(Base):
    __tablename__ = 'raw_shopify_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(String, nullable=False)
    shop_url = Column(String, nullable=False)  
    page_number = Column(Integer, nullable=False)  
    scraped_at = Column(DateTime, nullable=False)
    products_info = Column(Text, nullable=False)  

DATABASE_URL = "sqlite:///raw_shopify_data.db"  # SQLite connection URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

class SQLitePipeline:
    def open_spider(self, spider):
       
        self.session = SessionLocal()

    def process_item(self, item, spider):
        
        try:
            if "products" not in item["products_info"] or len(item["products_info"]["products"]) == 0:
                spider.logger.info(f"Skipping item with empty products: {item['shop_name']} (Page {item['page_number']})")
                return None  
            shop_name = item["shop_name"]
            shop_url = item["shop_url"]
            page_number = item["page_number"]
            scraped_at = item["scraped_at"]
            products_info = json.dumps(item["products_info"])  

            new_data = ShopifyRawData(
                shop_name=shop_name,
                shop_url=shop_url,
                page_number=page_number,
                scraped_at=scraped_at,
                products_info=products_info
            )

           
            self.session.add(new_data)
            self.session.commit()  

            spider.logger.info(f"Inserted data: {shop_name} (Page {page_number})")

        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error saving item: {e}")
            return None

        return item 

    def close_spider(self, spider):
        self.session.close()
