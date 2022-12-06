import logging
import random
import json

import datetime
from behave import fixture
from hashlib import sha1

from API.management import ManagementApi

from gen.gen_credit_card_number import credit_card_number

log = logging.getLogger("fixtures")

def assert_error_message(text, response):
    if response.request.method not in ('GET','DELETE'):
        string = '{4}. http код ответа {0}, {2} запрос {1} с телом запроса {3}'.format(response.status_code, response.request.url, response.request.method, response.request.body, text)
    else:
        string = '{3}. http код ответа {0}, {2} запрос {1}'.format(response.status_code, response.request.url, response.request.method, text)
    return string
    
@fixture
def cache(context, timeout=30, **kwargs):
    context.management_api.cache_update()

@fixture
def dicktion_cache(context, timeout=30, ** kwargs):
    context.dictionary_api.dictionary_cache_update()
# Получение сгенерированного ключа от тестового ТСП
@fixture
def get_merchant_key(context, timeout=30, **kwargs):
    generate_key = None
    get_merch_key_id = context.merch_id
    get_key_merchant = context.dictionary_api.get_merchant_key(get_merch_key_id)
    message = assert_error_message('Не получен код торг.предприятия', get_key_merchant)
    assert get_key_merchant.status_code == 200, message
    get_key_merchant = json.loads(get_key_merchant.text.encode('utf-8').decode('utf-8-sig'))
    generate_key = get_key_merchant['apiKey']
    context.gen_key = generate_key

# Генерация ключа в тестовом ТСП
@fixture
def generate_api_key(context, timeout=30, **kwargs):
    merchant_id = context.merch_id
    user_id = 1
    post_data = json.dumps({"id": merchant_id, "userId": user_id})
    generate_key = context.dictionary_api.put_generate_key(post_data)
    message = assert_error_message('Не сгенерирован ключ торг.предприятия', generate_key)
    assert generate_key.status_code == 200, message 
#    generate_key = json.loads(generate_key.text.encode('utf-8').decode('utf-8-sig'))

@fixture
def auth_tsp (context, timeout=30, **kwargs):
    key_tsp = context.gen_key
    post_data = json.dumps({"apiKey": key_tsp})
    auth = context.terminal_v2_api.auth(post_data)
    message = assert_error_message('Авторизация по токену провалилась', auth)
    assert auth.status_code == 200, message 
    auth = json.loads(auth.text.encode('utf-8').decode('utf-8-sig'))
    context.auth_key = auth['token']

@fixture # Авторизация в management api
def management_super_auth(context, timeout=30, **kwargs):
    login = context.auth_data['super_admin']['login']
    password = context.auth_data['super_admin']['password']
    context.management_super_auth = context.management.authorize(login, password)
    message = assert_error_message('Авторизация супер админа провалилась', context.management_super_auth)
    assert context.management_super_auth.status_code == 200, message
    context.management_super_token = context.management_super_auth.text

@fixture # Авторизация сотрудника тсп, в случае ошибки заведение и повторная авторизация
def management_tsp_auth(context, timeout=30, **kwargs):
    for x in range(2):
        login = context.auth_data['TSP']['login']
        password = context.auth_data['TSP']['password']
        context.tsp_management_auth = context.management.authorize(login, password)
        code = ''.join(random.choice('123456') for i in range(6))
        if context.tsp_management_auth == 200: 
            jwt_decode = context.management.decode_jwt(context.tsp_management_auth.text)
            assert jwt_decode['role_id'] == '4'  # сделать проверку адекватную
            log.info(jwt_decode)
            context.tsp_management_token = context.tsp_management_auth.text
            break # тут заведение тсп манагера, после цикл вернётся к авторизации. While использовать не стоит (генерацию тсп менеджеров можно породить)
        elif context.tsp_management_auth != 200:
            search_data = {}
            search_data['login'] = context.auth_data['TSP']['login']
            users = context.management.search_users(context.management_super_token, search_data)
            list_users = users['data']
            for user in list_users:
                if user['login'] == context.auth_data['TSP']['login']:
                    new_pass = {}
                    new_pass['id'] = user['id']
                    new_pass['password'] = context.auth_data['TSP']['password']
                    update_password = context.management.update_password_user(context.management_super_token, new_pass)
                    message = assert_error_message('Обновление пароля пользователя провалилось', update_password)
                    assert update_password.status_code == 200, message 
                else:
                    log.info('Проблема с пользователем ТСП, завести или обновить пароль существующему не удалось. Необходимо проверить данные в Б: список пользователей и учетные данные')
            tsp_management = {}
            tsp_management['changeUserId'] = 1
            tsp_management['createUserId'] = 1
            tsp_management['login'] = str('testTSP' + code)
            tsp_management['password'] = context.auth_data['TSP']['password']
            tsp_management['name'] = 'Иванов'
            tsp_management['last name'] = 'Иван'
            tsp_management['middleName'] = 'Иванович'
            tsp_management['email'] = str(code +'test@sobaka.ru')
            tsp_management['roleId'] = 4
            tsp_management['merchantId'] = 1
            tsp_management['executiveAuthorityId'] = 1
            tsp_management['regionIds'] = context.auth_data['TSP']['regionIds']
            tsp_management['productMatchingNotification'] = True
            log.info(tsp_management)
            tsp_list = context.management.add_user(context.management_super_token, tsp_management)
            return tsp_list
            # return tsp_management тут должно быть заведение пользователя, после повторная авторизация в начале цикла

