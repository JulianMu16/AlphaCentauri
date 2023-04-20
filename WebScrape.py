import requests
from bs4 import BeautifulSoup as bs
def DataPull():
    link_1 = 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/40,-110/land_ocean/all/1/2011-2013'
    neg110 = []
    link_2 = 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/40,-100/land_ocean/all/1/2011-2013'
    neg100 =[]
    link_3 = 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/40,-90/land_ocean/all/1/2011-2013'
    neg90 =[]
    link_3 = 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/40,-80/land_ocean/all/1/2011-2013'
    neg80 =[]
    

    page = requests.get(link_1)
    soup = bs(page.content,'lmxl')
    table = soup.find('div', id = 'page-content').find('div', id = 'data-table').find('td')
    # data one loop
    return table
DataPull()