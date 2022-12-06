import json
import random
from fixtures import assert_error_message

@When('{option} получим список магазинов')
def step_impl(context, option):
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000})
    post_shop = context.management.post_shop(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Список магазинов не получен', post_shop)
        assert post_shop.status_code == 200, message
        post_shop = json.loads(post_shop.text)
        context.shop_list = post_shop['data']
    elif option == 'Неуспешно':
        message = assert_error_message('Список магазинов не получен', post_shop)
        assert post_shop.status_code != 200, message

@Then('Проверим что не пустой список магазинов')
def step_impl(context):
    assert context.shop_list != [], 'Список магазинов пустой, необходимо проверить корректность выполнения предусловий или шагов'

@When('{option} получим информацию по тестовому магазину')
def step_impl(context, option):
    test_shop_name = 'Тестовый магазин Behave'
    post_data = json.dumps({"name": test_shop_name, "column": None, "direction": None, "page": 1, "pageSize": 1000})
    test_shop = context.management.post_shop(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Информация по магазину не получен', test_shop)
        assert test_shop.status_code == 200, message
        test_shop = json.loads(test_shop.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Информация по магазину получен, ожидалась ошибка', test_shop)
        assert test_shop.status_code != 200, message


@When('{option} cоздадим {type_shop} магазин')
def step_impl(context, option, type_shop):
    testing_shop_name = 'Тестовая магазин Behave'
    testing_shop_code = ''.join(random.choice('1234567890') for i in range(10))
    testing_shop_merchant = context.merch_id
    testing_shop_phone = ''.join(random.choice('1234567890') for i in range(10))
    testing_shop_address = 'Test address'
    post_data = {"name": testing_shop_name, "code": str(testing_shop_code), "address": testing_shop_address, "phone": "+7" + str(testing_shop_phone), "merchantId": testing_shop_merchant, "typeId" : 1, "login":"","password":""}
    if type_shop == 'интернет':
        post_data['typeId'] = 2
    testing_shop = context.management.add_shop(context.management_super_token, json.dumps(post_data))
    if option == 'Успешно':
        message = assert_error_message('Магазин не удалось добавить', testing_shop)
        assert testing_shop.status_code == 200, message
        testing_shop = json.loads(testing_shop.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Магазин удалось добавить, ожидалась ошибка', testing_shop)
        assert testing_shop.status_code != 200, message
    context.test_shop_create = testing_shop['id']

@Then('Проверим в списке созданный тестовый магазин')
def step_impl(context):
    create_shops = context.shop_id
    get_create_shop = context.management.get_shop(context.management_super_token, create_shops)
    message = assert_error_message('Не удалось получить информацию по магазину', get_create_shop)
    assert get_create_shop.status_code == 200, message
    get_create_shop = json.loads(get_create_shop.text)

@When('{option} редактируем {type_shop} магазин')
def step_impl(context, option, type_shop):
    up_shop_name = 'Тестовая магазин Behave'
    up_shop_code = ''.join(random.choice('1234567890') for i in range(8))
    up_shop_address = 'Testings address'
    up_shop_phone = ''.join(random.choice('1234567890') for i in range(10))
    post_data = {"id": context.shop_id, "name": up_shop_name, "code": str(up_shop_code), "address": up_shop_address, "phone": "+7" + str(up_shop_phone), "merchantId": context.merch_id, "typeId" : 1, "login":"","password":""}
    up_test_shop = context.management.put_shop(context.management_super_token, json.dumps(post_data))
    if option == 'Успешно':
        message = assert_error_message('Не удалось отредактировать магазин', up_test_shop)
        assert up_test_shop.status_code == 200, message
        up_test_shop = json.loads(up_test_shop.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось отредактировать магазин, ожидалась ошибка', up_test_shop)
        assert up_test_shop.status_code != 200, message

@When('{option} удалим тестовый магазин')
def step_impl(context, option):
    delete_test_shop = context.shop_id
    delete_test_shop_url = context.management.delete_shop(context.management_super_token, delete_test_shop)
    if option == 'Успешно':
        message = assert_error_message('Не удалось удалить магазин', delete_test_shop_url)
        assert delete_test_shop_url.status_code == 200, message
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось удалить магазин, ожидалась ошибка', delete_test_shop_url)
        assert delete_test_shop_url.status_code == 400, message