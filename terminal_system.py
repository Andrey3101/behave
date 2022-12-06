import requests
import logging
import urllib3

urllib3.disable_warnings()

class terminalApi():
    def __init__(self, url):
        self.t_url = url
        self.log = logging.getLogger("terminal_api")

    def add_reserve(self, reserve_body):
        rezervation_url = self.t_url + '/acceptor/acceptorAuthorization'
        self.log.debug(rezervation_url)
        req = requests.post(rezervation_url, headers= {"Content-Type": "application/json"}, data= reserve_body.encode('utf-8'), verify= False)
        return req
    
    def add_debit(self, wallet_transaction):
        spisanie_url = self.t_url + '/acceptor/acceptorBatchTransfer'
        self.log.debug(spisanie_url)
        req = requests.post(spisanie_url, headers= {"Content-Type": "application/json"}, data= wallet_transaction.encode('utf-8'), verify= False)
        return req

    def add_cancell(self, cancell_transaction):
        cancell_url = self.t_url + '/acceptor/acceptorCancellation'
        self.log.debug(cancell_url)
        req = requests.post(cancell_url, headers= {"Content-Type": "application/json"}, data= cancell_transaction.encode('utf-8'), verify= False)
        return req

    def add_refund(self, refund_transaction):
        refund_url = self.t_url + '/acceptor/acceptorRefund'
        self.log.debug(refund_url)
        req = requests.post(refund_url, headers= {"Content-Type": "appliction/json"}, data= refund_transaction.encode('utf-8'), verify= False)
        return req