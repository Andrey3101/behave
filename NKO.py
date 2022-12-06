import requests
import logging
import urllib3

urllib3.disable_warnings()

class nkoApi():
    def __init__(self, url):
        self.nko_url = url
        self.log = logging.getLogger("nko_api")

    def add_wallet(self, post_data):
        add_wallet_url = self.nko_url + '/cards/api/v1/surrogate/add'
        self.log.debug(add_wallet_url)
        req = requests.post(add_wallet_url, headers= {"Content-Type": "application/json"}, data= post_data, verify= False)
        return req
    
    def wallet_get_data(self, post_data):
        wallet_get_data_url = self.nko_url + '/cards/api/v1/wallet/get_data'
        self.log.debug(wallet_get_data_url)
        req = requests.post(wallet_get_data_url, headers= {"Content-Type": "application/json"}, data= post_data, verify= False)
        return req

    def check_credit(self, post_data):
        check_credit_url = self.nko_url + '/transactions/api/v1/credit/check'
        self.log.debug(check_credit_url)
        req = requests.post(check_credit_url, headers= {"Content-Type": "application/json"}, data= post_data, verify= False)
        return req

    def add_credit(self, post_data):
        add_credit_url = self.nko_url + '/transactions/api/v1/credit/add'
        self.log.debug(add_credit_url)
        req = requests.post(add_credit_url, headers= {"Content-Type": "application/json"}, data= post_data, verify= False)
        return req

    def check_balance (self, post_data):
        check_balance_url = self.nko_url + '/cards/api/v1/wallet/get_data'
        self.log.debug(check_balance_url)
        req = requests.post(check_balance_url, headers= {"Content-Type": "application/json"}, data= post_data, verify= False)
        return req

    def wallet_write (self, post_data):
        write_off_url = self.nko_url + '/transactions/api/v1/debit/add'
        self.log.debug(write_off_url)
        req = requests.post(write_off_url, headers= {"Content-Type": "application/json"}, data= post_data, verify= False)
        return req