@fixture # Авторизация за сотрудника ОИВ
def management_oiv_auth(context, timeout=30, **kwargs):
    for i in range(2):
        login = context.auth_data['OIV']['login']
        password = context.auth_data['OIV']['password']
        context.oiv_management_auth = context.management.authorize(login, password)
        code = ''.join(random.choice('1234567890') for i in range(6))
        if context.oiv_management_auth == 200:
            jwt_decode = context.management.jwt_decode(context.oiv_management_auth.text)
            assert jwt_decode['roleId'] == '4', 'Сотрудник не верная роль c id {0}, ожидалась c id 4'.format(jwt_decode['roleId'])
            log.info(jwt_decode)
            context.oiv_management_token = context.oiv_management_auth.text
            break
        elif context.oiv_management_auth != 200:
            search_data = {}
            search_data['login'] = context.auth_data['OIV']['login']
            users = context.management.search_users(context.management_super_token, search_data)
            list_users = users['data']
            for user_oiv in list_users:
                if user_oiv['login'] == context.auth_data['OIV']['login']:
                    new_pass = {}
                    new_pass['id'] = user_oiv['id']
                    new_pass['password'] = context.auth_data['OIV']['password']
                    update_password = context.management.update_password_user(context.management_super_token, new_pass)
                    message = assert_error_message('Обновление пароля пользователя провалилось', update_password)
                    assert update_password.status_code == 200, message
                else:
                    log.info("Упс, непредвиденная ошибка")
            management_oiv = {}
            management_oiv['changeUserId'] = 1
            management_oiv['createUserId'] = 1
            management_oiv['login'] = str('testIOV' + code)
            management_oiv['password'] = context.auth_data['OIV']['password']
            management_oiv['name'] = 'Тестовый'
            management_oiv['last name'] = 'ОИВ'
            management_oiv['middleName'] = 'string'
            management_oiv['email'] = str(code +'test@pes.ru')
            management_oiv['roleId'] = 3
            management_oiv['merchantId'] = 1
            management_oiv['executiveAuthorityId'] = 1
            management_oiv['regionIds'] = context.auth_data['OIV']['regionIds']
            management_oiv['productMatchingNotification'] = True
            log.info(management_oiv)
            list_oiv = context.management.add_user(context.management_super_token, management_oiv)
            return list_oiv

@fixture
def ensure_beneficiary(context, timeout=30, **kwargs):
    beneficiary_id = None
    benefic_name = 'Тестовый сотрудник '
    last_name = 'Test'
    code = ''.join(random.choice('1234567890') for i in range (6))
    benefic_type = 2
    sc_prg = context.soc_program
    exe_id = context.executive_id
    bnft_id = context.benefit_id
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000, "executiveAuthorityIds": [exe_id], "socialProgramIds": [sc_prg], "typeIds": [benefic_type]})
    benefic_search = context.management_api.post_beneficiary(context.management_super_token, post_data)
    message_er = assert_error_message('Список сотрудников не получен', benefic_search)
    assert benefic_search.status_code == 200, message_er
    benefic_search = json.loads(benefic_search.text.encode('utf-8').decode('utf-8-sig'))
    for ben_search in benefic_search['data']:
        if ben_search['personalNumber'] == code:
            beneficiary_id = ben_search['id']
            context.beneficiar_id = beneficiary_id
    if beneficiary_id == None:
        post_data = json.dumps({"typeId": benefic_type, "firstName": benefic_name, "lastName": last_name, "benefitTypeIds": [bnft_id], "divisionCode": code, "executiveAuthorityIds": [exe_id], "personalNumber": code, "socialProgramIds": [sc_prg], "enabled": True})
        beneficar_add = context.management_api.create_beneficiary(context.management_super_token, post_data)
        message_error = assert_error_message('Сотрудник не добавлен', beneficar_add)
        assert beneficar_add.status_code == 200, message_error
        beneficar_add = json.loads(beneficar_add.text.encode('utf-8').decode('utf-8-sig'))
        context.beneficiar_id = beneficar_add['id']

@fixture
def ensure_beneficiary_edit(context, timeout=30, **kwargs):
    ben_id_edit = None
    ben_f_name = 'Test'
    ben_l_name = 'Test'
    code = ''.join(random.choice('1234567890') for i in range (6))
    ben_t = 2
    ben_soc_prg = context.soc_program
    ben_execut = context.executive_id
    ben_bnft = context.benefit_id
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000, "executiveAuthorityIds": [ben_execut], "socialProgramIds": [ben_soc_prg], "typeIds": [ben_t]})
    ben_search_edit = context.management_api.post_beneficiary(context.management_super_token, post_data)
    message = assert_error_message('Список сотрудников не получен', ben_search_edit)
    assert ben_search_edit.status_code == 200, message
    ben_search_edit = json.loads(ben_search_edit.text.encode('utf-8').decode('utf-8-sig'))
    for ben_edit in ben_search_edit['data']:
        if ben_edit['personalNumber'] == code:
            ben_id_edit = ben_edit['id']
            context.beneficiar_id = ben_id_edit
    if ben_id_edit == None:
        post_data = json.dumps({"typeId": ben_t, "firstName": ben_f_name, "lastName": ben_l_name, "benefitTypeIds": [ben_bnft], "divisionCode": code, "executiveAuthorityIds": [ben_execut], "personalNumber": code, "socialProgramIds": [ben_soc_prg], "enabled": True})
        ben_add_edit = context.management_api.create_beneficiary(context.management_super_token, post_data)
        message_er = assert_error_message('Сотрудник не добавлен', ben_add_edit)
        assert ben_add_edit.status_code == 200, message_er
        ben_add_edit = json.loads(ben_add_edit.text.encode('utf-8').decode('utf-8-sig'))
        context.beneficiar_id = ben_add_edit['id']

@fixture # Проверка тестового социального учреждения в случае отсутствия его создания
def ensure_executive_authoritie(context, type_pseudocoail = False, timeout=30, **kwargs):
    executive_authoritie_id = None
    executive_authoritie_name = 'Тестовое социальное учреждение Behave'
    executive_authoritie_type = context.config.userdata['test_all_data']['typeId']
    executive_authoritie_region = context.config.userdata['test_all_data']['regionId']
    post_data = json.dumps({"name": executive_authoritie_name, "typeIds": [executive_authoritie_type], "regionIds": [executive_authoritie_region], "page": 1, "pageSize": 1000, "column": None, "direction": None})
    executive_authoritie_list = context.management_api.post_executive_authorities_list(context.management_super_token, post_data)
    message = assert_error_message('Список соц.учреждений не получен', executive_authoritie_list)
    assert executive_authoritie_list.status_code == 200, message
    executive_authoritie_list = json.loads(executive_authoritie_list.text.encode('utf-8').decode('utf-8-sig'))
    for executive_authoritie in executive_authoritie_list['data']:
        if executive_authoritie['regionId'] == executive_authoritie_region and executive_authoritie_name in executive_authoritie['name']:
            executive_authoritie_id = executive_authoritie['id']
            context.executive_id = executive_authoritie_id
            break
    if executive_authoritie_id == None:
        if type_pseudocoail == False:
            executive_authoritie_new = json.dumps({"name": executive_authoritie_name, "typeId": executive_authoritie_type, "regionId": executive_authoritie_region, "projectTypeId": 1})
            executive_authoritie = context.management_api.add_executive_authorities(context.management_super_token, executive_authoritie_new)
            message = assert_error_message('Добавление соц.учреждения провалилось', executive_authoritie)
            assert executive_authoritie.status_code == 200, message
            executive_authoritie = json.loads(executive_authoritie.text.encode('utf-8').decode('utf-8-sig'))
            context.executive_id = executive_authoritie['id']
        if type_pseudocoail == True:
            executive_authoritie_new = json.dumps({"name": executive_authoritie_name, "typeId": executive_authoritie_type, "regionId": executive_authoritie_region, "projectTypeId": 1})
            executive_authoritie = context.management_api.add_executive_authorities(context.management_super_token, executive_authoritie_new)
            message = assert_error_message('Добавление соц.учреждения провалилось', executive_authoritie)
            assert executive_authoritie.status_code == 200, message
            executive_authoritie = json.loads(executive_authoritie.text.encode('utf-8').decode('utf-8-sig'))
            context.executive_id = executive_authoritie['id']


