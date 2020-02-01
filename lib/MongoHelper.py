import redis
import threading
import logging


class MongoClient(object):

    # mutex = threading.Lock()  # gevent 里使用线程锁可能有问题
    config = None
    connection_pool = None
    connection_client = None

    def __init__(self, config):
        """
        :param config: {"host":"",
                        "port": 0,
                        "index": 0,
                        "auth": "",
                        "encoding": "",
                        "decode_responses": False,
                        "max_connections": 1,
                        "target_max_memory": 1024
                        }
        """
        self.config = config
        max_conn = 1
        if "max_connections" in self.config:
            max_conn = self.config["max_connections"]
            if max_conn <= 0:
                max_conn = 1
        decode_responses = False
        if "decode_responses" in config:
            decode_responses = config["decode_responses"]
        temp_pool = redis.ConnectionPool(host=self.config['host'], port=self.config['port'], db=self.config['index'],
                                         password=self.config['auth'],
                                         encoding=self.config['encoding'], max_connections=max_conn,
                                         decode_responses=decode_responses)
        self.connection_pool = temp_pool
        temp_client = redis.Redis(connection_pool=self.connection_pool)
        self.connection_client = temp_client



config = {
    "host": "",
    "port": 6379,
    "auth": "",
    "index": 11,
    "encoding": "utf-8",
    "decode_responses": True,  # 获取中文数据可以直接 decode python unicode
    "target_max_memory": 3896,
    "max_connections": 1
}

redis_client = MongoClient(config)
