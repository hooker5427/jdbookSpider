BOT_NAME = 'JDbooks'

SPIDER_MODULES = ['JDbooks.spiders']
NEWSPIDER_MODULE = 'JDbooks.spiders'

ROBOTSTXT_OBEY = False

# DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 10

DOWNLOADER_MIDDLEWARES = {
    'JDbooks.middlewares.RotateUserAgentMiddleware': 543,
    'JDbooks.middlewares.seleniumdownloadMiddleware': 545,
}

ITEM_PIPELINES = {
    'JDbooks.pipelines.JdspiderMySQLPipeline': 300
}

# 需要将调度器的类和去重的类替换为 Scrapy-Redis 提供的类
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_HOST = '47.115.21.129'
REDIS_PORT = 6379  # Redis集群中其中一个节点的端口


# 配置REDIS 连接密码
REDIS_PARAMS = {
    'password': 'redis',
}

# 配置持久化
# Scrapy-Redis 默认会在爬取全部完成后清空爬取队列和去重指纹集合。
# SCHEDULER_PERSIST = True

# 设置重爬
# SCHEDULER_FLUSH_ON_START = True
