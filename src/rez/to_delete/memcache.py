from rez.config import config
from rez.vendor.memcache import memcache
from rez.utils.logging_ import print_debug


_g_client = None


def connect():
    global _g_client

    if config.memcache_uri and _g_client is None:
        if config.debug("memcache"):
            print_debug("connecting to memcache servers %s." % config.memcache_uri)

        _g_client = memcache.Client(config.memcache_uri,
                                    debug=int(config.memcache))

    return _g_client


def disconnect():
    global _g_client

    if _g_client:
        if config.debug("memcache"):
            print_debug("disconnecting all memcache servers.")

        _g_client.disconnect_all()
        _g_client = None


def get(key, search_path=None):
    if search_path and search_path not in config.memcache_search_paths:
        return None

    connection = connect()

    if connection:
        if config.debug("memcache"):
            print_debug("fetching key '%s' from memcache." % key)

        return connection.get(key)

    return None


def set(key, value, search_path=None):
    if search_path and search_path not in config.memcache_search_paths:
        return False

    connection = connect()

    if connection:
        if config.debug("memcache"):
            print_debug("setting key '%s' in memcache." % key)

        return connection.set(key, value, time=config.memcache_ttl)

    return False