@fixture # Тестовое социальное учреждение для редактирования и удаления
def ensure_executive_authoritie_edit(context, type_pseudocoail = False, timeout=30, **kwargs):
    exe_id = None
    executive_code = ''.join(random.choice('1234567890') for i in range(8))
    executive_name = 'Тестовое соц учреждение Behave' + str(executive_code)
    executive_type = context.config.userdata['test_all_data']['typeId']
    executive_project_type = 1 #социальный
    executive_region = context.config.userdata['test_all_data']['regionId']
    post_data = json.dumps({"name": executive_name, "typeIds": [executive_type], "regionIds": [executive_region]})
    ex_list = context.management_api.post_executive_authorities_list(context.management_super_token, post_data)
    message = assert_error_message('Список соц.учреждений не получен', ex_list)
    assert ex_list.status_code == 200, message
    ex_list = json.loads(ex_list.text.encode('utf-8').decode('utf-8-sig'))
    for authritie in ex_list['data']:
        if authritie['regionId'] == executive_region and authritie['name'] == executive_name:
            exe_id = authritie['id']
            context.executive_id = exe_id
    if exe_id == None:
        if type_pseudocoail == False:
            post_data = json.dumps({"name": executive_name, "typeId": executive_type, "projectTypeId": executive_project_type, "regionId": executive_region, "projectTypeId": 1})
            exe_add = context.management_api.add_executive_authorities(context.management_super_token, post_data)
            message = assert_error_message('Добавление соц.учреждения провалилось', exe_add)
            assert exe_add.status_code == 200, message
            exe_add = json.loads(exe_add.text.encode('utf-8').decode('utf-8-sig'))
            context.executive_id = exe_add['id']
        if type_pseudocoail == True:
            post_data = json.dumps({"name": executive_name, "typeId": executive_type, "projectTypeId": executive_project_type, "regionId": executive_region, "projectTypeId": 2})
            execut = context.management_api.add_executive_authorities(context.management_super_token, post_data)
            message = assert_error_message('Добавление соц.учреждения провалилось', execut)
            assert execut.status_code == 200, message
            execut = json.loads(execut.text.encode('utf-8').decode('utf-8-sig'))
            context.executive_id = execut['id']

@fixture # Проверка возможности создания категории льгот
def ensure_benefit_types (context, timeout=30, **kwargs):
    benefit_type_id = None
    benefit_type_name = 'Тестовая категория льгот Behave'
    benefit_type_region = context.config.userdata['test_all_data']['regionId']
    benefit_type_code = ''.join(random.choice('1234567890') for i in range(6))
    post_data = json.dumps({"name": benefit_type_name, "regionIds": [benefit_type_region], "page": 1, "pageSize": 1000,"column":"ChangeDate","direction":2})
    benefit_type_list = context.management_api.post_benefit_types(context.management_super_token, post_data)
    message = assert_error_message('Список категорий льгот не получен', benefit_type_list)
    assert benefit_type_list.status_code == 200, message
    benefit_type_list = json.loads(benefit_type_list.text.encode('utf-8').decode('utf-8-sig'))
    for benefit_type in benefit_type_list['data']:
        if benefit_type_name in benefit_type['name'] and benefit_type['regionId'] == benefit_type_region:
            benefit_type_id = benefit_type['id']
            context.benefit_id = benefit_type_id
            break
    if benefit_type_id == None:
        post_data = json.dumps({"name": benefit_type_name, "description": benefit_type_code, "code": benefit_type_code, "regionId": benefit_type_region})
        benefit_type_add = context.management_api.add_benefit_types(context.management_super_token, post_data)
        message = assert_error_message('Категория льготы не добавлена', benefit_type_add)
        assert benefit_type_add.status_code == 200, message
        benefit_type_add = json.loads(benefit_type_add.text.encode('utf-8').decode('utf-8-sig'))
        benefit_type_id = benefit_type_add['id']
        benefit_t_code = benefit_type_add['code']
        context.benefit_type_code = benefit_t_code
        context.benefit_id = benefit_type_id

@fixture
def ensure_benefit_edit(context,timeout=30, **kwargs):
    benefit_ed_id = None
    benefit_ed_code = ''.join(random.choice('1234567890') for i in range(6))
    benefit_ed_name = 'Тестовая категория льгот' + str(benefit_ed_code)
    benefit_ed_region = context.config.userdata['test_all_data']['regionId']
    post_data = json.dumps({"name": benefit_ed_name, "regionIds": [benefit_ed_region], "page": 1, "pageSize": 1000, "column": "ChangeDate", "direction":2})
    benefit_list = context.management_api.post_benefit_types(context.management_super_token, post_data)
    message = assert_error_message('Список категорий льгот не получен', benefit_list)
    assert benefit_list.status_code == 200, message
    benefit_list = json.loads(benefit_list.text.encode('utf-8').decode('utf-8-sig'))
    for benefit in benefit_list['data']:
        if benefit['name'] == benefit_ed_name and benefit['regionId'] == benefit_ed_region:
            benefit_ed_id = benefit['id']
            context.benefit_id = benefit_ed_id
    if benefit_ed_id == None:
        post_data = json.dumps({"name": benefit_ed_name, "description": benefit_ed_code, "code": benefit_ed_code, "regionId": benefit_ed_region})
        ben_add = context.management_api.add_benefit_types(context.management_super_token, post_data)
        message = assert_error_message('Категория льготы не добавлена', ben_add)
        assert ben_add.status_code == 200, message
        ben_add = json.loads(ben_add.text.encode('utf-8').decode('utf-8-sig'))
        benefit_ed_id = ben_add['id']
        benefit_ed_code = ben_add['code']
        context.benefit_type_code = benefit_ed_code
        context.benefit_id = benefit_ed_id


