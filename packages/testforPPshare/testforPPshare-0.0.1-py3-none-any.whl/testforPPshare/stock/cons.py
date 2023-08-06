def get_data(market_code, curr_type, num, page):
    result = {
        'reportName':
        'RPT_IMP_INTRESTRATEN',
        'columns':
        'REPORT_DATE,REPORT_PERIOD,IR_RATE,CHANGE_RATE,INDICATOR_ID,LATEST_RECORD,MARKET,MARKET_CODE,CURRENCY,CURRENCY_CODE',
        'filter':
        '(MARKET_CODE="{}")(CURRENCY_CODE="{}")(INDICATOR_ID="{}")'.format(
            market_code, curr_type, num),
        'pageNumber':
        page,
        'pageSize':
        '100',
        'sortTypes':
        '-1',
        'sortColumns':
        'REPORT_DATE',
        'p':
        page,
        'pageNo':
        page,
        'pageNum':
        page,
    }
    return result


URL_TYPE = {'https': 'https://', 'http': 'http://', 'ftp': 'ftp://'}

URL_DIC = {
    'easymoney': 'datacenter-web.eastmoney.com/',
    'shibor': 'www.shibor.org/dqs/rest/cm-u-bk-shibor/'
}

URL_PARA = {
    'easymoney': 'api/data/v1/get?',
    'data': 'ShiborHisExcel?lang=cn&startDate={}&endDate={}',
    'quote':
    'ShiborPriHisExcel?lang=cn&startDate={}&endDate={}&memCode=|100000111000000101001|100000211000000101001|100000311000000101001|100000411000000101001|100000531000000102001|100000844030000102001|100000711000000102001|100000911000000102001|100001435010000102001|200001131000000102001|101000111000000104001|102000031000000104001|290000531000000106001|100001011000000102001|100001244010000102001|101050011000000208011|100005311000000103001|100001511000000102001&instnCnNm=|%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C|%E5%86%9C%E4%B8%9A%E9%93%B6%E8%A1%8C|%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C|%E5%BB%BA%E8%AE%BE%E9%93%B6%E8%A1%8C|%E4%BA%A4%E9%80%9A%E9%93%B6%E8%A1%8C|%E6%8B%9B%E5%95%86%E9%93%B6%E8%A1%8C|%E4%B8%AD%E4%BF%A1%E9%93%B6%E8%A1%8C|%E5%85%89%E5%A4%A7%E9%93%B6%E8%A1%8C|%E5%85%B4%E4%B8%9A%E9%93%B6%E8%A1%8C|%E6%B5%A6%E5%8F%91%E9%93%B6%E8%A1%8C|%E5%8C%97%E4%BA%AC%E9%93%B6%E8%A1%8C|%E4%B8%8A%E6%B5%B7%E9%93%B6%E8%A1%8C|%E6%B1%87%E4%B8%B0%E9%93%B6%E8%A1%8C|%E6%B1%87%E4%B8%B0%E4%B8%AD%E5%9B%BD|%E5%8D%8E%E5%A4%8F%E9%93%B6%E8%A1%8C|%E5%B9%BF%E5%8F%91%E9%93%B6%E8%A1%8C|%E9%82%AE%E5%82%A8%E9%93%B6%E8%A1%8C|%E5%9B%BD%E5%BC%80%E8%A1%8C|%E6%B0%91%E7%94%9F%E9%93%B6%E8%A1%8C&instnEnNm=|ICBC|ABC|BOC|CBC|BOCOM|CMB|CNCB|CEB|CIB|SPDB|BOB|BOS|HSBC|HXB|GDB|PSBC|CDB|CMSB',
    'avg': 'ShiborMnHisExcel?lang=cn&startDate={}&endDate={}&tendencyvalue='
}
