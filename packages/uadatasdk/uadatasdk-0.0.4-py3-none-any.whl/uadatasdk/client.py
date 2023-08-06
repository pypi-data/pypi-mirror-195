import itertools
import random
import socket
import threading
import time
from os import getenv
import platform
from thriftpy2 import transport, protocol
from thriftpy2.rpc import make_client
from .server_clien import pingpong_thrift
import json
import pandas
import numpy
if platform.system().lower() != "windows":
    socket_error = (transport.TTransportException, socket.error, protocol.cybin.ProtocolError)
else:
    socket_error = (transport.TTransportException, socket.error)
print(socket_error)
class JQDataClient(object):
#threading.local()可以为每个线程创建自己的局部名称空间, 放入到该局部空间的数据不会被其他线程干扰
    _threading_local = threading.local()
    _auth_params = {}
    request_attempt_count = 3
    _instance = getattr(_threading_local, '_instance', None)
    _address = getenv('address')
    _post = int(getenv('post'))

    @classmethod
    def instance(cls):
        #判断有没有_instance
        _instance = getattr(cls._threading_local, '_instance', None)
        if _instance is None:
            if not cls._auth_params:
                username = cls._get_username_from_env()
                password = cls._get_password_from_env()
                if username and password:
                    cls._auth_params = {
                        "username": username,
                        "password": password,

                    }
            if cls._auth_params:
                _instance = JQDataClient(**cls._auth_params)

            cls._threading_local._instance = _instance

        return _instance

    def __init__(self,username="", password=""):
        self.username = username
        self.password = password



        self.client = None
        self.inited = False
        self.not_auth = True
        self.compress = True

        self._request_id_generator = itertools.count(
            random.choice(range(0, 1000, 10))
        )


    @staticmethod
    def _get_auth_param_from_env(name):
        for prefix in ["UADATA", "UADATASDK"]:
            value = getenv('_'.join([prefix, name]).upper())
            if value:
                return value


    @classmethod
    def _get_username_from_env(cls):
        for name in ["username", "user", "account", "mob"]:
            value = cls._get_auth_param_from_env(name)
            if value:
                return value


    @classmethod
    def _get_password_from_env(cls):
        for name in ["password", "passwd"]:
            value = cls._get_auth_param_from_env(name)
            if value:
                return value
    def query(self, method, params):

        # params["timeout"] = self.request_timeout
        # #一个1000以内的数字

        client = make_client(pingpong_thrift.PingPong,self._address,self._post,timeout=100*100)
        params = str(params)
        params = params.encode()

        result = client.query(method, params)
        return self.result(result)

    def result(self,result):
        result = result.replace("'", '"')
        result = json.loads(result)
        err = result.get('error', None)
        if err:
            raise Exception("{0}".format(err))
        type = result.pop('type')
        if type == 'DataFrame':

            column = result.pop('column')

            df = pandas.DataFrame(result.values(),index=result.keys(),columns=column)
            return df
        elif type == 'ndarray':
            result = result['data']
            result = numpy.array(result)
            return result
        elif type == 'list':
            return result['data']
        elif type =='str':
            return result['data']
        else:
            return result['data']

    def __call__(self, method, **kwargs):
        err, result = None, None
        for _ in range(self.request_attempt_count):
            try:
                result = self.query(method, kwargs)

                break
            except socket_error as ex:
                if not self._ping_server():
                    self._reset()
                err = ex
                time.sleep(0.6)
            except ResponseError as ex:
                err = ex

        if result is None and isinstance(err, Exception):
            raise err

        return result
    def __getattr__(self, method,):

        return lambda **kwargs: self(method, **kwargs)


    @classmethod
    def set_auth_params(cls, **params):
        if params != cls._auth_params and cls.instance():
            #关闭连接
            cls.instance()._reset()
            cls._threading_local._instance = None
        cls._auth_params = params
        cls.instance().ensure_auth()
    #创建thrift连接
    def _create_client(self):
        self.client = make_client(
            pingpong_thrift.PingPong,self._address,self._post)
        return self.client
    def ensure_auth(self):
        if self.username:
            print("zli")
            error, response = None, None
            for _ in range(self.request_attempt_count):
                try:
                    self._create_client()
                    response = self.client.auth(
                        self.username,
                        self.password,
                    )
                    break
                except socket_error as ex:
                    error = ex
                    time.sleep(0.5)
                    if self.client:
                        self.client.close()
                        self.client = None
                    continue

            if response.get('error'):
                self._auth_params = {}
                raise Exception('{}'.format(response['error']))
        self.inited = True

    #关闭连接
    def _reset(self):
        if self.client:
            self.client.close()
            self.client = None
        self.inited = False
        self.http_token = ""




class PanelObsoleteWarning(Warning):
    """Pandas 的 panel 结构过时警告"""


class ResponseError(Exception):
    """响应错误"""

