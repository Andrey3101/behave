import requests
import logging
import urllib3

urllib3.disable_warnings()

class dictionaryApi():
    def __init__(self, url):
        self.dictionary_data_url = url
        self.log = logging.getLogger("dictionary_api")

    def dictionary_cache_update(self):
        # Принудительное обновление всего кеша
        add_cache_update = self.dictionary_data_url + '/cacheupdate'
        self.log.debug(add_cache_update)
        req = requests.get(add_cache_update, headers= {"Content-Type": "application/json"}, verify= False)
        return req

    def put_generate_key(self, post_data):
        # Генерация ключа
        add_put_generate_key_url = self.dictionary_data_url + '/merchant/generateApiKey'
        self.log.debug(add_put_generate_key_url)
        req = requests.put(add_put_generate_key_url, headers= {"Content-Type": "application/json"}, data= post_data, verify= False)
        return req

    def get_merchant_key(self, merchant_id):
        add_merchant_key_url = self.dictionary_data_url + '/merchant/' + str(merchant_id)
        self.log.debug(add_merchant_key_url)
        req = requests.get(add_merchant_key_url, headers= {"Content-Type": "application/json"}, verify= False)
        return req