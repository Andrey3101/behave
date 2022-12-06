import json
import random
from fixtures import assert_error_message

@When('{option} получим список терминалов')
def step_impl(context, option):
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000})
    post_terminal_list = context.management.post_terminal(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Список терминалов не получен', post_terminal_list)
        assert post_terminal_list.status_code == 200, message
        post_terminal_list = json.loads(post_terminal_list.text)
        context.terminal_list = post_terminal_list['data']
    elif option == 'Неуспешно':
        message = assert_error_message('Список терминалов получен, ожидалась ошибка', post_terminal_list)
        assert post_terminal_list != 200, message

@Then('Проверим что не пустой список терминалов')
def step_impl(context):
    assert context.terminal_list != [], 'Список терминалов пустой, необходимо проверить корректность выполнения предусловий или шагов'

@When('{option} получим информацию по тестовому терминалу')
def step_impl(context, option):
    test_terminal_merchant = context.merch_id
    test_terminal_shop = context.shop_id
    post_data = json.dumps({"column": None, "dicrection": None, "page": 1, "pageSize": 1000, "merchantId": test_terminal_merchant, "shopId": test_terminal_shop})
    test_terminal = context.management.post_terminal(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Информация по терминалу не получена', test_terminal)
        assert test_terminal.status_code == 200, message
        test_terminal = json.loads(test_terminal.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Информация по терминалу получена, ожидалась ошибка', test_terminal)
        assert test_terminal != 200, message

@When('{option} cоздадим тестовый терминал')
def step_impl(context, option):
    test_terminal_number = ''.join(random.choice('1234567890') for i in range(10))
    test_terminal_shop = context.shop_id
    test_terminal_merchant = context.merch_id
    post_data = json.dumps({"number": test_terminal_number, "shopId": test_terminal_shop, "merchantId": test_terminal_merchant})
    test_terminal_create = context.management.add_terminal(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Терминал не удалось создать', test_terminal_create)
        assert test_terminal_create.status_code == 200, message
        test_terminal_create = json.loads(test_terminal_create.text)
        context. test_create_terminal = test_terminal_create['id']
    elif option == 'Неуспешно':
        message = assert_error_message('Терминал удалось создать, ожидалась ошибка', test_terminal_create)
        assert test_terminal_create.status_code != 200, message

@Then('Проверим в списке созданный тестовый терминал')
def step_impl(context):
    create_terminal = context.test_create_terminal
    get_terminal = context.management.get_terminal(context.management_super_token, create_terminal)
    message = assert_error_message('Не удалось получить информацию по терминалу', get_terminal)
    assert get_terminal.status_code == 200, message
    get_terminal = json.loads(get_terminal.text)

@When('{option} редактируем тестовый терминал')
def step_impl(context, option):
    update_terminal_id = context.terminal_id
    update_terminal_number = ''.join(random.choice('1234567890') for i in range(10))
    update_terminal_shop = context.shop_id
    update_terminal_merchant = context.merch_id
    post_data = json.dumps({"id": update_terminal_id ,"number": update_terminal_number, "shopId": update_terminal_shop, "merchantId": update_terminal_merchant})
    update_terminal_create = context.management.put_terminal(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Не удалось отредактировать терминал', update_terminal_create)
        assert update_terminal_create.status_code == 200, message
        update_terminal_create = json.loads(update_terminal_create.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось отредактировать терминал, ожидалась ошибка', update_terminal_create)
        assert update_terminal_create.status_code != 200, message

@Then('Удалим тестовый терминал')
def step_impl(context):
    delete_terminal = context.terminal_id
    del_terminal = context.management.delete_terminal(context.management_super_token, delete_terminal)
    message = assert_error_message('Не удалось удалить терминал', del_terminal)
    assert del_terminal.status_code == 200, message