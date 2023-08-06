import redis

class redisUtil:
    # 创建连接池并连接到redis，并设置最大连接数量;
    # conn_pool = redis.ConnectionPool(host='192.168.31.11',
    #                                  port=6379,
    #                                  max_connections=10,
    #                                  password='120721')
    conn_pool = redis.ConnectionPool(host='home.hddly.cn',
                                     port=56379,
                                     max_connections=10,
                                     password='120721')
    # 第一个客户端访问
    # re_pool = redis.Redis(connection_pool=conn_pool)

    #在集合中添加值
    def sadd(self,setname,setvalues):
        re_pool = redis.Redis(connection_pool=self.conn_pool)
        re_pool.sadd(setname,setvalues)

    #在集合中判断值存在
    def sismember(self,setname,setvalue):
        re_pool = redis.Redis(connection_pool=self.conn_pool)
        return re_pool.sismember(setname,setvalue)

    #在集合中删除某个元素
    def sremove(self,setname,setvalue):
        re_pool = redis.Redis(connection_pool=self.conn_pool)
        return re_pool.srem(setname,setvalue)

    #获取集合元素个数
    def scard(self,setname):
        re_pool = redis.Redis(connection_pool=self.conn_pool)
        return re_pool.scard(setname)