@fixture # Проверка возможности создания социальной программы
def ensure_social_program (context, social_account_nko = True, timeout=30, **kwargs):
    social_program_id = None
    social_program_name = 'Тестовая социальная программа Behave'
    social_program_region = context.config.userdata['test_all_data']['regionId']
    social_check = context.config.userdata['test_all_data']['check_all']
    date_from = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")
    code = ''.join(random.choice('1234567890') for i in range(5))
    post_data = json.dumps({"column":"ChangeDate","direction":2, "name": social_program_name, "executiveAuthorityIds":[context.executive_id],"benefitTypeIds":[context.benefit_id],"regionIds":[social_program_region], "page": 1, "pageSize": 1000})
    social_program_list = context.management_api.post_social_program(context.management_super_token, post_data)
    message = assert_error_message('Список соц.программ не получены', social_program_list) 
    assert social_program_list.status_code == 200, message
    social_program_list = json.loads(social_program_list.text.encode('utf-8').decode('utf-8-sig'))
    for social_program in social_program_list['data']:
        if social_program_name in social_program['name'] and social_program['typeId'] == 1 and social_program['regionId'] == social_program_region and context.executive_id == social_program['executiveAuthorityId'] and context.benefit_id in social_program['benefitTypeIds']:
            social_program_id = social_program['id']
            context.soc_program = social_program_id
            context.social_program_code = social_program['code']
            break
    if social_program_id == None:
        if social_account_nko == True:
            social_programs_name = 'Тестовая социальная программа Behave'
            post_data = json.dumps({"name": social_programs_name,"dateFrom": date_from ,"dateTo": None ,"description": code, "typeId": 1, "executiveAuthorityId": context.executive_id, "regionId": social_program_region, "benefitTypeIds": [context.benefit_id], "balanceBurn": social_check, "checkBenefitDates": social_check, "checkProductCatalogPrice": social_check, "checkProductPrice": social_check, "checkProductQuantity": social_check, "checkReserveAndTransferAmount": social_check, "projectTypeId": 0, "socialAccountTypeId": 1})
            social_program_add = context.management_api.add_social_program(context.management_super_token, post_data)
            message = assert_error_message('Добавление соц.программы провалено', social_program_add)
            assert social_program_add.status_code == 200, message
            social_program_add = json.loads(social_program_add.text.encode('utf-8').decode('utf-8-sig'))
            social_program_add = context.management_api.get_social_program(context.management_super_token, social_program_add['id'])
            social_program_add = json.loads(social_program_add.text.encode('utf-8').decode('utf-8-sig'))
            social_program_id = social_program_add['id']
            soc_program_code = social_program_add['code']
            context.soc_program = social_program_id
            context.social_program_code = soc_program_code
        if social_account_nko == False:
            social_programs_name = 'Тестовая социальная программа Behave'
            post_data = json.dumps({"name": social_programs_name,"dateFrom": date_from ,"dateTo": None ,"description": code, "typeId": 1, "executiveAuthorityId": context.executive_id, "regionId": social_program_region, "benefitTypeIds": [context.benefit_id], "balanceBurn": social_check, "checkBenefitDates": social_check, "checkProductCatalogPrice": social_check, "checkProductPrice": social_check, "checkProductQuantity": social_check, "checkReserveAndTransferAmount": social_check, "projectTypeId": 0, "socialAccountTypeId": 2})
            social_program_add = context.management_api.add_social_program(context.management_super_token, post_data)
            message = assert_error_message('Добавление соц.программы провалено', social_program_add)
            assert social_program_add.status_code == 200, message
            social_program_add = json.loads(social_program_add.text.encode('utf-8').decode('utf-8-sig'))
            social_program_add = context.management_api.get_social_program(context.management_super_token, social_program_add['id'])
            social_program_id = social_program_add['id']
            soc_program_code = social_program_add['code']
            context.soc_program = social_program_id
            context.social_program_code = soc_program_code


@fixture
def ensure_social_program_edit(context, social_account_nko = True, timeout=30, **kwargs):
    soc_edit_id = None
    code = ''.join(random.choice('1234567890') for i in range(5))
    soc_edit_name = 'Тестовая социальная программа Behave' + str(code)
    soc_edit_type = 1
    soc_edit_region = context.config.userdata['test_all_data']['regionId']
    soc_edit_check = context.config.userdata['test_all_data']['check_all']
    date_from = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")
    post_data = json.dumps({"column": "ChangeDate", "direction": 2, "executiveAuthorityIds":[context.executive_id], "regionId": soc_edit_region, "benefitTypeIds": [context.benefit_id], "page": 1, "pageSize": 1000})
    soc_edit_list = context.management_api.post_social_program(context.management_super_token, post_data)
    message = assert_error_message('Список соц.программ не получены', soc_edit_list) 
    assert soc_edit_list.status_code == 200, message
    soc_edit_list = json.loads(soc_edit_list.text.encode('utf-8').decode('utf-8-sig'))
    for social in soc_edit_list['data']:
        if social['name'] == soc_edit_name and social['typeId'] == soc_edit_type and social['regionId'] == soc_edit_region:
            soc_edit_id = social['id']
            context.soc_program = soc_edit_id
            context.social_program_code = social['code']
    if soc_edit_id == None:
        if social_account_nko == True:
            post_data = json.dumps({"name": soc_edit_name, "dateFrom": date_from, "dateTo": None, "direction": code, "typeId": soc_edit_type, "executiveAuthorityId": context.executive_id, "regionId": soc_edit_region, "benefitTypeIds": [context.benefit_id], "balanceBurn": soc_edit_check, "checkBenefitDates": soc_edit_check, "checkProductCatalogPrice": soc_edit_check, "checkProductPrice": soc_edit_check, "checkProductQuantity": soc_edit_check, "checkReserveAndTransferAmount": soc_edit_check, "projectTypeId": 0, "socialAccountTypeId": 1})
            soc_cr_add = context.management_api.add_social_program(context.management_super_token, post_data)
            message = assert_error_message('Добавление соц.программы провалено', soc_cr_add)
            assert soc_cr_add.status_code == 200, message
            soc_cr_add = json.loads(soc_cr_add.text.encode('utf-8').decode('utf-8-sig'))
            soc_cr_add = context.management_api.get_social_program(context.management_super_token, soc_cr_add['id'])
            soc_cr_add = json.loads(soc_cr_add.text.encode('utf-8').decode('utf-8-sig'))
            soc_edit_id = soc_cr_add['id']
            context.soc_program = soc_edit_id
            context.social_program_code = soc_cr_add['code']
        if social_account_nko == False:
            post_data = json.dumps({"name": soc_edit_name, "dateFrom": date_from, "dateTo": None, "direction": code, "typeId": soc_edit_type, "executiveAuthorityId": context.executive_id, "regionId": soc_edit_region, "benefitTypeIds": [context.benefit_id], "balanceBurn": soc_edit_check, "checkBenefitDates": soc_edit_check, "checkProductCatalogPrice": soc_edit_check, "checkProductPrice": soc_edit_check, "checkProductQuantity": soc_edit_check, "checkReserveAndTransferAmount": soc_edit_check, "projectTypeId": 0, "socialAccountTypeId": 2})
            soc_cr_add = context.management_api.add_social_program(context.management_super_token, post_data)
            message = assert_error_message('Добавление соц.программы провалено', soc_cr_add)
            assert soc_cr_add.status_code == 200, message
            soc_cr_add = json.loads(soc_cr_add.text.encode('utf-8').decode('utf-8-sig'))
            soc_cr_add = context.management_api.get_social_program(context.management_super_token, soc_cr_add['id'])
            soc_cr_add = json.loads(soc_cr_add.text.encode('utf-8').decode('utf-8-sig'))
            soc_edit_id = soc_cr_add['id']
            context.soc_program = soc_edit_id
            context.social_program_code = soc_cr_add['code']


