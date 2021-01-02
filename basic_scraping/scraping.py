import datetime
import os
import shutil
import time
from urllib import request

from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pandas as pd


def scraping(mkt, symbol, outfolder):
    """
    url先の <div id="chart_search_left"> の <img> を取得する。
    1つ処理するごとに4秒ほど休むのは、スクレイピングルールです。
    （※viet-kabu.comがスクレイピング対象の画像を表示しなくなったので動くけど機能しません）
    """
    dic = {"HOSE": 'hcm', "HNX": 'hn'}
    url = 'https://www.viet-kabu.com/{0}/{1}.html'.format(dic[mkt], symbol)
    soup = BeautifulSoup(request.urlopen(url).read(), 'lxml')
    tag_img = soup.find(id='chart_search_left').find('img')
    if tag_img:
        request.urlretrieve(tag_img['src'], outfolder + '/{0}.png'.format(symbol))
        print(symbol)
    time.sleep(4)

# mysql
CON_STR = 'mysql+mysqldb://python:python123@127.0.0.1/pythondb?charset=utf8&use_unicode=1'
CON = create_engine(CON_STR, echo=False).connect()

# delete old files
OUTFOLDER = os.path.dirname(os.path.abspath(__file__)) + '/chart'
shutil.rmtree(OUTFOLDER)
os.mkdir(OUTFOLDER)

# top 5 by industry
print('\n' + 'top 5')
# sql
CON.execute('DELETE FROM vietnam_research_dailytop5')
AGG = pd.read_sql_query(
    '''
    SELECT
          CONCAT(c.industry_class, '|', i.industry1) AS ind_name
        , i.market_code
        , i.symbol
        , AVG(i.trade_price_of_a_day) AS trade_price_of_a_day
        , AVG(i.per) AS per
    FROM (vietnam_research_industry i INNER JOIN vietnam_research_indclass c
        ON i.industry1 = c.industry1) INNER JOIN vietnam_research_sbi s
        ON i.market_code = s.market_code AND i.symbol = s.symbol
    GROUP BY ind_name, i.market_code, i.symbol
    HAVING per >1;
    ''', CON)

# criteria
CRITERIA = [{"by": ['trade_price_of_a_day', 'per'], "order": False},
            {"by": ['ind_name', 'trade_price_of_a_day', 'per'], "order": [True, False, False]}]

# Sort descending and get top 5
AGG = AGG.sort_values(by=CRITERIA[0]["by"], ascending=CRITERIA[0]["order"])
AGG = AGG.groupby('ind_name').head()

# Sort descending and insert table
AGG = AGG.sort_values(by=CRITERIA[1]["by"], ascending=CRITERIA[1]["order"])
AGG.to_sql('vietnam_research_dailytop5', CON, if_exists='append', index=None)

# scraping from top 5 list
for i, row in AGG.iterrows():
    scraping(row['market_code'], row['symbol'], OUTFOLDER)

# log
with open(os.path.dirname(os.path.abspath(__file__)) + '/result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'stock_chart.py')

# Output
print('Congrats!')
time.sleep(2)
