from datetime import datetime
import json
import random
from fixtures import assert_error_message


@When('{option} получим список торговых предприятий')
def step_impl(context, option):
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000})
    merchant = context.management.post_merchant(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Список торг.предприятий не получен', merchant)
        assert merchant.status_code == 200, message
        merchant = json.loads(merchant.text)
        context.merchant_list = merchant['data']
    elif option == 'Неуспешно':
        message = assert_error_message('Список тор.предприятий получен, ожидалась ошибка', merchant)
        assert merchant.status_code != 200, message

@Then('Проверим что не пустой список торговых предприятий')
def step_impl(context):
    assert context.merchant_list != [], 'Список торг.предприятий пустой, необходимо проверить корректность выполнения предусловий или шагов'

@When('{option} получим информацию по тестовому торговому предприятию')
def step_impl(context, option):
    test_merchant_name = 'Тестовое торговое предприятие Behave'
    test_merchant_type = context.config.userdata['test_all_data']['typeId']
    test_merchant_region = context.config.userdata['test_all_data']['regionId']
    post_data = json.dumps({"name": test_merchant_name, "typeId": test_merchant_type, "regionId": test_merchant_region, "column": None, "direction": None, "page": 1, "pageSize": 1000})
    test_merchant = context.management.post_merchant(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Информация по торг.предприятию не получена', test_merchant)
        assert test_merchant.status_code == 200, message
        test_merchant = json.loads(test_merchant.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Информация по торг.предприятию получена, ожидалась ошибка', test_merchant)
        assert test_merchant.status_code != 200, message

@When('{option} cоздадим тестовое торговое преприятие')
def step_impl(context, option):
    add_test_merchant_name = 'Тестовая соц программа Behave'
    add_test_merchant_type = context.config.userdata['test_all_data']['typeId']
    add_test_merchant_region = context.config.userdata['test_all_data']['regionId']
    code = ''.join(random.choice('1234567890') for i in range(6))
    add_test_merchant_legal_name = 'Test name' + str(code)
    add_test_merchant_inn = ''.join(random.choice('1234567890') for i in range(12))
    add_test_merchant_legal_address = 'Test address' + str(add_test_merchant_inn)
    phone = ''.join(random.choice('1234567890') for i in range(10))
    add_test_merchant_soc_prog = context.soc_program
    add_test_merchant_productCatalogAutoLoad = context.config.userdata['test_all_data']['productCatalogAutoLoad']
    add_test_merchant_productCatalogAutoApprove = context.config.userdata['test_all_data']['productCatalogAutoApprove']
    post_data = json.dumps({"typeId": add_test_merchant_type,"parentid": None , "name": add_test_merchant_name, "code": code, "comment": None, "legalName": add_test_merchant_legal_name, "inn": add_test_merchant_inn, "legalAddress": add_test_merchant_legal_address, "phone": phone, "regionId": add_test_merchant_region, "socialProgramIds": [add_test_merchant_soc_prog], "productCatalogAutoLoad": add_test_merchant_productCatalogAutoLoad, "productCatalogAutoApprove": add_test_merchant_productCatalogAutoApprove})
    merchant_add = context.management.add_merchant(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Торг.предприятие не удалось создать', merchant_add)
        assert merchant_add.status_code == 200, message
        merchant_add = json.loads(merchant_add.text)
        context.create_tsp = merchant_add['id']
    elif option == 'Неуспешно':
        message = assert_error_message('Торг.предприятие удалось создать, ожидалась ошибка', merchant_add)
        assert merchant_add != 200, message

@Then('Проверим в списке созданное тестовое торговое преприятие')
def step_impl(context):
    create_tsp = context.create_tsp
    get_tsp = context.management.get_merchant(context.management_super_token, create_tsp)
    message = assert_error_message('Не удалось получить информацию по торг.предприятию', get_tsp)
    assert get_tsp.status_code == 200, message
    get_tsp = json.loads(get_tsp.text)

@When('{option} редактируем тестовое торговое предприятие')
def step_impl(context, option):
    up_tsp_id = context.merch_id
    code = ''.join(random.choice('1234567890') for i in range (6))
    up_tsp_name = 'Тестовая социальная программа behave' + str(code)
    inn = ''.join(random.choice('1234567890') for i in range (12))
    up_tsp_type = context.config.userdata['test_all_data']['typeId']
    up_tsp_region = context.config.userdata['test_all_data']['regionId']
    date_update = (datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    post_data = json.dumps({"id": up_tsp_id, "name": up_tsp_name, "code": code, "legalName": "Test legal Name Behave", "inn": inn, "legalAddress": "Test address", "dateFrom": date_update, "dateTo": None, "description": None, "typeId": up_tsp_type, "executiveAuthorityId": context.executive_id, "regionId": up_tsp_region, "socialProgramIds": [context.soc_program], "productCatalogAutoLoad": True, "productCatalogAutoApprove": True})
    update_tsp_list = context.management.put_merchant(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Не удалось отредактировать торг.предприятие', update_tsp_list)
        assert update_tsp_list.status_code == 200, message
        update_tsp_list = json.loads(update_tsp_list.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось отредактировать торг.предприятие, ожидалась ошибка', update_tsp_list)
        assert update_tsp_list != 200, message

@When('{option} удалим тестовое торговое предприятие')
def step_impl(context, option):
    delete_social_program = context.merch_id
    del_soc_proc = context.management.delete_merchant(context.management_super_token, delete_social_program)
    if option == 'Успешно':
        message = assert_error_message('Не удалось удалить торг.предприятие', del_soc_proc)
        assert del_soc_proc.status_code == 200, message
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось удалить торг.предприятие, ожидалась ошибка', del_soc_proc)
        assert del_soc_proc.status_code == 400, message