@fixture # Проверка возможности создания Торгового предприятия
def ensure_merchant (context, timeout=30, **kwargs):
    merchant_id = None
    code = ''.join(random.choice('1234567890') for i in range(6))
    add_merchant_name = 'Тестовое торговое предприятие Behave'
    add_merchant_region = context.config.userdata['test_all_data']['regionId']
    add_merchant_type = context.config.userdata['test_all_data']['typeId']
    post_data = json.dumps({"socialProgramIds":[context.soc_program],"page":1,"pageSize":1000,"column":"ChangeDate","direction":2,"enabled":True})
    add_merchant_list = context.management_api.post_merchant(context.management_super_token, post_data)
    message = assert_error_message('Список торговых предприятий не получен', add_merchant_list)
    assert add_merchant_list.status_code == 200, message
    add_merchant_list = json.loads(add_merchant_list.text.encode('utf-8').decode('utf-8-sig'))
    for add_merchant in add_merchant_list['data']:
        if add_merchant['name'] == add_merchant_name and add_merchant['regionId'] == add_merchant_region and add_merchant['typeId'] == add_merchant_type and context.soc_program in add_merchant['socialProgramIds']:
            merchant_id = add_merchant['id']
            context.merch_id = merchant_id
            context.merch_code = add_merchant['code']
            break
    if merchant_id == None:
        add_merchant_legal_name = 'Тестовое торговое предприятие Behave'
        add_merchant_inn = ''.join(random.choice('1234567890') for i in range(12))
        add_merchant_legal_address = 'Test address' + str(code)
        add_merchant_phone = ''.join(random.choice('1234567890') for i in range(10))
        add_merchant_soc_prog = context.soc_program
        merchant_productCatalogAutoLoad = context.config.userdata['test_all_data']['productCatalogAutoLoad']
        merchant_productCatalogAutoApprove = context.config.userdata['test_all_data']['productCatalogAutoApprove']
        post_data = json.dumps({"typeId": add_merchant_type, "parentId": None, "name": add_merchant_name, "code": code, "comment": None, "legalName": add_merchant_legal_name, "inn": add_merchant_inn, "legalAddress": add_merchant_legal_address, "phone": '+7' + str(add_merchant_phone), "regionId": add_merchant_region, "socialProgramIds": [add_merchant_soc_prog], "productCatalogAutoLoad": merchant_productCatalogAutoLoad, "productCatalogAutoApprove": merchant_productCatalogAutoApprove})
        add_merchant_create = context.management_api.add_merchant(context.management_super_token, post_data)
        message = assert_error_message('Торговое предприятие не создано', add_merchant_create)
        assert add_merchant_create.status_code == 200, message
        add_merchant_create = json.loads(add_merchant_create.text.encode('utf-8').decode('utf-8-sig'))
        merchant_id = add_merchant_create['id']
        context.merch_id = merchant_id
        context.merch_code = add_merchant_create['code']

@fixture
def ensure_merchant_edit(context, timeout=30, **kwargs):
    merchant_id = None
    merchant_edit_code = ''.join(random.choice('1234567890') for i in range(6))
    merchant_edit_name = 'Тестовое торговое предприятие Behave' + str(merchant_edit_code)
    merchant_edit_inn = ''.join(random.choice('1234567890') for i in range(12))
    merchant_edit_phone = ''.join(random.choice('1234567890') for i in range(10))
    merchant_edit_soc = context.soc_program
    merchant_edit_region = context.config.userdata['test_all_data']['regionId']
    merchant_edit_type = context.config.userdata['test_all_data']['typeId']
    post_data = json.dumps({"socialProgramIds": [merchant_edit_soc], "page": 1, "pageSize":1000,"column":"ChangeDate","direction":2,"enabled":True})
    merchant_list = context.management_api.post_merchant(context.management_super_token, post_data)
    message = assert_error_message('Список торговых предприятий не получен', merchant_list)
    assert merchant_list.status_code == 200, message
    merchant_list = json.loads(merchant_list.text.encode('utf-8').decode('utf-8-sig'))
    for merchant in merchant_list['data']:
        if merchant['name'] == merchant_edit_name and merchant['regionId'] == merchant_edit_region:
            merchant_id = merchant['id']
            context.merch_id = merchant_id
            context.merch_code = merchant['code']
    if merchant_id == None:
        post_data = json.dumps({"typeId": merchant_edit_type, "parentId": None, "name": merchant_edit_name, "code": merchant_edit_code, "comment": None, "legalName": "Тестовое имя", "inn": merchant_edit_inn, "legalAddress": "Тестовый адрес", "phone": "+7" + str(merchant_edit_phone), "regionId": merchant_edit_region, "socialProgramIds": [merchant_edit_soc], "productCatalogAutoLoad": True, "productCatalogAutoApprove": True})
        merch_list = context.management_api.add_merchant(context.management_super_token, post_data)
        message = assert_error_message('Торговое предприятие не создано', merch_list)
        assert merch_list.status_code == 200, message
        merch_list = json.loads(merch_list.text.encode('utf-8').decode('utf-8-sig'))
        merchant_id = merch_list['id']
        context.merch_id = merchant_id
        context.merch_code = merch_list['code']

