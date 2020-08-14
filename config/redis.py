import redis

# host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
cache = redis.Redis(connection_pool=pool)


def update_sid_uid_map(sid, uid):
    maps = cache.hgetall('sid_uid_map')
    if maps is None:
        return
    maps[sid] = uid
    cache.hmset('sid_uid_map', maps)
    print('update_sid_uid_map--{}--update--{}'.format(maps, (sid, uid)))


def get_uid_with_sid(sid):
    maps = cache.hgetall('sid_uid_map')
    print('get_uid_with_sid--{}'.format(maps))
    if maps is None:
        return None
    return maps[sid]


def add_online_uids(uid):
    cache.sadd('online_uids', uid)
    print('add_online_uids--{}'.format(cache.smembers('online_uids')))


def remove_online_uids(uid):
    cache.srem('online_uids', uid)
    print('add_online_uids--{}'.format(cache.smembers('online_uids')))


def get_online_uids():
    sets = cache.smembers('online_uids')
    return sets
