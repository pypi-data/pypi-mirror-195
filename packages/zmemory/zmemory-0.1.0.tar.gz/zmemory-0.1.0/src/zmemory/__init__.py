from redis import Redis


class Memory(object):
    def __init__(self, config):
        self.instance = Redis(decode_responses=True, **config)

    def get(self, k):
        """获取值
        c.get('access_token_00b73bbe23f34a468b2a5f158701f17f_wx')
        """
        return self.instance.get(k)

    def set(self, k, v, *args):
        """修改值
        c.get('access_token_00b73bbe23f34a468b2a5f158701f17f_wx')
        """
        return self.instance.set(k, v, *args)

    def hget(self, name, k):
        """获取值
        c.get('access_token_00b73bbe23f34a468b2a5f158701f17f_wx')
        """
        return self.instance.hget(name, k)

    def remove(self, k):
        """修改值
        c.get('access_token_00b73bbe23f34a468b2a5f158701f17f_wx')
        """
        return self.instance.delete(k)

    def expire(self, k, seconds):
        """设置过期时间"""
        self.instance.expire(k, seconds)