@fixture # Проверка магазина если магазин отсутствует то его создание
def ensure_shop(context, timeout=30, **kwargs):
    add_shop_id = None
    code = ''.join(random.choice('1234567890') for i in range(8))
    add_shop_name = 'Тестовый магазин Behave'
    add_shop_address = 'Test address'
    add_shop_phone = ''.join(random.choice('1234567890') for i in range(10))
    add_shop_merchant = context.merch_id
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000, "merchantIds": [add_shop_merchant]})
    add_shop_list = context.management_api.post_shop(context.management_super_token, post_data)
    message = assert_error_message('Список магазинов торгового предприятия не получен', add_shop_list)
    assert add_shop_list.status_code == 200, message
    add_shop_list = json.loads(add_shop_list.text.encode('utf-8').decode('utf-8-sig'))
    for add_shop in add_shop_list['data']:
        if add_shop['merchantId'] == add_shop_merchant and add_shop['name'] == add_shop_name:
            add_shop_id = add_shop['id']
            context.shop_id = add_shop_id
            context.sh_code = add_shop['code']
            break
    if add_shop_id == None:
        post_data = json.dumps({"name": add_shop_name, "code": str(code), "address": add_shop_address, "phone": "+7" + str(add_shop_phone), "merchantId": add_shop_merchant, "typeId" : 1, "login":"","password":""})
        add_shop_create = context.management_api.add_shop(context.management_super_token, post_data)
        message = assert_error_message('Магазин торговому предприятию не добавлен', add_shop_create)
        assert add_shop_create.status_code == 200, message
        add_shop_create = json.loads(add_shop_create.text.encode('utf-8').decode('utf-8-sig'))
        add_shop_id = add_shop_create['id']
        context.shop_id = add_shop_id
        context.sh_code = add_shop_create['code']

@fixture
def ensure_shop_edit(context, timeout=30, **kwargs):
    shop_id = None
    shop_edit_code = ''.join(random.choice('1234567890') for i in range(8))
    shop_edit_name = 'Тестовая касса Behave' + str(shop_edit_code)
    shop_edit_phone = ''.join(random.choice('1234567890') for i in range(10))
    shop_edit_merch = context.merch_id
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000, "merchantIds": [shop_edit_merch]})
    shop_list = context.management_api.post_shop(context.management_super_token, post_data)
    message = assert_error_message('Список магазинов торгового предприятия не получен', shop_list)
    assert shop_list.status_code == 200, message
    shop_list = json.loads(shop_list.text.encode('utf-8').decode('utf-8-sig'))
    for shop in shop_list['data']:
        if shop['name'] == shop_edit_name and shop['merchantId'] == shop_edit_merch:
            shop_id = shop['id']
            context.shop_id = shop_id
            context.sh_code = shop['code']
    if shop_id == None:
        post_data = json.dumps({"name": shop_edit_name, "code": str(shop_edit_code), "address": "Тестовый адрес", "phone": "+7" + str(shop_edit_phone), "merchantId": shop_edit_merch, "typeId" : 1, "login":"","password":""})
        sh_list = context.management_api.add_shop(context.management_super_token, post_data)
        message = assert_error_message('Магазин торговому предприятию не добавлен', sh_list)
        assert sh_list.status_code == 200, message
        sh_list = json.loads(sh_list.text.encode('utf-8').decode('utf-8-sig'))
        shop_id = sh_list['id']
        context.shop_id = shop_id
        context.sh_code = sh_list['code']


@fixture # Проверка тестовой кассы (терминала) если её нет то создание
def ensure_terminal(context, timeout=30, **kwargs):
    add_terminal_id = None
    add_terminal_code = ''.join(random.choice('1234567890') for i in range(10))
    add_terminal_merchant = context.merch_id
    add_terminal_shop = context.shop_id
    post_data = json.dumps({"merchantIds":[add_terminal_merchant],"shopIds":[add_terminal_shop], "column": None, "direction": None, "page": 1, "pageSize": 1000})
    add_terminal_list = context.management_api.post_terminal(context.management_super_token, post_data)
    message = assert_error_message('Список касс магазина торгового предприятия не получен', add_terminal_list)
    assert add_terminal_list.status_code == 200, message
    add_terminal_list = json.loads(add_terminal_list.text.encode('utf-8').decode('utf-8-sig'))
    for add_terminal in add_terminal_list['data']:
        if add_terminal['merchantId'] == add_terminal_merchant and add_terminal['shopId'] == add_terminal_shop:
            add_terminal_id = add_terminal['id']
            context.terminal_id = add_terminal_id
            context.term_code = add_terminal['number']
            break
    if add_terminal_id == None:
        post_data = json.dumps({"number": add_terminal_code, "merchantId": add_terminal_merchant, "shopId": add_terminal_shop})
        add_terminal = context.management_api.add_terminal(context.management_super_token, post_data)
        message = assert_error_message('Касса магазину не добавлена', add_terminal)
        assert add_terminal.status_code == 200, message
        add_terminal = json.loads(add_terminal.text.encode('utf-8').decode('utf-8-sig'))
        add_terminal_id = add_terminal['id']
        context.terminal_id = add_terminal['id']
        context.term_code = add_terminal['number']

@fixture
def ensure_terminal_edit(context, timeout=30, **kwargs):
    terminal_edit_id = None
    terminal_edit_code = ''.join(random.choice('1234567890') for i in range(10))
    terminal_edit_merchant = context.merch_id
    terminal_edit_shop = context.shop_id
    post_data = json.dumps({"merchantIds": [terminal_edit_merchant], "shopIds": [terminal_edit_shop], "column": None, "direction": None, "page": 1, "pageSize": 1000})
    terminal_list = context.management_api.post_terminal(context.management_super_token, post_data)
    message = assert_error_message('Список касс магазина торгового предприятия не получен', terminal_list)
    assert terminal_list.status_code == 200, message
    terminal_list = json.loads(terminal_list.text.encode('utf-8').decode('utf-8-sig'))
    for terminal in terminal_list['data']:
        if terminal['merchantId'] == terminal_edit_merchant and terminal['shopId'] == terminal_edit_shop:
            terminal_edit_id = terminal['id']
            context.terminal_id = terminal_edit_id
            context.term_code = terminal['number']
    if terminal_edit_id == None:
        post_data = json.dumps({"number": terminal_edit_code, "merchantId": terminal_edit_merchant, "shopId": terminal_edit_shop})
        term_list = context.management_api.add_terminal(context.management_super_token, post_data)
        message = assert_error_message('Касса магазину не добавлена', term_list)
        assert term_list.status_code == 200, message
        term_list = json.loads(term_list.text.encode('utf-8').decode('utf-8-sig'))
        terminal_edit_id = term_list['id']
        context.terminal_id = terminal_edit_id
        context.term_code = term_list['number']

