from multiprocessing import set_forkserver_preload
from unicodedata import name
import requests
import json
import logging
import jwt
import urllib3
from datetime import datetime

urllib3.disable_warnings()

class ManagementApi():
    def __init__(self, url):
        self.m_url = url
        self.log = logging.getLogger("management_api")

    def decode_jwt(self, token):
        data = jwt.decode(token, options={"verify_signature": False})
        return data

    def authorize (self, login, password):
        # Подключение к апи для авторизации
        auth = json.loads('{"login": "", "password": ""}')
        auth['login'] = login
        auth['password'] = password
        m_auth_url = self.m_url+'/auth/login'
        self.log.debug(m_auth_url)
        post_data = json.dumps(auth)
        self.log.debug(post_data)
        req = requests.post(m_auth_url, headers = {"Content-Type": "application/json"}, data=post_data, verify=False)
        return req

    def add_merchant(self, management_token, post_data):
        # Подключение к апи ТСП
        m_add_merchant_url = self.m_url + '/merchant'
        self.log.debug(m_add_merchant_url)
        req = requests.post(m_add_merchant_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def post_merchant(self, management_token, post_data):
        post_merchant_url = self.m_url + '/merchant/search'
        self.log.debug(post_merchant_url)
        req = requests.post(post_merchant_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req
    
    def get_merchant(self, management_token, get_merchant_id):
        get_merchant_url = self.m_url + '/merchant/' + str(get_merchant_id)
        self.log.debug(get_merchant_url)
        req = requests.get(get_merchant_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def put_merchant(self, management_token, post_data):
        put_merchant_url = self.m_url + '/merchant'
        self.log.debug(put_merchant_url)
        req = requests.put(put_merchant_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req
    
    def delete_merchant(self, management_token, del_merchant):
        delete_merchant_url = self.m_url + '/merchant/' + str(del_merchant)
        self.log.debug(delete_merchant_url)
        req = requests.delete(delete_merchant_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def add_shop(self, management_token, post_data):
        # Подключение к апи магазина
        m_add_shop_url = self.m_url + '/shop'
        self.log.debug(m_add_shop_url)
        req = requests.post(m_add_shop_url, headers = {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data = post_data, verify=False)
        return req

    def post_shop(self, management_token, post_data):
        # Подключение к апи магазина для поиска
        post_shop_url = self.m_url + '/shop/search'
        self.log.debug(post_shop_url)
        req = requests.post(post_shop_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def get_shop (self, management_token, get_shop_id):
        #Подключение к апи магазина для поиска тестового магазина
        get_shop_url = self.m_url + '/shop/' + str(get_shop_id)
        self.log.debug(get_shop_url)
        req = requests.get(get_shop_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req
    
    def put_shop (self, management_token, post_data):
        # Подключение к апи магазина для редактирования
        put_shop_url = self.m_url + '/shop'
        self.log.debug(put_shop_url)
        req = requests.put(put_shop_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req
    
    def delete_shop (self, management_token, delete_shop_id):
        # Подключение к апи магазина для удаления
        delete_shop_url = self.m_url + '/shop/' + str (delete_shop_id)
        self.log.debug(delete_shop_url)
        req = requests.delete(delete_shop_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def add_terminal(self, management_token, post_data):
        # Подключение к апи Теминала
       add_terminal_url = self.m_url + '/terminal'
       self.log.debug(add_terminal_url)
       req = requests.post(add_terminal_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
       return req

    def post_terminal(self, management_token, post_data):
        post_terminal_url = self.m_url + '/terminal/search'
        self.log.debug(post_terminal_url)
        req = requests.post(post_terminal_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def get_terminal(self, management_token, terminal_id):
        get_terminal_url = self.m_url + '/terminal/' + str(terminal_id)
        self.log.debug(get_terminal_url)
        req = requests.get(get_terminal_url, headers= {"Content-Typre": "applicaiton/json", "Authorization": "Bearer " + management_token},verify= False)
        return req

    def put_terminal(self, management_token, post_data):
        put_terminal_url = self.m_url + '/terminal'
        self.log.debug(put_terminal_url)
        req = requests.put(put_terminal_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def delete_terminal(self, management_token, delete_terminal_id):
        delete_terminal_url = self.m_url + '/terminal/' + str(delete_terminal_id)
        self.log.debug(delete_terminal_url)
        req = requests.delete(delete_terminal_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req
    
    def add_product_catelog(self, management_token, post_data):
        # подключение к апи для создания каталога товаров
        add_product_catelog_url = self.m_url + '/productcatalog'
        self.log.debug(add_product_catelog_url)
        req = requests.post(add_product_catelog_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def search_product_catalog(self, management_token, post_data):
        post_product_catelog_url = self.m_url + '/productcatalog/search'
        self.log.debug(post_product_catelog_url)
        req = requests.post(post_product_catelog_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def get_product_catalog(self, management_token, get_product_catelog_id):
        get_product_catalog_url = self.m_url + '/productcatalog/' + str(get_product_catelog_id)
        self.log.debug(get_product_catalog_url)
        req = requests.get(get_product_catalog_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def put_product_catalog(self, management_token, post_data):
        put_product_catelog_url = self.m_url + '/productcatalog'
        self.log.debug(put_product_catelog_url)
        req = requests.put(put_product_catelog_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def add_product_catalog_product(self, management_token, post_data):
        add_product_catalog_product_url = self.m_url + '/productcatalog/product'
        self.log.debug(add_product_catalog_product_url)
        req = requests.post(add_product_catalog_product_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def search_product_catalog_product(self, management_token, post_data):
        post_product_catalog_product_url = self.m_url + '/productcatalog/product/search'
        self.log.debug(post_product_catalog_product_url)
        req = requests.post(post_product_catalog_product_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def get_product_catalog_product(self, management_token, product_catalog_id, product_catalog_product_id):
        get_product_catalog_product_url = self.m_url + '/productcatalog/product/' + str(product_catalog_id) + '/' + str(product_catalog_product_id)
        self.log.debug(get_product_catalog_product_url)
        req = requests.get(get_product_catalog_product_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def put_product_catalog_product(self, management_token, post_data):
        put_product_catalog_product_url = self.m_url + '/productcatalog/product'
        self.log.debug(put_product_catalog_product_url)
        req = requests.put(put_product_catalog_product_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def delete_product_catalog_product(self, management_token, post_data):
        delete_product_catalog_product_url = self.m_url + '/productcatalog/product/delete'
        self.log.debug(delete_product_catalog_product_url)
        req = requests.post(delete_product_catalog_product_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def product_status(self, management_token, post_data):
        put_product_status_url = self.m_url + '/productcatalog/product/updateStatus'
        self.log.debug(put_product_status_url)
        req = requests.put(put_product_status_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def product_catalog_matching(self, management_token, post_data, full=False):
        if full == False:
        # Отправка каталога на согласование
            product_catalog_matching_url = self.m_url + '/productcatalog/matching'
        else:
            product_catalog_matching_url = self.m_url + '/productcatalog/fullyMatching'
        self.log.debug(product_catalog_matching_url)
        req = requests.put(product_catalog_matching_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def product_catalog_active(self, management_token, post_data):
        # Активация каталога
        product_catalog_active_url = self.m_url + '/productcatalog/active'
        self.log.debug(product_catalog_active_url)
        req = requests.put(product_catalog_active_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def product_catelog_cancell(self, management_token, post_data):
        # Отменить каталог
        product_catalog_cancell_url = self.m_url + '/productcatalog/cancel'
        self.log.debug(product_catalog_cancell_url)
        req = requests.put(product_catalog_cancell_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req
    
    def add_user(self, management_token, post_data):
        # подключение к апи пользователей, получения списка пользователей
        m_add_user_url = self.m_url + '/user'
        self.log.debug(m_add_user_url)
        post_data = json.dumps(post_data)
        req = requests.post(m_add_user_url, headers = {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data = post_data, verify=False)
        resp = json.loads(req.text.encode('utf-8').decode('utf-8-sig'))
        self.log.debug(resp)
        return req

    def search_users(self, management_token, post_data):
        # Подключение к апи пользователей для поиска всех доступных пользователей
        get_user_url = self.m_url + '/user/search'
        self.log.debug(get_user_url)
        post_data = json.dumps(post_data)
        req = requests.post(get_user_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data = post_data, verify=False)
        resp = json.loads(req.text.encode('utf8').decode('utf-8-sig'))
        self.log.debug(resp)
        return resp

    def update_password_user (self, management_token, post_data):
        # Подключение к апи пользователей для смены пароля
        get_list_user_url = self.m_url + '/user/changePass'
        self.log.debug(get_list_user_url)
        post_data = json.dumps(post_data)
        req = requests.put(get_list_user_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data = post_data, verify=False)
        return req

    
    def add_social_program(self, management_token, post_data):
        # Подключение к апи социальной программы
        get_social_program_url = self.m_url + '/socialprogram'
        self.log.debug(get_social_program_url)
        req = requests.post(get_social_program_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def post_social_program(self, management_token, post_data):
        # Подключение к апи социальной программы для поиска соц  программ
        post_social_program_url = self.m_url + '/socialprogram/search'
        self.log.debug(post_social_program_url)
        req = requests.post(post_social_program_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def get_social_program(self, management_token, get_soc_prog):
        # Подключение к апи социальной программы для получения конктреной соц программы по id
        social_program_url = self.m_url + '/socialprogram/' + str(get_soc_prog)
        self.log.debug(social_program_url)
        req = requests.get(social_program_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def put_social_program(self, management_token, post_data):
        # Подключение к апи социальной программы
        put_social_program_url = self.m_url + '/socialprogram'
        self.log.debug(put_social_program_url)
        req = requests.put(put_social_program_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req
    def delete_social_program(self, management_token, del_soc_prog):
        delete_social_program_url = self.m_url + '/socialprogram/' + str(del_soc_prog)
        self.log.debug(delete_social_program_url)
        req = requests.delete(delete_social_program_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def add_executive_authorities(self, management_token, post_data):
        # Подключение к апи социальных учреждений
        executive_authorities_url = self.m_url + '/executiveauthority'
        self.log.debug(executive_authorities_url)
        req = requests.post(executive_authorities_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data=post_data, verify=False)
        return req

    def get_executive_authorities_entity_list(self, management_token):
        # Подключение к апи соц учреждений для поиска возможных типов соц учреждений
        get_executive_authorities_entitys_url = self.m_url + '/executiveauthority/type'
        self.log.debug(get_executive_authorities_entitys_url)
        req = requests.get(get_executive_authorities_entitys_url, headers= {"Content-Type": "application/json","Authorization": "Bearer " + management_token}, verify= False)
        return req

    def post_executive_authorities_list(self, management_token, post_data):
        # Подключение к апи соц учреждений для поиска всех доступных соц учреждений
        get_list_executive_authorities_url = self.m_url + '/executiveauthority/search'
        self.log.debug(get_list_executive_authorities_url)
        req = requests.post(get_list_executive_authorities_url, headers= {"Content-Type": "application/json","Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def get_exeutive_authorities(self, management_token, executive_authoritie_id):
        # Подключение к апи соц учреждений для поиска соц учреждения по id
        get_exe_url = self.m_url + '/executiveauthority/' + str(executive_authoritie_id)
        self.log.debug(get_exe_url)
        req = requests.get(get_exe_url, headers= {"Content-Type": "application/json" ,"Authorization": "Bearer " + management_token}, verify= False)
        return req
    
    def put_executive_authorities(self, management_token, post_data):
        put_executive_url = self.m_url + '/executiveauthority'
        self.log.debug(put_executive_url)
        req = requests.put(put_executive_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token},data= post_data, verify= False)
        return req

    def delete_executive_authorities(self, management_token, delete_executive_id):
        delete_executive_url = self.m_url + '/executiveauthority/' + str(delete_executive_id)
        self.log.debug(delete_executive_url)
        req = requests.delete(delete_executive_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def add_benefit_types(self, management_token, post_data):
        # Подключение к апи категории льгот
        benefit_types_url = self.m_url + '/benefittype'
        self.log.debug(benefit_types_url)
        req = requests.post(benefit_types_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def post_benefit_types(self, management_token, post_data):
        # Подключение к апи категории льгот для получения всех доступных категорий льгот
        post_benefit_types_url = self.m_url + '/benefittype/search'
        self.log.debug(post_benefit_types_url)
        req = requests.post(post_benefit_types_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req
    
    def get_benefit_type(self, management_token, test_benefit_id):
        # Получение категории льгот по id
        get_benefit_type_url = self.m_url + '/benefittype/' + str(test_benefit_id)
        self.log.debug(get_benefit_type_url)
        req = requests.get(get_benefit_type_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify=False)
        return req

    def put_benefit_type(self, management_token, post_data):
        # Подключение к апи катагории льгот для редактирования
        put_benefit_type_url = self.m_url + '/benefittype'
        self.log.debug(put_benefit_type_url)
        req = requests.put(put_benefit_type_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify=False)
        return req

    def delete_benefit_type(self, management_token, delete_benefit_id):
        # Подключение к апи категории льгот для удаления
        delete_benefit_type_url = self.m_url + '/benefittype/' + str(delete_benefit_id)
        self.log.debug(delete_benefit_type_url)
        req = requests.delete(delete_benefit_type_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify=False)
        return req

    def add_product_category(self, management_token, post_data):
        # Подключение к апи категории продуктов
        add_product_category_url = self.m_url + '/productcategory'
        self.log.debug(add_product_category_url)
        req = requests.post(add_product_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def post_product_category(self, management_token, post_data):
        post_prduct_category_url = self.m_url + '/productcategory/search'
        self.log.debug(post_prduct_category_url)
        req = requests.post(post_prduct_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def get_product_category(self, management_token, get_product_category_id):
        get_product_category_url = self.m_url + '/productcategory/' + str(get_product_category_id)
        self.log.debug(get_product_category_url)
        req = requests.get(get_product_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def put_product_category(self, management_token, post_data):
        put_product_category_url = self.m_url + '/productcategory'
        self.log.debug(put_product_category_url)
        req = requests.put(put_product_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def delete_product_category(self, management_token, delete_product_category_id):
        delete_product_category_url = self.m_url + '/productcategory/' + str(delete_product_category_id)
        self.log.debug(delete_product_category_url)
        req = requests.delete(delete_product_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def post_transaction_batch(self, management_token, post_data):
        transaction_batch_url = self.m_url + '/transactionbatch/search'
        self.log.debug(transaction_batch_url)
        req = requests.post(transaction_batch_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def get_transaction_batch(self, management_token, transaction_batch_id):
        get_transaction_url = self.m_url + '/transactionbatch/' + str(transaction_batch_id)
        self.log.debug(get_transaction_url)
        req = requests.get(get_transaction_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def import_product_catalog(self, management_token, file, socialProgramId, merchantId):
        import_catalog_url = self.m_url + '/Import/productCatalog?socialProgramId=' + str(socialProgramId) + '&merchantId=' + str(merchantId)
        self.log.debug(import_catalog_url)
        name = datetime.now().strftime('%Y%m%dT%H%M%S%f')[:-3]+'.xlsx'
        files = {'file' : (name, file, 'type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        req = requests.post(import_catalog_url, headers= {"Authorization": "Bearer " + management_token}, 
                            files=files, verify= False)
        return req
    
    def import_product_catalog_products(self, management_token, file, productCatalogId):
        import_catalog_url = self.m_url + '/import/productCatalogProducts?productCatalogId=' + str(productCatalogId)
        self.log.debug(import_catalog_url)
        name = datetime.now().strftime('%Y%m%dT%H%M%S%f')[:-3]+'.xlsx'
        files = {'file' : (name, file, 'type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        req = requests.post(import_catalog_url, headers= {"Authorization": "Bearer " + management_token}, 
                            files=files, verify= False)
        return req

    def import_beneficiaries(self, management_token, file, socialProgramId):
        import_ben_url = self.m_url + '/Import/beneficiaries?socialProgramId='+str(socialProgramId)
        self.log.debug(import_ben_url)
        name = datetime.now().strftime('%Y%m%dT%H%M%S%f') +'.xlsx'
        files = {'file': (name, file, 'type=text/csv')}
        req = requests.post(import_ben_url, headers= {"Authorization": "Bearer " + management_token}, files= files, verify= False)
        return req

    def create_beneficiary(self, management_token, post_data):
        # Создание сотрудника предприятия
        create_benefit_url = self.m_url + '/beneficiary'
        self.log.debug(create_benefit_url)
        req = requests.post(create_benefit_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data=post_data, verify= False)
        return req

    def get_beneficiary(self, management_token, benefit_id):
        get_benefit_url = self.m_url + '/beneficiary/' + str(benefit_id)
        self.log.debug(get_benefit_url)
        req = requests.get(get_benefit_url, headers={"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, verify= False)
        return req

    def put_beneficiary(self, management_token, post_data):
        put_benefit_url = self.m_url + '/beneficiary'
        self.log.debug(put_benefit_url)
        req = requests.put(put_benefit_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def post_beneficiary(self, management_token, post_data):
        post_ben_url = self.m_url + '/beneficiary/search'
        self.log.debug(post_ben_url)
        req = requests.post(post_ben_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req


    def import_social(self, management_token, file):
        import_soc_url = self.m_url + '/Import/socialaccounts'
        self.log.debug(import_soc_url)
        name = datetime.now().strftime('%Y%m%dT%H%M%S%f') + '.csv'
        files ={'file': (name, file, 'type=text/csv')}
        req = requests.post(import_soc_url, headers= {"Authorization": "Bearer " + management_token}, files= files, verify= False)
        return req

    def import_log(self, management_token, post_data):
        log_import_url = self.m_url + '/import/log/search'
        self.log.debug(log_import_url)
        req = requests.post(log_import_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= post_data, verify= False)
        return req

    def search_socialaccount(self, management_token, request):
        post_prduct_category_url = self.m_url + '/socialaccount/search'
        self.log.debug(post_prduct_category_url)
        req = requests.post(post_prduct_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= request, verify= False)
        return req

    def create_socialaccount(self, management_token, request):
        post_create_socialaccount_url = self.m_url + '/socialaccount'
        self.log.debug(post_create_socialaccount_url)
        req = requests.post(post_create_socialaccount_url,
                            headers={"Content-Type": "application/json", "Authorization": "Bearer " + management_token},
                            data=request, verify=False)
        return req

    def search_beneficiarys(self, management_token, request):
        post_prduct_category_url = self.m_url + '/beneficiary/search'
        self.log.debug(post_prduct_category_url)
        req = requests.post(post_prduct_category_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= request, verify= False)
        return req

    def cache_update(self):
        get_cache_update_url = self.m_url + '/cacheupdate'
        self.log.debug(get_cache_update_url)
        req = requests.get(get_cache_update_url, verify= False)
        return req
    
    def get_import_log(self, management_token, id):
        get_import_log_url = self.m_url + '/Import/log/'+str(id)
        self.log.debug(get_import_log_url)
        req = requests.get(get_import_log_url, headers= {"Authorization": "Bearer " + management_token}, verify= False)
        return req

    #check for exist
    def get_balance(self, management_token, id):
        get_balance_url = self.m_url + '/socialaccount/' + str(id) + '/balance'
        self.log.debug(get_balance_url)
        req = requests.get(get_balance_url, headers={"Authorization": "Bearer " + management_token}, verify=False)
        return req

    def add_credit(self, management_token, request, id):
        add_credit_url = self.m_url + '/socialaccount/' + str(id) + '/credit'
        self.log.debug(add_credit_url)
        req = requests.post(add_credit_url, headers= {"Content-Type": "application/json", "Authorization": "Bearer " + management_token}, data= request, verify= False)
        return req
