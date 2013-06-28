# Scrapy settings for ecommerce project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os
BOT_NAME = 'ecommerce'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['ecommerce.spiders']
NEWSPIDER_MODULE = 'ecommerce.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0) Gecko/20100101 Firefox/9.0'

FEED_EXPORTERS = {
    'jsonlines': 'scrapy.contrib.exporter.JsonLinesItemExporter',
    }

FEED_FORMAT = 'jsonlines'

FEED_URI = "output/%(name)s/%(time)s.json"

DOWNLOAD_DELAY = 30

HTTPCACHE_ENABLED = True

ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
IMAGES_STORE = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'\spiders\output\magicalement'))

LOG_FILE = 'log_spider.log'

