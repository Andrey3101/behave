import json
import random
from fixtures import assert_error_message


@When('{option} получим список категорий льгот')
def step_impl(context, option):
    post_data = json.dumps({"page": 1,"pageSize": 5,"column": None,"direction": None})
    test_benefit_type = context.management.post_benefit_types(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Список категорий льгот не получен', test_benefit_type)
        assert test_benefit_type.status_code == 200, message
        test_benefit_type = json.loads(test_benefit_type.text)
        context.test_benefit_list = test_benefit_type['data']
    elif option == 'Неуспешно':
        message = assert_error_message('Список категорий получен успешно, ожидалась ошибка', test_benefit_type)
        assert test_benefit_type.status_code != 200, message

@Then('Проверим что список категорий льгот не пустой')
def step_impl(context):
    assert context.test_benefit_list != [], 'Список категорий пустой, необходимо проверить корректность выполнения предусловий или шагов'

@When('{option} получим информацию по тестовой категории льгот')
def step_impl(context, option):
    test_category_name = 'Тестовая категория льгот Behave'
    test_category_region = context.config.userdata['test_all_data']['regionId']
    post_data = json.dumps({"name": test_category_name, "code": None, "regionIds": [test_category_region], "page": 1, "pageSize": 1000, "column": None, "direction": None})
    test_benefit_category_list = context.management.post_benefit_types(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Информация по категории льготы не получена', test_benefit_category_list)
        assert test_benefit_category_list.status_code == 200, message
        test_benefit_category_list = json.loads(test_benefit_category_list.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Информация по категории льготы получена, ожидалась ошибка', test_benefit_category_list)
        assert test_benefit_category_list != 200, message

@When('{option} создадим тестовую категорию льгот')
def step_impl(context, option):
    test_benefit_type_name_add = 'Тестовая категория льгот'
    code = ''.join(random.choice('1234567890') for i in range(6))
    test_benefit_type_region_add = context.config.userdata['test_all_data']['regionId']
    post_data = json.dumps({"name": test_benefit_type_name_add, "code": code, "regionId": test_benefit_type_region_add, "description": test_benefit_type_name_add})
    test_create_benefit_type = context.management.add_benefit_types(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Категорию льготы не удалось создать', test_create_benefit_type)
        assert test_create_benefit_type.status_code == 200, message
        test_create_benefit_type = json.loads(test_create_benefit_type.text)
        context.create_benefit_type = test_create_benefit_type['id']
    elif option == 'Неуспешно':
        message = assert_error_message('Категорию льготы удалось создать, ожидалась ошибка', test_create_benefit_type)
        assert test_create_benefit_type.status_code != 200, message

@Then('Проверим в списке созданную категорию льгот')
def step_impl(context):
    test_benefit_type = context.create_benefit_type
    get_benefit_type = context.management.get_benefit_type(context.management_super_token, test_benefit_type)
    message = assert_error_message('Не удалось получить информацию по категории льготы', get_benefit_type)
    assert get_benefit_type.status_code == 200, message
    get_benefit_type = json.loads(get_benefit_type.text)
    context.check_benefit_type = get_benefit_type['id']

@When('{option} редактируем тестовую категорию льгот')
def step_impl(context, option):
    up_benefit_type_id = context.benefit_id
    up_benefit_type_name = 'Тестовая категория льгот behave'
    up_benefit_type_region = context.config.userdata['test_all_data']['regionId']
    code = ''.join(random.choice('1234567890') for i in range(6))
    post_data = json.dumps({"Id": up_benefit_type_id, "name": up_benefit_type_name + str(code), "description": up_benefit_type_name, "code": code, "regionId": up_benefit_type_region, "registerTypeId": 1})
    update_benefit_type = context.management.put_benefit_type(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Не удалось отредактировать категорию льготы', update_benefit_type)
        assert update_benefit_type.status_code == 200, message
        update_benefit_type = json.loads(update_benefit_type.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось отредактировать категорию льготы, ожидалась ошибка', update_benefit_type)
        assert update_benefit_type.status_code != 200, message

@When('{option} удалим тестовую категорию льгот')
def step_impl(context, option):
    delete_benefit_type = context.benefit_id
    del_benefit_type = context.management.delete_benefit_type(context.management_super_token, delete_benefit_type)
    if option == 'Успешно':
        message = assert_error_message('Не удалось удалить категорию льготы', del_benefit_type)
        assert del_benefit_type.status_code == 200, message
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось удалить категорию льготы, ожидалась ошибка', del_benefit_type)
        assert del_benefit_type.status_code == 400, message
