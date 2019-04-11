import time
from functools import wraps

import pendulum


def timer(func):
    """
    calculate function spend time
    :param func:
    :return:
    """

    @wraps(func)
    def timed(*args, **kwargs):
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("spend time:{}".format(end - begin))

    return timed


def url2path(url):
    """
    replace '/' to '_' to transfer url to file_path
    :param url: string
    :return:
    """
    return url.strip().replace("/", "_")


def absolute_time(time_str):
    """
    parse time  string like '1小时前' --->'pendulum.now().subtract(1) '
    :param time_str: string
    :return: string
    """
    time_str = "1 小时前"
    num = time_str.strip()[0]
    if not isinstance(int(num), int):
        return
    now = pendulum.now(tz="Asia/shanghai")
    real_time = now.subtract(years=1)
    print(now, real_time)


class Http404Exception(Exception):
    """
    cache 404 exception
    """

    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg
