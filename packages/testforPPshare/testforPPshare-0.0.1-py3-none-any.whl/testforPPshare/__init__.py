"""
获取上海银行间同业拆放利率（Shibor）
贷款基础利率（LPR）
"""
from testforPPshare.stock.shibor import (shibor, LPR)
"""
获取中国银行同业间拆借市场数据（chinbor）
伦敦银行同业间拆借市场数据（Libor）
香港银行同业间拆借市场数据（hibor）
欧洲银行同业间拆借市场数据（euribor）
新加坡银行同业间拆借市场数据（sibor）
"""
from testforPPshare.stock.bor import (get_chinbor, get_euribor, get_hibor, get_libor,
                              get_sibor)
