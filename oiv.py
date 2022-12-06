import random
import json
from fixtures import assert_error_message

@When('{option} получим список социальных учреждений')
def step_impl(context, option):
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000})
    oivs = context.management.post_executive_authorities_list(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Список социальных учреждений не получен', oivs)
        assert oivs.status_code == 200, message
        oivs = json.loads(oivs.text)
        context.oivs_list = oivs['data']
    elif option == 'Неуспешно':
        message = assert_error_message('Список социальных учреждений получен, ожидалась ошибка', oivs)
        assert oivs.status_code != 200, message

@Then('Проверим что не пустой список социальных учреждений')
def step_impl(context):
    assert context.oivs_list != [], 'Список социальных учреждени пустой, необходимо проверить корректность выполнения предусловий или шагов'

@When('{option} получим информацию по {number} соц.учреждению из списка')
def step_impl(context, number, option):
    oiv_number = (context.oivs_list[int(number)-1])['id']
    oiv_get = context.management.get_exeutive_authorities(context.management_super_token, oiv_number)
    if option == 'Успешно':
        message = assert_error_message('Информация по соц.учреждению не получена', oiv_get)
        assert oiv_get.status_code == 200, message
        oiv_get = json.loads(oiv_get.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Информация по соц.учреждению получена, ожидалась ошибка', oiv_get)
        assert oiv_get.status_code != 200, message

@When('{option} cоздадим социальное учреждение')
def step_impl(context, option):
    test_executive_id = None
    test_executive = 'Социальное учреждение Behave'
    test_executive_type = context.config.userdata['test_all_data']['typeId']
    test_executive_region = context.config.userdata['test_all_data']['regionId']
    test_executive_project = context.config.userdata['test_all_data']['type_project']
    post_data = json.dumps({"regionIds": [test_executive_region], "typeIds": [test_executive_type]})
    search_executive = context.management.post_executive_authorities_list(context.management_super_token, post_data)
    message = assert_error_message('Список соц.учреждений не получен', search_executive)
    assert search_executive.status_code == 200, message
    search_executive = json.loads(search_executive.text)
    for executive in search_executive['data']:
        if executive['regionId'] == test_executive_region and executive['typeId'] == test_executive_type and executive['name'] == test_executive:
            test_executive_id = executive['id']
            context.test_create_oiv = test_executive_id
    if test_executive_id == None:
        post_data = json.dumps({"name": test_executive, "regionId": test_executive_region, "typeId": test_executive_type, "projectTypeId": test_executive_project})
        create_oiv = context.management.add_executive_authorities(context.management_super_token, post_data)
        message = assert_error_message('Социальное учреждение не удалось создать', create_oiv)
        assert create_oiv.status_code == 200, message
        create_oiv = json.loads(create_oiv.text)
        test_executive_id = create_oiv['id']
        context.test_create_oiv = test_executive_id
    if option == 'Успешно':
        get_oiv_id = context.test_create_oiv
        get_oiv = context.management.get_exeutive_authorities(context.management_super_token, get_oiv_id)
        message = assert_error_message('Социальное учреждение не удалось создать и получить по нему информацию', get_oiv)
        assert get_oiv.status_code == 200, message
        get_oiv = json.loads(get_oiv.text)
        context.add_executive = get_oiv
    elif option == 'Неуспешно':
        message = assert_error_message('Социальное учреждение удалось создать и получить информацию по нему, ожидалась ошибка', get_oiv)
        assert get_oiv.status_code != 200, message

@Then('Проверим в списке созданное социальное учреждение')
def step_impl(context):
    add_executive_id = context.add_executive['id']
    get_executive = context.management.get_exeutive_authorities(context.management_super_token, add_executive_id)
    message = assert_error_message('Не удалось получить информацию по социальному учреждению', get_executive)
    assert get_executive.status_code == 200, message
    get_executive = json.loads(get_executive.text)
    context.check_executive_id = get_executive['id']

@When('{option} редактируем тестовое социальное учреждение')
def step_impl(context, option):
    up_oiv_id = context.executive_id
    code = ''.join(random.choice('1234567890') for i in range(6))
    up_oiv_name = "Тестовый ОИВ " + str(code)
    up_oiv_type = context.config.userdata['test_all_data']['typeId']
    up_oiv_region = context.config.userdata['test_all_data']['regionId']
    up_oiv_project = context.config.userdata['test_all_data']['type_project']
    post_data = json.dumps({"id": up_oiv_id, "name": up_oiv_name, "typeId": up_oiv_type, "regionId": up_oiv_region, "projectTypeId": up_oiv_project})
    update_oiv = context.management.put_executive_authorities(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Не удалось отредактировать социальное учреждение', update_oiv)
        assert update_oiv.status_code == 200, message
        update_oiv = json.loads(update_oiv.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось отредактировать социальное учреждение, ожидалась ошибка', update_oiv)
        assert update_oiv.status_code != 200, message

@When('{option} удалим тестовое социальное учреждение')
def step_impl(context, option):
    del_executive_id = context.executive_id
    del_executive = context.management.delete_executive_authorities(context.management_super_token, del_executive_id)
    if option == 'Успешно':
        message = assert_error_message('Не удалось удалить социальное учреждение', del_executive)
        assert del_executive.status_code == 200, message
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось удалить социальное учреждение, ожидалась ошибка', del_executive)
        assert del_executive.status_code == 400, message