import requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from testforPPshare.util.text import paramter_wrong
import testforPPshare.stock.cons as cs


def get_bor(curr_type, period, market_code):
    """
    爬取easymoney网站数据的函数
    """

    (pages, df) = get_df(curr_type=curr_type,
                         page=1,
                         market_code=market_code,
                         check=True,
                         period=period)
    futures = thread(pages=pages,
                     df=df,
                     curr_type=curr_type,
                     period=period,
                     market_code=market_code)
    for future in futures:
        df = df.append(future.result(), ignore_index=True)
    for i in [
            'INDICATOR_ID', 'LATEST_RECORD', 'MARKET', 'MARKET_CODE',
            'CURRENCY', 'CURRENCY_CODE'
    ]:
        del df[i]
    df.columns = ['日期', '时期', '利率（%）', '涨跌（BP）']
    return df


def get_df(page, curr_type, period, market_code, check=False, df=0):
    if len(period) != 2:
        raise Exception(paramter_wrong('period'))
    else:
        if period == 'ON':
            num = '001'
        elif 'W' in period:
            num = '1{:02}'.format(int(period[:-1]))
        elif 'M' in period:
            num = '2{:02}'.format(int(period[:-1]))
        elif 'Y' in period:
            num = '3{:02}'.format(int(period[:-1]))
        else:
            raise Exception(paramter_wrong('period'))
    # print(f"正在爬取第{page}页")
    # url = 'https://datacenter-web.eastmoney.com/api/data/v1/get?'
    data = cs.get_data(market_code, curr_type, num, page)
    url = cs.URL_TYPE['https'] + cs.URL_DIC['easymoney'] + cs.URL_PARA[
        'easymoney']
    res = requests.get(url=url, params=data)
    try:
        data = res.json()['result']['data']
    except:
        raise Exception(paramter_wrong('period'))
    if check:
        df = pd.DataFrame(data[0], index=[0])
        for i in data[1:]:
            df = df.append(i, ignore_index=True)
        return (res.json()['result']['pages'], df)
    else:
        return data


def thread(pages, df, curr_type, period, market_code):
    futures = []
    with ThreadPoolExecutor(20) as t:
        for page in range(2, pages + 1):
            future = t.submit(get_df,
                              page=page,
                              df=df,
                              period=period,
                              curr_type=curr_type,
                              market_code=market_code)
            futures.append(future)
    # print("爬取完成")
    return futures


if __name__ == '__main__':
    print(get_bor(curr_type='JPY', period='8M', market_code='003'))
