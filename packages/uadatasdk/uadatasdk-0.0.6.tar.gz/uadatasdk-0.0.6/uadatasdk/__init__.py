from .client import JQDataClient
from .api import *
from .server_clien import *
from .utlis import *
def auth(username, password, host=None, port=None):
    """账号认证"""
    JQDataClient.set_auth_params(
        username=username,
        password=password,
    )