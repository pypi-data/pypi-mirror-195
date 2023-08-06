from uadatasdk.uadatasdk.__init__ import auth

try:
    from .client import JQDataClient
except:
    from uadatasdk.uadatasdk.client import JQDataClient

try:
    from .utlis import *
except:
    from uadatasdk.uadatasdk.utlis import *
import json

@assert_auth
def get_price(security, start_date='None', end_date='None', frequency='daily',
              fields='None', skip_paused='False', fq='pre', count='None', fill_paused='True'):
    security = convert_security(security)
    start_date = to_date_str(start_date)
    end_date = to_date_str(end_date)
    if (not count) and (not start_date):
        start_date = "2015-01-01"
    if count=='None' and start_date=='None':
        raise ParamsError("(start_date, count) only one param is required")
    elif count!='None' and start_date!='None':
        raise ParamsError("(start_date, count) only one param is required")
    if count != 'None':
        count = str(count)
    print(locals())
    return JQDataClient.instance().get_price(**locals())

@assert_auth
def get_all_securities(date='None'):
    date = to_date_str(date)
    return JQDataClient.instance().get_all_securities(**locals())

@assert_auth
def get_all_trade_days():
    """
    获取所有交易日

    :return 包含所有交易日的 numpy.ndarray, 每个元素为一个 datetime.date 类型.
    """
    data = JQDataClient.instance().get_all_trade_days()
    # if str(data.dtype) != "object":
    #     data = data.astype(datetime.datetime)
    return data

@assert_auth
def get_trade_days(start_date='None', end_date='None', count='None'):
    """
    获取指定日期范围内的所有交易日

    :return numpy.ndarray, 包含指定的 start_date 和 end_date, 默认返回至 datatime.date.today() 的所有交易日
    """
    start_date = to_date_str(start_date)
    end_date = to_date_str(end_date)
    if start_date == None and count == None:
        raise Exception("start_date和coun二选一,不能都为空")
    if count !='None':
        count = str(count)
    data = JQDataClient.instance().get_trade_days(**locals())

    return data

@assert_auth
def get_future_contracts(underlying_symbol, date='None'):
    """
    获取某期货品种在策略当前日期的可交易合约标的列表

    :param security 期货合约品种，如 ‘AG’(白银)
    :return 某期货品种在策略当前日期的可交易合约标的列表
    """
    # assert underlying_symbol, "underlying_symbol is required"
    date = to_date_str(date)
    underlying_symbol = underlying_symbol.upper()

    return JQDataClient.instance().get_future_contracts(underlying_symbol=underlying_symbol, date=date)

@assert_auth
def get_dominant_future(underlying_symbol, date='None'):
    """
    获取主力合约对应的标的

    :param underlying_symbol 期货合约品种，如 ‘AG’(白银)
    :param date 日期（默认为当前时刻，当指定 end_date 时则表示开始日期）
    :param end_date 结束日期，当指定该参数时表示获取一段时间的主力合约
    :return 主力合约对应的期货合约（指定 end_date 时返回 pandas.Series，否则返回字符串）
    """
    date = to_date_str(date)
    cli = JQDataClient.instance()
    return cli.get_dominant_future(underlying_symbol=underlying_symbol, date=date)


@assert_auth
def get_security_info(code):
    assert code, "code is required"
    result = JQDataClient.instance().get_security_info(**locals())
    return Security(**result)

@assert_auth
def normalize_code(code):

    return JQDataClient.instance().normalize_code(**locals())

@assert_auth
def get_extras(fields, security, start_date='None', end_date='None',count='None'):
    if fields == 'open_interest' or fields == 'futures_sett_price':
        start_date = to_date_str(start_date)
        end_date = to_date_str(end_date)
        security = convert_security(security)
        if count == None:
            count = str(count)

        return JQDataClient.instance().get_extras(**locals())
    else:
        raise Exception("{0} erroy".format(fields))