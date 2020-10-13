# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class MovieDataPipeline:
    def process_item(self, item, spider):
        item_df = pd.DataFrame(data=item, index=[0])
        item_df.to_csv('movie2020_url.csv', mode='a', index=False, header=None)
        return item