@fixture # Проверка тестовой категории продуктов если её нет то создание
def ensure_product_category(context, timeout=30, **kwargs):
    product_categories_id = None
    product_category_name = 'Тестовая категория продуктов Behave'
    product_category_merchant = context.merch_id
    code = ''.join(random.choice('1234567890') for i in range(8))
    post_data = json.dumps({"merchantIds":[product_category_merchant],"page":1,"pageSize":1000,"column":"ChangeDate","direction":2})
    product_category_list = context.management_api.post_product_category(context.management_super_token, post_data)
    message = assert_error_message('Список категорий товаров не получен', product_category_list)
    assert product_category_list.status_code == 200, message
    product_category_list = json.loads(product_category_list.text.encode('utf-8').decode('utf-8-sig'))
    for product_category in product_category_list['data']:
        if product_category['merchantId'] == product_category_merchant and product_category_name in product_category['name']:
            product_categories_id = product_category['id']
            context.pr_category_id = product_categories_id
            break
    if product_categories_id == None:
        post_data = json.dumps({"name": product_category_name + str(code), "code": str(code), "merchantId": product_category_merchant})
        product_category_add = context.management_api.add_product_category(context.management_super_token, post_data)
        message = assert_error_message('Тестовая категория продуктов не добавлена', product_category_add)
        assert product_category_add.status_code == 200, message
        product_category_add = json.loads(product_category_add.text.encode('utf-8').decode('utf-8-sig'))
        product_categories_id = product_category_add['id']
        context.pr_category_id = product_category_add['id']

@fixture
def ensure_category_edit(context, timeout=30, **kwargs):
    category_edit_id = None
    category_edit_code = ''.join(random.choice('1234567890') for i in range(8))
    category_edit_name = 'Тестовая категория продуктов Behave' + str(category_edit_code)
    category_edit_merchant = context.merch_id
    post_data = json.dumps({"merchantIds": [category_edit_merchant], "page": 1, "pageSize": 1000, "column": "ChangeDate", "direction":2})
    category_list = context.management_api.post_product_category(context.management_super_token, post_data)
    message = assert_error_message('Список категорий товаров не получен', category_list)
    assert category_list.status_code == 200, message
    category_list = json.loads(category_list.text.encode('utf-8').decode('utf-8-sig'))
    for pr_category in category_list['data']:
        if pr_category['merchantId'] == category_edit_merchant and pr_category['name'] == category_edit_name:
            category_edit_id = pr_category['id']
            context.pr_category_id = category_edit_id
    if category_edit_id == None:
        post_data = json.dumps({"name": category_edit_name, "code": str(category_edit_code), "merchantId": category_edit_merchant})
        cat_list = context.management_api.add_product_category(context.management_super_token, post_data)
        message = assert_error_message('Тестовая категория продуктов не добавлена', cat_list)
        assert cat_list.status_code == 200, message
        cat_list = json.loads(cat_list.text.encode('utf-8').decode('utf-8-sig'))
        category_edit_id = cat_list['id']
        context.category_data = cat_list
        context.pr_category_id = category_edit_id


@fixture
def ensure_product_catalog(context,timeout=30, **kwargs):
    product_catalog_id = None
    get_product_in_catalog = []
    count_product_in_catalog = 3 # Пока для регулирования указал кол-во товаров тут
    product_catalog_executive_Authority = context.executive_id
    product_catalog_merchant = context.merch_id
    product_catalog_social_program = context.soc_program
    product_category = context.pr_category_id
    product_catalog_date = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    management_api = ManagementApi(context.config.userdata['management_url'])
    post_data = json.dumps({"column": "ChangeDate", "direction": None, "page": 1, "pageSize": 1000, "showCancelled": False, "merchantIds": [product_catalog_merchant], "socialProgramIds": [product_catalog_social_program]})
    post_catalog = management_api.search_product_catalog(context.management_super_token, post_data)
    message = assert_error_message('Список каталогов продуктов торг.предприятия не получен', post_catalog)
    assert post_catalog.status_code == 200, message
    post_catalog = json.loads(post_catalog.text.encode('utf-8').decode('utf-8-sig'))
    for catalogs in post_catalog['data']:
        if catalogs['merchantId'] == product_catalog_merchant and catalogs['socialProgramId'] == product_catalog_social_program:
            product_catalog_id = catalogs['id']
            post_data = json.dumps({"productCatalogId": product_catalog_id, "socialProgramIds": [product_catalog_social_program]})
            product = management_api.search_product_catalog_product(context.management_super_token, post_data)
            message = assert_error_message('Список продуктов в каталоге продуктов не получен', product)
            assert product.status_code == 200, message         
            product = json.loads(product.text.encode('utf-8').decode('utf-8-sig'))
            if len(product['data']) >= count_product_in_catalog:
                get_product_in_catalog = product['data']
                break
    if get_product_in_catalog == []:
        product_catalog_id = None
        post_data = json.dumps({"merchantId": product_catalog_merchant, "socialProgramId": product_catalog_social_program, "statusId": 1, "dateFrom": product_catalog_date, "executiveAuthorityId": product_catalog_executive_Authority, "typeId": 1})
        create_catalog = management_api.add_product_catelog(context.management_super_token, post_data)
        message = assert_error_message('Каталог продуктов не создан', create_catalog)
        assert create_catalog.status_code == 200, message
        create_catalog = json.loads(create_catalog.text.encode('utf-8').decode('utf-8-sig'))
        assert create_catalog['statusId'] == 1, 'Статус созданного каталога не верный: {0}, жидался статус 1'.format(create_catalog['statusId'])
        product_catalog_id = create_catalog['id']
        for products in range(count_product_in_catalog):
            product_code = ''.join(random.choice('1234567890') for i in range(4))
            price = 1 # для регулирования цены указано тут
            post_data = json.dumps({"name": "Тестовый товар Behave" + product_code, "merchantId": product_catalog_merchant, "categoryId": product_category, "unitTypeId": 1, "price": price, "productCatalogId": product_catalog_id, "code": product_code})
            create_product = management_api.add_product_catalog_product(context.management_super_token, post_data)
            message = assert_error_message('Продукт не добавлен в каталог', create_product)
            assert create_product.status_code == 200, message
            create_product = json.loads(create_product.text.encode('utf-8').decode('utf-8-sig'))
        post_data = json.dumps({"productCatalogId": product_catalog_id})
        product = management_api.search_product_catalog_product(context.management_super_token, post_data)
        message = assert_error_message('Список продуктов в каталоге продуктов не получен', product)
        assert product.status_code == 200, message
        product = json.loads(product.text.encode('utf-8').decode('utf-8-sig'))
        assert len(product['data']) >= count_product_in_catalog, 'кол-во продектов в созданном каталоге не верно проверьте каталог с id {0}'.format(product_catalog_id)
        get_product_in_catalog = product['data']
        post_data = json.dumps({"id": product_catalog_id})
        matchig = context.management_api.product_catalog_matching(context.management_super_token, post_data, full=False)
        message = assert_error_message('Каталог не согласован', matchig)
        assert matchig.status_code == 200, message
        post_data = json.dumps({"id": product_catalog_id})
        full_matching_catalog = context.management_api.product_catalog_matching(context.management_super_token, post_data, full= True)
        message = assert_error_message('Каталог полностью не согласован', full_matching_catalog)
        assert full_matching_catalog.status_code == 200, message
        context.product_in_catalog = get_product_in_catalog
    elif get_product_in_catalog != []:
        context.product_in_catalog = get_product_in_catalog

