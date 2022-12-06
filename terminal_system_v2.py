import requests
import logging
import urllib3

urllib3.disable_warnings()

class terminalApi_v2():
    def __init__(self, url):
        self.t2_url = url
        self.log = logging.getLogger("terminal_v2_api")
    # Авторизация по полученному токену за ТСП
    def auth(self, post_data):
        auth_url = self.t2_url + '/auth'
        self.log.debug(auth_url)
        req = requests.post(auth_url, headers= {"Content-Type": "application/json"}, data= post_data, verify= False)
        return req
    # Резервирование средств
    def batch_auth(self, guid_token, post_data):
        batch_url = self.t2_url + '/batch/auth'
        self.log.debug(batch_url)
        req = requests.post(batch_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token},data= post_data, verify= False)
        return req
    # Списание средств
    def batch_transfer(self, guid_token, post_data):
        transfer_url = self.t2_url + '/batch/transfer'
        self.log.debug(transfer_url)
        req = requests.post(transfer_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token}, data= post_data, verify= False)
        return req
    # Отмена зарезервированных средств
    def batch_cancell(self, guid_token, post_data):
        cancell_url = self.t2_url + '/batch/cancellation'
        self.log.debug(cancell_url)
        req = requests.post(cancell_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token}, data= post_data, verify= False)
        return req
    # Возврат средств
    def batch_refund(self, guid_token, post_data):
        refund_url = self.t2_url + '/batch/refund'
        self.log.debug(refund_url)
        req = requests.post(refund_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token}, data= post_data, verify= False)
        return req
    # Получение социальной программы
    def reference_sog_prog(self, guid_token):
        reference_url = self.t2_url + '/reference/socialPrograms'
        self.log.debug(reference_url)
        req = requests.get(reference_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token}, verify= False)
        return req
    # Получение списка соц категорий
    def reference_prod_cat(self, guid_token, sog_prog):
        prod_cat_url = self.t2_url +'/reference/productCategories?socialProgramId=' + str(sog_prog)
        self.log.debug(prod_cat_url)
        req = requests.get(prod_cat_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token}, verify= False)
        return req

    def import_product_categories(self, post_data, guid_token):
        import_categories_url = self.t2_url + '/reference/productCategories/import'
        self.log.debug(import_categories_url)
        req = requests.post(import_categories_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token}, data= post_data, verify= False)
        return req

    def import_products(self, post_data, guid_token):
        import_products_url = self.t2_url + '/reference/products/import'
        self.log.debug(import_products_url)
        req = requests.post(import_products_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token}, data= post_data, verify= False)
        return req

    def import_terminals(self, post_data, guid_token):
        import_terminals_url = self.t2_url + '/reference/terminals/import'
        self.log.debug(import_terminals_url)
        req = requests.post(import_terminals_url, headers= {"Content-Type": "application/json", "Authorization": "Guid " + guid_token}, data= post_data, verify= False)
        return req