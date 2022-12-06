import json
import random
from fixtures import assert_error_message

@When('{options} получим список категорий продуктов')
def step_impl(context, options):
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000})
    post_product_category = context.management.post_product_category(context.management_super_token, post_data)
    if options == 'Успешно':
        message = assert_error_message('Список категорий продуктов не получен', post_product_category)
        assert post_product_category.status_code == 200, message
        post_product_category = json.loads(post_product_category.text)
        context.post_product_category_list = post_product_category
    elif options == 'Неуспешно':
        message = assert_error_message('Список категорий продуктов получен, ожидалась ошибка', post_product_category)
        assert post_product_category != 200, message

@Then('Проверим что не пустой список категорий продуктов')
def step_impl(context):
    assert context.post_product_category_list != [], 'Список категорий пустой, необходимо проверить корректность выполнения предусловий или шагов'

@When('{options} получим информацию по тестовой категории продуктов')
def step_impl(context, options):
    test_product_category_merchant = context.merch_id
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000, "merchantIds": [test_product_category_merchant], "enabled": True})
    test_product_category_add = context.management.post_product_category(context.management_super_token, post_data)
    if options == 'Успешно':
        message = assert_error_message('Информация по категории продуктов не получена', test_product_category_add)
        assert test_product_category_add.status_code == 200, message
        test_product_category_add = json.loads(test_product_category_add.text)
    elif options == 'Неуспешно':
        message = assert_error_message('Информация по категории продуктов получена, ожидалась ошибка', test_product_category_add)
        assert test_product_category_add.status_code != 200, message

@When('{options} cоздадим тестовую категорию продуктов')
def step_impl(context, options):
    add_test_product_category_name = 'Тестовая категория продуктов Behave'
    add_test_product_category_code = ''.join(random.choice('1234567890') for i in range(8))
    add_test_product_category_merchant = context.merch_id
    post_data = json.dumps({"name": add_test_product_category_name + str(add_test_product_category_code), "code": add_test_product_category_code, "merchantId": add_test_product_category_merchant})
    test_prod_cat = context.management.add_product_category(context.management_super_token, post_data)
    if options == 'Успешно':
        message = assert_error_message('Категорию продуктов не удалось создать', test_prod_cat)
        assert test_prod_cat.status_code == 200, message
        test_prod_cat = json.loads(test_prod_cat.text)
        context.create_product_category_add = test_prod_cat['id']
    elif options == 'Несупешно':
        message = assert_error_message('Категорию продуктов удалось создать, ожидалась ошибка', test_prod_cat)
        assert test_prod_cat.status_code != 200, message

@Then('Проверим в списке созданную тестовую категорию продуктов')
def step_impl(context):
    get_test_product_category = context.create_product_category_add
    get_product_category_add = context.management.get_product_category(context.management_super_token, get_test_product_category)
    message = assert_error_message('Не удалось получить информацию по категории льготы', get_product_category_add)
    assert get_product_category_add.status_code == 200, message
    get_product_category_add = json.loads(get_product_category_add.text)

@When('{options} редактируем тестовую категорию продуктов')
def step_impl(context, options):
    put_test_product_category_id = context.pr_category_id
    put_test_product_category_name = 'Тестовая категория продуктов Behave'
    put_test_product_category_code = ''.join(random.choice('12345667890') for i in range(8))
    put_test_product_category_merchant = context.merch_id
    post_data = json.dumps({"id": put_test_product_category_id, "name": put_test_product_category_name + str(put_test_product_category_code), "code": put_test_product_category_code, "merchantId": put_test_product_category_merchant})
    put_test_product_category = context.management.put_product_category(context.management_super_token, post_data)
    if options == 'Успешно':
        message = assert_error_message('Не удалось отредактировать категорию продуктов', put_test_product_category)
        assert put_test_product_category.status_code == 200, message
        put_test_product_category = json.loads(put_test_product_category.text)
    elif options == 'Неуспешно':
        message = assert_error_message('Удалось отредактировать категорию льготы, ожидалась ошибка', put_test_product_category)
        assert put_test_product_category.status_code != 200, message

@When('{options} удалим тестовую категорию продуктов')
def step_impl(context, options):
    delete_test_product_category_id = context.pr_category_id
    delete_test_product_category = context.management.delete_product_category(context.management_super_token, delete_test_product_category_id)
    if options == 'Успешно':
        message = assert_error_message('Не удалось удалить категорию льготы', delete_test_product_category)
        assert delete_test_product_category.status_code == 200, message
    elif options == 'Неуспешно':
        message = assert_error_message('Удалось удалить категорию льготы, ожидалась ошибка', delete_test_product_category)
        assert delete_test_product_category.status_code == 400, message