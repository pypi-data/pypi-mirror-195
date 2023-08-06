import pandas as pd
import datetime
import testforPPshare.stock.cons as cs


def shibor(mode='data', start_date=None, end_date=datetime.date.today()):
    """
    获取上海银行间同业拆放利率（Shibor）：data
    shibor报价数据：quote
    shibor均值数据：avg
    Parameters
    ------
    start_year:起始年份(%Y-%M-%D)
    end_year:截止年份(%Y-%M-%D)
    Return
    ------
    date:日期
    ON:隔夜拆放利率
    1W:1周拆放利率
    2W:2周拆放利率
    1M:1个月拆放利率
    3M:3个月拆放利率
    6M:6个月拆放利率
    9M:9个月拆放利率
    1Y:1年拆放利率
    """
    # url = {
    #     'data':
    #     'https://www.shibor.org/dqs/rest/cm-u-bk-shibor/ShiborHisExcel?lang=cn&startDate={}&endDate={}',
    #     'quote':
    #     'https://www.shibor.org/dqs/rest/cm-u-bk-shibor/ShiborPriHisExcel?lang=cn&startDate={}&endDate={}&memCode=|100000111000000101001|100000211000000101001|100000311000000101001|100000411000000101001|100000531000000102001|100000844030000102001|100000711000000102001|100000911000000102001|100001435010000102001|200001131000000102001|101000111000000104001|102000031000000104001|290000531000000106001|100001011000000102001|100001244010000102001|101050011000000208011|100005311000000103001|100001511000000102001&instnCnNm=|%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C|%E5%86%9C%E4%B8%9A%E9%93%B6%E8%A1%8C|%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C|%E5%BB%BA%E8%AE%BE%E9%93%B6%E8%A1%8C|%E4%BA%A4%E9%80%9A%E9%93%B6%E8%A1%8C|%E6%8B%9B%E5%95%86%E9%93%B6%E8%A1%8C|%E4%B8%AD%E4%BF%A1%E9%93%B6%E8%A1%8C|%E5%85%89%E5%A4%A7%E9%93%B6%E8%A1%8C|%E5%85%B4%E4%B8%9A%E9%93%B6%E8%A1%8C|%E6%B5%A6%E5%8F%91%E9%93%B6%E8%A1%8C|%E5%8C%97%E4%BA%AC%E9%93%B6%E8%A1%8C|%E4%B8%8A%E6%B5%B7%E9%93%B6%E8%A1%8C|%E6%B1%87%E4%B8%B0%E9%93%B6%E8%A1%8C|%E6%B1%87%E4%B8%B0%E4%B8%AD%E5%9B%BD|%E5%8D%8E%E5%A4%8F%E9%93%B6%E8%A1%8C|%E5%B9%BF%E5%8F%91%E9%93%B6%E8%A1%8C|%E9%82%AE%E5%82%A8%E9%93%B6%E8%A1%8C|%E5%9B%BD%E5%BC%80%E8%A1%8C|%E6%B0%91%E7%94%9F%E9%93%B6%E8%A1%8C&instnEnNm=|ICBC|ABC|BOC|CBC|BOCOM|CMB|CNCB|CEB|CIB|SPDB|BOB|BOS|HSBC|HXB|GDB|PSBC|CDB|CMSB',
    #     'avg':
    #     'https://www.shibor.org/dqs/rest/cm-u-bk-shibor/ShiborMnHisExcel?lang=cn&startDate={}&endDate={}&tendencyvalue='
    # }
    url = cs.URL_TYPE['https'] + cs.URL_DIC['shibor'] + cs.URL_PARA[mode]
    if not start_date:
        start_date = end_date - datetime.timedelta(days=30)
    df = pd.read_excel(url.format(start_date, end_date))[:-2]
    return df


def LPR(start_date=None, end_date=datetime.date.today()):
    """
    获取贷款基础利率（LPR）
    Parameters
    ------
    start_year:起始年份(%Y-%M-%D)
    end_year:截止年份(%Y-%M-%D)
    Return
    ------
    date:日期
    1Y:1年贷款利率
    5Y:5年贷款利率
    """
    if not start_date:
        start_date = end_date - datetime.timedelta(weeks=53)
    url = cs.URL_TYPE['https'] + cs.URL_DIC['LPR'] + cs.URL_PARA['LPR']
    df = pd.read_excel(url.format(start_date, end_date))[:-2]
    return df


if __name__ == '__main__':
    # print(shibor('data'))
    # print(shibor('queto'))
    # print(shibor('avg'))
    print(LPR())