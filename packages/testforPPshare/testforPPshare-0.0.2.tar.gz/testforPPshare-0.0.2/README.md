# testforPPshare使用指南（by@zemengchuan）
GitHub链接：https://github.com/zemengchuan/PPtest

## 用途：

testforPPshare是PPshare项目的测试版本，目前的功能是集成了许多爬取宏观数据的爬虫

## 安装方式

```python
pip install testforPPshare
```

## 使用方式

```python
import testforPPshare as tp
```

- 获取上海银行间同业拆放利率
  shibor(mode='data', start_date=None, end_date=datetime.date.today())
  三个参数都有默认值，直接调用即可。默认是一个月前到今天的数据。mode可以选择
    - Shibor：data
    - shibor报价数据：quote
    - shibor均值数据：avg
```python
tp.shibor()
```