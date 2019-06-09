#！/usr/bin/env python
#! -*-coding:utf-8 -*-

import requests
import hmac
import operator

#Major retry
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

try:
    from urllib import urlencode
# python3
except ImportError:
    from urllib.parse import urlencode

BASE_API_HOST = "https://api.bkex.vip"

class BkexAPI:

    def __init__(self, secretkey, accesskey):
        self.__Secret_Key = str(secretkey)
        self.__Access_Key = str(accesskey)

    def __encryption(self, sort_data):
        signature = hmac.new(self.__Secret_Key.encode("utf-8"),sort_data.encode("utf-8"),digestmod="SHA256").hexdigest()
        return signature

    def __create_header(self, sort_data):
        signature = self.__encryption(sort_data)
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            'Cache-Control': 'no-cache',
            "Content-Type": "application/x-www-form-urlencoded",
            "X_ACCESS_KEY": self.__Access_Key,
            "X_SIGNATURE": signature
        }
        return headers

    def __sort_dict(self, massage):
        return urlencode(dict(sorted(massage.items(), key=operator.itemgetter(0))))

    def __sign(self,method, url, params={}):
        adapter = HTTPAdapter(max_retries=3)
        res = requests.Session()
        res.mount(url, adapter)
        try:
            sort_data = self.__sort_dict(params)
            headers = self.__create_header(sort_data)
            return res.request(method, url, params=params, headers=headers, timeout=30).json()
        except Exception as e:
            return f'the error is {e}'
        except ConnectionError as ce:
            return f'connect timeout error is {ce}'

    def __get_no_sign(self, method, url, params):
        adapter = HTTPAdapter(max_retries=3)
        res = requests.Session()
        res.mount(url, adapter)
        try:
            sort_data = self.__sort_dict(params)
            headers = self.__create_header(sort_data)
            return res.request(method, url, params=sort_data or {},headers=headers, timeout=30).json()
        except Exception as e:
            return f'the error is {e}'
        except ConnectionError as ce:
            return f'connect timeout error is {ce}'

    def get_wallet_balance(self,**kwargs):
        path = f'{BASE_API_HOST}/v1/u/wallet/balance'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_exchangeinfo(self,**kwargs):
        path = f'{BASE_API_HOST}/v1/exchangeInfo'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_quotation_depth(self,**kwargs):
        '''
        :e.g.:
         start.get_quotation_depth(pair='BTC_USDT',size=100,precision=3)
        '''
        path = f'{BASE_API_HOST}/v1/q/depth'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_quotation_deals(self,**kwargs):
        '''
        :e.g.:
        start.get_quotation_deals(pair='BKK_USDT',size=20)
        '''
        path = f'{BASE_API_HOST}/v1/q/deals'
        return self.__get_no_sign('GET', path, params=kwargs)

    def get_24hr_ticker_price_change_statistics(self,**kwargs):
        '''
        :e.g.:
        start.get_24hr_ticker_price_change_statistics(pair='BKK_USDT')
        '''
        path = f'{BASE_API_HOST}/v1/q/ticker'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_pair_price_ticker(self,**kwargs):
        '''
        :e.g.:
        start.get_pair_price_ticker(pair='BKK_USDT')
        '''
        path = f'{BASE_API_HOST}/v1/q/ticker/price'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_kline(self,**kwargs):
        '''
        :e.g.:
        start.get_kline(pair='BKK_USDT',interval='1m',size=500)
        '''
        path = f'{BASE_API_HOST}/v1/q/kline'
        return self.__get_no_sign('GET',path,params=kwargs)

    def get_all_unfinished_order(self,**kwargs):
        '''
        :e.g.:
        start.get_all_unfinished_order(pair='BKK_USDT',size=100,page=1,direction="BID")
        '''
        path = f'{BASE_API_HOST}/v1/u/trade/order/listUnfinished'
        return self.__sign('GET',path,params=kwargs)

    def get_all_finished_order(self,**kwargs):
        '''
        :e.g.:
        start.get_all_finished_order(pair='BKK_USDT',page=1,size=10,starttime=1558700996000,endtime=1558704596000,direction='BID')
        '''
        path = f'{BASE_API_HOST}/v1/u/trade/order/history'
        return self.__sign('GET',path,params=kwargs)

    def create_new_order(self,**kwargs):
        '''
        :e.g.:
       start.create_new_order(pair='BKK_USDT',price=0.0001,amount=10,direction='BID')
        '''
        path = f'{BASE_API_HOST}/v1/u/trade/order/create'
        return self.__sign('POST',path,params=kwargs)

    def cancel_order(self,**kwargs):
        '''

        :e.g.:
        start.cancel_order(pair='BKK_USDT',orderNo='2019052421031411851080140'
        '''
        path = f'{BASE_API_HOST}/v1/u/trade/order/cancel'
        return self.__sign('POST',path,params=kwargs)

    def batch_create_new_order(self,**kwargs):
        '''
        :e.g.:
       start.create_new_order(pair='BKK_USDT',price=0.0001,amount=10,direction='BID')
        '''
        path = f'{BASE_API_HOST}/v1/u/trade/order/batchCreate'
        return self.__sign('POST', path, params=kwargs)

if __name__ == "__main__":

    secret_key = ""
    access_key = ""
    start = BkexAPI(secret_key,access_key)

