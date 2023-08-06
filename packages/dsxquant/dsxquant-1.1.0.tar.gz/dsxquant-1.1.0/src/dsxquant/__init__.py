from typing import Union
from dsxquant.config import config
# 默认服务器
config.DEFAULT_SERVER_IP = "129.211.209.104"
config.DEFAULT_PORT = 8085
from dsxquant.config.config import MARKET
from dsxquant.dataser.dsx_dataser import DsxDataser
from dsxquant.dataser.parser.base import BaseParser
# 市场编号
market = MARKET
# 周期
cycle = config.CYCLE
# 复权
fq = config.FQ
# 报表类型
report_type = config.REPORT_TYPE
# 数据采集器
dataser = DsxDataser
# 解析器
parser = BaseParser
# 默认维护一个连接
conn:DsxDataser = DsxDataser()
def close():
    conn.close()
def connect():
    if not conn.connected:conn.connect()
    return True
# 下面重新封装一下
def get_category(category_id:int=0) -> Union[BaseParser,None]:
    if connect():  return conn.get_category(category_id)

def get_hangye() -> Union[BaseParser,None]:
    if connect():  return conn.get_hangye()

def get_gainian() -> Union[BaseParser,None]:
    if connect():  return conn.get_gainian()

def get_diyu() -> Union[BaseParser,None]:
    if connect():  return conn.get_diyu()

def get_stocks(market:int=None,symbol:str=None,hangye:str=None,gainian:str=None,diyu:str=None,listing_date:str=None) -> Union[BaseParser,None]:
    if connect():  return conn.get_stocks(market,symbol,hangye,gainian,diyu,listing_date)

def get_quotes(symbols:Union[list,str,tuple]) -> Union[BaseParser,None]:
    if connect():  return conn.get_quotes(symbols)

def get_klines(symbol:str,market:int,page:int=1,page_size:int=320,fq:str=config.FQ.DEFAULT,cycle:config.CYCLE=config.CYCLE.DAY) -> Union[BaseParser,None]:
    if connect():  return conn.get_klines(symbol,market,page,page_size,fq,cycle)

def get_finance(symbol,market:int,report_type:config.REPORT_TYPE=config.REPORT_TYPE.DEFAULT,report_date="") -> Union[BaseParser,None]:
    if connect():  return conn.get_finance(symbol,market,report_type,report_date)

def get_sharebonus(symbol:str,market:int,start:str=None,end:str=None) -> Union[BaseParser,None]:
    if connect():  return conn.get_sharebonus(symbol,market,start,end)

def get_factors(symbol:str,market:int) -> Union[BaseParser,None]:
    if connect():  return conn.get_factors(symbol,market)

def get_timeshring(symbol:str,market:int,trade_date:str="") -> Union[BaseParser,None]:
    if connect():  return conn.get_timeshring(symbol,market,trade_date)

def get_translist(symbol:str,market:int,trade_date:str="",page:int=1,page_size:int=10) -> Union[BaseParser,None]:
    if connect():  return conn.get_quotes(symbol,market,trade_date,page,page_size)