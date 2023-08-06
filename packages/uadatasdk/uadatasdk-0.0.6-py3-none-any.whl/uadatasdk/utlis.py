
import datetime
from functools import wraps
from importlib import import_module
import six


class Security(object):
    code = None
    display_name = None
    name = None
    start_date = None
    end_date = None
    type = None
    parent = None

    def __init__(self, **kwargs):
        self.code = kwargs.get("code", None)
        self.display_name = kwargs.get("display_name", None)
        self.name = kwargs.get("name", None)
        self.start_date = to_date(kwargs.get("start_date", None))
        self.end_date = to_date(kwargs.get("end_date", None))
        self.type = kwargs.get("type", None)
        self.parent = kwargs.get("parent", None)

    def __repr__(self):
        return self.code

    def __str__(self):
        return self.code

def to_date(date):
    """
    >>> convert_date('2015-1-1')
    datetime.date(2015, 1, 1)

    >>> convert_date('2015-01-01 00:00:00')
    datetime.date(2015, 1, 1)

    >>> convert_date(datetime.datetime(2015, 1, 1))
    datetime.date(2015, 1, 1)

    >>> convert_date(datetime.date(2015, 1, 1))
    datetime.date(2015, 1, 1)
    """
    if is_str(date):
        if ':' in date:
            date = date[:10]
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
    elif isinstance(date, datetime.datetime):
        return date.date()
    elif isinstance(date, datetime.date):
        return date
    elif date is None:
        return None
    raise ParamsError("type error")

def is_str(s):
    return isinstance(s, six.string_types)

def to_date_str(dt):
    if dt is None:
        return None

    if isinstance(dt, six.string_types):
        return dt
    if isinstance(dt, datetime.date):
        return dt.strftime("%Y-%m-%d")

class ParamsError(Exception):
    pass

class PandasChecker(object):


    @staticmethod
    def check_version():
        if import_module("pandas").__version__[:4] >= "0.25":
            return True
        return 'False'

    VERSION_NOTICE_MESSAGE = (
        "当前环境 pandas 版本高于 0.25，get_price 与 get_fundamentals_continuously "
        "接口的 panel 参数将固定为 False（0.25 及以上版本的 pandas 不再支持 panel，"
        "如使用该数据结构和相关函数请注意修改）"
    )

def convert_security(s):
    if isinstance(s, six.string_types):
        return s
    elif isinstance(s, Security):
        return str(s)
    elif isinstance(s, (list, tuple)):
        res = []
        for i in range(len(s)):
            if isinstance(s[i], Security):
                res.append(str(s[i]))
            elif isinstance(s[i], six.string_types):
                res.append(s[i])
            else:
                raise ParamsError("can't find symbol {}".format(s[i]))
        return res
    elif s is None:
        return s
    else:
        raise ParamsError("security's type should be Security or list")

def assert_auth(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        from .client import JQDataClient
        if not JQDataClient.instance():
            raise Exception("Please run jqdatasdk.auth first")

        elif True:
            if JQDataClient.instance().inited == True:
                return func(*args, **kwargs)
            else:
                raise Exception("Please run jqdatasdk.auth first")

    return _wrapper
