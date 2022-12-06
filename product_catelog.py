import datetime
import json
import random
from time import sleep
from fixtures import assert_error_message

@When('{option} получим список каталогов товаров')
def step_impl(context, option):
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000})
    prod_catalog = context.management.search_product_catalog(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Список каталогов товаров не получен', prod_catalog)
        assert prod_catalog.status_code == 200, message
        prod_catalog = json.loads(prod_catalog.text)
        context.product_catalogs = prod_catalog
    elif option == 'Неуспешно':
        message = assert_error_message('Список социальных учреждений получен, ожидалась ошибка', prod_catalog)
        assert prod_catalog != 200, message
    
@Then('Проверим что список каталогов не пустой')
def step_impl(context):
    assert context.product_catalogs != [], 'Список каталогов товаров пустой, необходимо проверить корректность выполнения предусловий или шагов'

@When('{option} {action} тестовый каталог товаров')
def step_impl(context, option, action):
    product_catalog_id = None
    product_catalog_status = 1
    product_catalog_executive = context.executive_id
    product_catalog_merchant = context.merch_id
    product_catalog_social = context.soc_program
    product_catalog_date = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    if option == 'Успешно' and action == 'создадим':
        post_data = json.dumps({"merchantId": product_catalog_merchant, "socialProgramId": product_catalog_social, "statusId": product_catalog_status, "dateFrom": product_catalog_date, "executiveAuthorityId": product_catalog_executive, "typeId": 1})
        product_catalog_list = context.management.add_product_catelog(context.management_super_token, post_data)
        message = assert_error_message('Тестовый каталог не создан', product_catalog_list)
        assert product_catalog_list.status_code == 200, message
        product_catalog_list = json.loads(product_catalog_list.text)
        product_catalog_id = product_catalog_list['id']
        context.create_catalog = product_catalog_id
    elif option == 'Успешно' and action == 'редактируем':
        product_catalog_update_id = context.get_product_catalog_id
        post_data = json.dumps({"id": product_catalog_update_id, "dateFrom": product_catalog_date, "statusId": product_catalog_status, "executiveAuthorityId": product_catalog_executive, "merchantId": product_catalog_merchant, "socialProgramId": product_catalog_social, "matchingSentDate": product_catalog_date, "matchingDate": product_catalog_date, "typeId": 1})
        product_catalog_update = context.management.put_product_catalog(context.management_super_token, post_data)
        message = assert_error_message('Тестовый каталог не отредактирован', product_catalog_update)
        assert product_catalog_update.status_code == 200, message
        product_catalog_update = json.loads(product_catalog_update.text)

@Then('Проверим тестовый каталог товаров')
def step_impl(context):
    product_catalog_get_id = None
    product_catalog_executive = context.executive_id
    product_catalog_merchant = context.merch_id
    product_catalog_social = context.soc_program
    post_data = json.dumps({"executiveAuthorityIds": [product_catalog_executive], "merchantIds": [product_catalog_merchant], "socialProgramIds": [product_catalog_social]})
    product_catalog_get = context.management.search_product_catalog(context.management_super_token, post_data)
    message = assert_error_message('Список каталогов товаров не получен', product_catalog_get)
    assert product_catalog_get.status_code == 200, message
    product_catalog_get = json.loads(product_catalog_get.text)
    for catalogs_product in product_catalog_get['data']:
        if catalogs_product['executiveAuthorityId'] == product_catalog_executive and catalogs_product['socialProgramId'] == product_catalog_social and catalogs_product['merchantId'] == product_catalog_merchant:
            product_catalog_get_id = catalogs_product['id']
            context.get_product_catalog_id = product_catalog_get_id
        get_product_catalog = context.management.get_product_catalog(context.management_super_token, product_catalog_get_id)
        message = assert_error_message('Каталог товаров не получен', get_product_catalog)
        assert get_product_catalog.status_code == 200, message
        get_product_catalog = json.loads(get_product_catalog.text)


@When('{option} добавим тестовый товар в каталог товаров')
def step_impl(context, option):
    product_in_catalog = []
    catalog_id = None
    code = ''.join(random.choice('1234567890') for i in range(8))
    create_product_catalog_name = 'Тестовый товар Behave'
    create_product_catalog_merchant = context.merch_id
    create_product_catalog_category = context.pr_category_id
    create_product_catalog_social = context.soc_program
    create_product_catalog_executive = context.executive_id
    count_produts_in_catalog = 3
    post_data = json.dumps({"merchantIds": [create_product_catalog_merchant], "socialProgramIds": [create_product_catalog_social]})
    get_catalog = context.management.search_product_catalog(context.management_super_token, post_data)
    message = assert_error_message('Список каталогов товаров не получен', get_catalog)
    assert get_catalog.status_code == 200, message
    get_catalog = json.loads(get_catalog.text)
    for catalog in get_catalog['data']:
        if catalog['merchantId'] == create_product_catalog_merchant and catalog['socialProgramId'] == create_product_catalog_social:
            catalog_id = catalog['id']
            context.catalog_ids = catalog_id
            get_product = json.dumps({"productCatalogId": catalog_id})
            products = context.management.search_product_catalog_product(context.management_super_token, get_product)
            message = assert_error_message('Список продуктов в каталоге не получен', products)
            assert products.status_code == 200, message
            products = json.loads(products.text)
            if len(products) >= count_produts_in_catalog:
                product_in_catalog = products
    if product_in_catalog == []:
        catalog_id = None
        date = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
        post_data = json.dumps({"merchantId": create_product_catalog_merchant, "socialProgramId": create_product_catalog_social, "statusId": 1, "dateFrom": date, "executiveAuthorityId": create_product_catalog_executive, "typeId": 1}) # Значение typeId указано по умолчанию, возможно стоит вынести в конфиг
        catalog_create = context.management.add_product_catelog(context.management_super_token, post_data)
        message = assert_error_message('Тестовый каталог не создан', catalog_create)
        assert catalog_create.status_code == 200, message
        catalog_create = json.loads(catalog_create.text)
        catalog_id = catalog_create['id']
        context.catalog_ids = catalog_id
        for product in range(count_produts_in_catalog):
            code_product = ''.join(random.choice('1234567890') for i in range (6))
            price = ''.join(random.choice('1234567890') for i in range(2))
            post_data = json.dumps({"name": create_product_catalog_name, "merchantId": create_product_catalog_merchant, "categoryId": create_product_catalog_category, "unitTypeId": 1, "price": price, "productCatalogId": catalog_id, "code": code_product})
            post_product_create = context.management.add_product_catalog_product(context.management_super_token, post_data)
            message = assert_error_message('В тестовый каталог продукт не добавлен', post_product_create)
            assert post_product_create.status_code == 200, message
            post_product_create = json.loads(post_product_create.text)
        product_get = json.dumps({"productCatalogId": catalog_id})
        post_prod = context.management.search_product_catalog_product(context.management_super_token, product_get)
        message = assert_error_message('Список продуктов в каталоге не получен', post_prod)
        assert post_prod.status_code == 200, message
        post_prod = json.loads(post_prod.text)
        if len(post_prod) >= count_produts_in_catalog:
            product_in_catalog = post_prod
    if option == 'Успешно':
        product_catag_id = context.catalog_ids
        create_product_in_catalog = context.management.get_product_catalog(context.management_super_token,product_catag_id)
        message = assert_error_message('Информация по продукту в тестовом каталоге не получена', create_product_in_catalog)
        assert create_product_in_catalog.status_code == 200, message
        create_product_in_catalog = json.loads(create_product_in_catalog.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Информация по продукту в тестовом каталоге получена, ожидалась ошибка', create_product_in_catalog)
        assert create_product_in_catalog.status_code != 200, message

@Then('Отправим тестовый каталог товаров на согласование')
def step_impl(context):
    product_catalog_fully_math = context.catalog_ids
    post_data = json.dumps({"id": product_catalog_fully_math})
    product_catalog_matching = context.management.product_catalog_matching(context.management_super_token, post_data, full = False)
    message = assert_error_message('Тестовый каталог не отправлен на согласование', product_catalog_matching)
    assert product_catalog_matching.status_code == 200, message

@Then('Полностью согласуем тестовый каталог товаров')
def step_impl(context):
    product_catalog_math = context.catalog_ids
    post_data = json.dumps({"id": product_catalog_math})
    product_catalog_math_fully = context.management.product_catalog_matching(context.management_super_token, post_data, full = True)
    message = assert_error_message('Тестовый каталог не отправлен на полное согласование', product_catalog_math_fully)
    assert product_catalog_math_fully.status_code == 200, message

@Then('Проверим {option} тестовый каталог')
def step_impl(context,option):
    if option == 'созданный':
        get_product_catalog = context.create_catalog
        up_product_catalog = context.management.get_product_catalog(context.management_super_token, get_product_catalog)
        message = assert_error_message('Информация по созданному каталогу не получена', up_product_catalog)
        assert up_product_catalog.status_code == 200, message
        up_product_catalog = json.loads(up_product_catalog.text)
    elif option == 'отредактированный':
        put_product_catalog = context.get_product_catalog_id
        get_update_product_catalog = context.management.get_product_catalog(context.management_super_token, put_product_catalog)
        message = assert_error_message('Информация по отредактированному каталогу не получена', get_update_product_catalog)
        assert get_update_product_catalog.status_code == 200, message
        get_update_product_catalog = json.loads(get_update_product_catalog.text)
    elif option == 'согласованный':
        matching_products_catalog = context.catalog_ids
        match_product_catalog = context.management.get_product_catalog(context.management_super_token, matching_products_catalog)
        message = assert_error_message('Информация по согласованному каталогу не получена', match_product_catalog)
        assert match_product_catalog.status_code == 200, message
        match_product_catalog = json.loads(match_product_catalog.text)
    pass

@Given('Подготовлен тестовый xslx файл каталога товаров c {counts} {string}')
def step_impl(context, counts, string):
    context.import_data_catalog = {'sheets':[]}
    sheet = {'data': []}
    sheet['name'] = 'Import Catalog products'
    sheet['header'] = ['Категория', 'Код категории', 'Название', 'Артикул', 'Цена', 'Единица', 'Лимит', 'Период']
    data = []
    for count in range(int(counts)):
        category_data = context.category_data['name']
        category_code = context.category_data['code']
        price = ''.join(str(random.randint(1,9)))
        code_pr = ''.join(random.choice('1234567890') for i in range(8))
        name = "Тестовый товар" + str(code_pr)
        context.name_prdct = name
        context.name_code_pr = code_pr
        name_ed = 'шт.'
        name_lim = '0'
        name_per = 'нет'
        sheet['data'].append([category_data, category_code, name, str(code_pr), str(price), name_ed, name_lim, name_per])
    context.import_data_catalog['sheets'].append(sheet)
    for x in range(3):
        try:
            context.import_xlsx_catalog = context.exel.generate_excel(context.import_data_catalog)
            break
        except:
            context.behave_log.info('Генерация xlsx файла прошла с ошибкой, будет повторная попытка №{0}'.format(x+2))
            sleep(2)

@When('{status} импортируем каталог товаров в {type} каталог')
def step_impl(context, status, type):
    try:
        context.import_xlsx_catalog
    except AttributeError:
        raise AttributeError('Файл не был сгенерирован автотестом, проверьте шаг "Дано"(Given) Подготовлен тестовый xlsx файл каталога товаров с 1 или более записью'.format())
    if type == 'новый':
        creat_catalog = context.management.import_product_catalog(context.management_super_token, context.import_xlsx_catalog, context.soc_program , context.merch_id)
    elif type == 'созданный':
        creat_catalog = context.management.import_product_catalog_products(context.management_super_token, context.import_xlsx_catalog, context.empty_product_catalog_id)
    if status == 'Успешно':
        message = assert_error_message('Информация по согласованному каталогу не получена', creat_catalog)
        assert creat_catalog.status_code == 200, message
        response = json.loads(creat_catalog.text)
        assert response['errorDataCount'] == 0, 'Импорт содержит ошибки в кол-ве {0}. importLogId {1}'.format(response['errorDataCount'], response['importLogId'])
        assert response['importLogId'] != 0, 'В ответе на импорт importLogId имеет значение 0. Весь ответ {0}'.format(response)
        context.status_import = response

@Then('Проверим созданный тестовый каталог товаров')
def step_impl(context):
    product_soc_prg = context.soc_program
    product_tsp = context.merch_id
    name_prod = context.name_prdct
    prod_code = context.name_code_pr
    category = context.category_data['id']
    post_data = json.dumps({"column": "ChangeDate", "direction": None, "page": 1, "pageSize": 1000, "showCancelled": False, "merchantIds": [product_tsp], "socialProgramIds": [product_soc_prg]})
    search_product_catalog = context.management.search_product_catalog(context.management_super_token, post_data)
    message = assert_error_message('Список продуктов в каталоге не получен', search_product_catalog)
    assert search_product_catalog.status_code == 200, message
    search_product_catalog = json.loads(search_product_catalog.text)
    for merch in search_product_catalog['data']:
        if merch['statusId'] == 3:
            merch_id = merch['id']
            get_prdct_ctg = context.management.get_product_catalog(context.management_super_token, merch_id)
            message = assert_error_message('Информация по каталогу продуктов не получена', get_prdct_ctg)
            assert get_prdct_ctg.status_code == 200, message
            get_prdct_ctg = json.loads(get_prdct_ctg.text)
            post_data = json.dumps({"column": "ChangeDate", "direction": None, "page": 1, "pageSize": 1000, "productCatalogId": merch_id})
            prod_cat_prod_search = context.management.search_product_catalog_product(context.management_super_token, post_data)
            message = assert_error_message('Список продуктов в каталоге не получен', prod_cat_prod_search)
            assert prod_cat_prod_search.status_code == 200, message
            for pr_cat_pr in json.loads(prod_cat_prod_search.text)['data']:
                if pr_cat_pr['name'] == name_prod and pr_cat_pr['code'] == prod_code and pr_cat_pr['categoryId'] == category and pr_cat_pr['statusId'] == 3:
                    assert 'Продукты импортированы в каталог без ошибок'
                else:
                    assert 'Произошла ошибка при добавлении продуктов в импортированный каталог'
        else:
            assert 'Произошла ошибка'