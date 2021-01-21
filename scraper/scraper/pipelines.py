# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline


class ScraperPipeline:
    def process_item(self, item, spider):
        return item

class ImageItemOWPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        #https://docs.scrapy.org/en/latest/topics/media-pipeline.html
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        adapter = ItemAdapter(item)
        adapter['path'] = file_paths
        return item