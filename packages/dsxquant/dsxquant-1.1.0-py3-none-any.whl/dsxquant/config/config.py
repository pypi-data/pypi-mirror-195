
import struct
# 调试模式
DSXDEBUG = True
# 默认服务器地址
DEFAULT_SERVER_IP = None
# 默认服务器端口号
DEFAULT_PORT = None
# 周期
class CYCLE:
    T='t'                           # 分时线
    T5='t5'                         # 五日分时线
    DAY="day"                       # 日K
    WEEK="week"                     # 周K
    MONTH="month"                   # 月K
    YEAR="year"                     # 年K
    M1="m1"                         # 1分钟K
    M5="m5"                         # 5分钟K
    M15="m15"                       # 15分钟K
    M30="m30"                       # 30分钟K
    M60="m60"                       # 60分钟K
# 市场代码
class MARKET:
    SH=0                            # 上交所
    SZ=1                            # 深交所
    BJ=2                            # 北交所
    HK=3                            # 港交所
    US=4                            # 美国
# 复权类型
class FQ:
    DEFAULT=''                      # 默认不复权
    QFQ="qfq"                       # 前复权
    HFQ="hfq"                       # 后复权
# 财务报表类型
class REPORT_TYPE:
    DEFAULT=''                      # 财务简报
    INDEX='index'                   # 财务指标
    PROFIT="profit"                 # 利润表
    CASHFLOW="cashflow"             # 现金流量表
    BALANCESHEET="balancesheet"     # 资产负债表

# socket 连接超时
CONNECT_TIMEOUT = 30
# 打包格式符 b 0=不压缩 1=压缩 i 为包大小
PACK_TYPE = 'bi'
# 消息协议头部长度，根据打包格式符自动计算
HEADER_LEN = struct.calcsize(PACK_TYPE)
# 是压缩传输数据
ENABLE_GZIP = True