@fixture # пусто каталог для импорта
def ensure_product_empty_catalog(context,timeout=30, **kwargs):
    product_catalog_executive_Authority = context.executive_id
    product_catalog_merchant = context.merch_id
    product_catalog_social_program = context.soc_program
    product_catalog_date = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    post_data = json.dumps({"merchantId": product_catalog_merchant, "socialProgramId": product_catalog_social_program, "statusId": 1, "dateFrom": product_catalog_date, "executiveAuthorityId": product_catalog_executive_Authority, "typeId": 1})
    create_catalog = context.management.add_product_catelog(context.management_super_token, post_data)
    message = assert_error_message('Каталог не создан', create_catalog)
    assert create_catalog.status_code == 200, message
    create_catalog = json.loads(create_catalog.text.encode('utf-8').decode('utf-8-sig'))
    assert create_catalog['statusId'] == 1, 'Статус созданного каталога не верный: {0}, жидался статус 1'.format(create_catalog['statusId'])
    context.empty_product_catalog_id = create_catalog['id']

@fixture # Необходимо сгенерировать карту, завести счет и пополнить его
def ensure_card(context, check_nko=True,  timeout=30, **kwargs):
    gencard = (credit_card_number(16, 1))
    pan_hash = sha1(bytes((str(gencard)), 'utf-8')).hexdigest().upper()
    tsp = context.merch_id
    if check_nko == True:
        social_programm = context.social_program_code
        surrogate_name = pan_hash + social_programm
        post_data = json.dumps({"surrogate_name": surrogate_name, "project_id": context.merch_code, "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce", "region_id": "39"})
        wallet_check = context.nko_url.wallet_get_data(post_data)
        message = assert_error_message('Получить кошелек от НКО не удалось', wallet_check)
        assert wallet_check.status_code == 200, message
        wallet_check = json.loads(wallet_check.text.encode('utf-8').decode('utf-8-sig'))
        if wallet_check['code'] == 1050:
            post_data = json.dumps({"surrogate_name": surrogate_name,  "name_ending": str(gencard[0]), "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce"})
            create_wallet = context.nko_url.add_wallet(post_data)
            message = assert_error_message('Создать кошелек в НКО не удалось', create_wallet)
            assert create_wallet.status_code == 200, message
            create_wallet = json.loads(create_wallet.text.encode('utf-8').decode('utf-8-sig'))
        post_data = json.dumps({"surrogate_name": surrogate_name, "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce"})
        check_balance_in_wallet = context.nko_url.check_balance(post_data)
        message = assert_error_message('Получить информацию по кошульку в НКО не удалось', check_balance_in_wallet)
        assert check_balance_in_wallet.status_code == 200, message
        check_balance_in_wallet = json.loads(check_balance_in_wallet.text)
        if check_balance_in_wallet['code'] == 1050:
            post_data = json.dumps({"surrogate_name": surrogate_name, "name_ending": str(surrogate_name), "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce"})
            create_wallet = context.nko_url.add_wallet(post_data)
            message = assert_error_message('Не удалось добавить кошелёк', create_wallet)
            assert create_wallet.status_code == 200, message
            create_wallet = json.loads(create_wallet.text)
            balance_in_wallet = create_wallet['balance']
        else:
            balance_in_wallet = check_balance_in_wallet['balance']
        if 1000 > int(balance_in_wallet):
            post_balance = 1000 - int(balance_in_wallet)
            wallet_id = random.randint(1000000000000000,9999999999999999)
            tras_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+03:00")
            post_data = json.dumps({"id": wallet_id, "amount": post_balance, "surrogate_name": surrogate_name, "time": tras_time, "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce", "organisation_id": tsp})
            wallet_balance = context.nko_url.add_credit(post_data)
            message = assert_error_message('Не удалось пополнить кошелёк', wallet_balance)
            assert wallet_balance.status_code == 200, message
            wallet_balance = json.loads(wallet_balance.text)
        elif 1000 < int(balance_in_wallet):
            get_balance = (balance_in_wallet) - 1000
            id_tran_debit = random.randint(1000000000000000,9999999999999999)
            time_debit = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+03:00")
            post_data = json.dumps({"id": id_tran_debit, "amount": get_balance, "surrogate_name": surrogate_name, "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce", "organisation_id": tsp, "time": time_debit})
            wallet_spisenie = context.nko_url.wallet_write(post_data)
            message = assert_error_message('Не удалось списать средства с кошелька', wallet_spisenie)
            assert wallet_spisenie.status_code == 200, message
            wallet_spisenie = json.loads(wallet_spisenie.text)
    elif check_nko == False:
        message = 'Проверка карт имеет значение False'
    context.hash_pan = pan_hash

class ContextCleaner():
    def __init__(self, context):
        self.context = context

    def clean_test_tsp(self):
        pass