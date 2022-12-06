from datetime import datetime
import json
import random
from uuid import uuid4
from fixtures import assert_error_message


class BatchAuthData():
    def __init__(self):
        self.merchant_auth = None
        self.terminal_auth = None
        self.social_prgm = None
        self.PAN_hash = None
        self.auth_time = None
        self.auth_id = None
        self.product_auth = None
        self.gener_key = None

class BatchTransferData():
    def __init__(self):
        self.merchant_transfer = None
        self.terminal_tranfer = None
        self.auth_code = None
        self.transfer_time = None
        self.transfer_id = None

@Given('Запрос на резервирование "auth_request_v2"')
def step_impl(context):
    context.BatchAuthData = BatchAuthData()
    context.BatchAuthData.merchant_auth = context.sh_code
    context.BatchAuthData.terminal_auth = context.term_code
    context.BatchAuthData.social_prgm = context.social_program_code
    context.BatchAuthData.PAN_hash = context.hash_pan
    context.BatchAuthData.auth_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
    context.BatchAuthData.auth_id = str(uuid4())
    prodct = context.product_in_catalog
    context.prdt = prodct
    prodct = random.choice(context.product_in_catalog)
    context.BatchAuthData.product_auth = prodct
    context.BatchAuthData.gener_key = context.auth_key


@When('Запрос на резервирование "auth_request_v2" отправлен в терминальную службу')
def step_impl(context):
    post_data = json.dumps({"merchantId": context.BatchAuthData.merchant_auth, "terminalId": context.BatchAuthData.terminal_auth, "socialProgramId": context.BatchAuthData.social_prgm, "paymentType": 0, "card": {"pan": context.BatchAuthData.PAN_hash}, "batch": {"id": context.BatchAuthData.auth_id, "dateTime": context.BatchAuthData.auth_time, "amount": context.BatchAuthData.product_auth['price'], "products": [{"type": 0, "code": context.BatchAuthData.product_auth['code'], "name": context.BatchAuthData.product_auth['name'], "unit": "PIEC", "quantity": str(float(context.BatchAuthData.product_auth['price'])), "price": str(float(context.BatchAuthData.product_auth['price'])), "amount": str(float(context.BatchAuthData.product_auth['price']))}]}})
    auth_batch_transaction = context.terminal_v2_api.batch_auth(context.BatchAuthData.gener_key, post_data)
    message = assert_error_message('Не удалось отправить запрос резервирования по протоколу Эвотор', auth_batch_transaction)
    assert auth_batch_transaction.status_code == 200, message
    auth_batch_transaction = json.loads(auth_batch_transaction.text)
    context.auth_reservation_v2 = auth_batch_transaction
    context.authtorization_code = auth_batch_transaction['authCode']

@Then('Получен ответ "responseCode: {status}"')
def step_impl(context, status):
    auth_data = context.auth_reservation_v2
    result_code = auth_data['responseCode']
    if result_code == int(status):
        return 'полученный ответ не соответствует ОР, ожидася код {0}'.format(result_code)
    else:
        return 'полученный ответ не соотвествует ОР, получен код {0}'.format(result_code)

@When('Значение {entities} "{data}" из запроса отсутствует в {proc}')
def step_impl(context, entities, data, proc):
    if proc == 'СП':
        if entities == 'магазина' and data == 'merchant_id':
            context.BatchAuthData.merchant_auth = '0'
        else:
            context.BatchAuthData.merchant_auth = context.sh_code
        if entities == 'кассы' and data == 'terminal_id':
            context.BatchAuthData.terminal_auth = '0'
        else:
            context.BathAuthData = context.term_code
    else:
        if entities == 'карты' and data == 'panhash':
            context.BatchAuthData.PAN_hash = '0'
        else:
            context.BatchAuthData = context.hash_pan
            pass
    pass

@Given('Проверим {option} в НКО, там он {wallet_option} {balance}')
def step_impl(context, option, balance, wallet_option):
    pan = context.hash_pan
    soc_program = context.social_program_code
    tsp = context.merch_id
    surrogate_name = pan + soc_program
    post_data = json.dumps({"surrogate_name": surrogate_name, "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce"})
    check_balance_in_wallet = context.nko_url.check_balance(post_data)
    message = assert_error_message('Получить информацию по кошульку в НКО не удалось', check_balance_in_wallet)
    assert check_balance_in_wallet.status_code == 200, message
    check_balance_in_wallet = json.loads(check_balance_in_wallet.text)
    if option == 'кошелек' and balance == 'отсутствует':
        assert check_balance_in_wallet['code'] == 1050, 'Ожидался код 1050 что кошелёк будет не найден, в ответ получили {0}, карта {1} и соц.прогамма {2}'.format(check_balance_in_wallet['code'], pan, soc_program)
    elif option == 'баланс' and balance != 'отсутствует':
        balance = int(balance)
        if check_balance_in_wallet['code'] == 1050:
            post_data = json.dumps({"surrogate_name": surrogate_name, "name_ending": str(surrogate_name), "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce"})
            create_wallet = context.nko_url.add_wallet(post_data)
            message = assert_error_message('Не удалось добавить кошелёк', create_wallet)
            assert create_wallet.status_code == 200, message
            create_wallet = json.loads(create_wallet.text)
            balance_in_wallet = create_wallet['balance']
        else:
            balance_in_wallet = check_balance_in_wallet['balance']
        if balance > int(balance_in_wallet):
            post_balance = balance - int(balance_in_wallet)
            wallet_id = random.randint(1000000000000000,9999999999999999)
            tras_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+03:00")
            post_data = json.dumps({"id": wallet_id, "amount": post_balance, "surrogate_name": surrogate_name, "time": tras_time, "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce", "organisation_id": tsp})
            wallet_balance = context.nko_url.add_credit(post_data)
            message = assert_error_message('Не удалось пополнить кошелёк', wallet_balance)
            assert wallet_balance.status_code == 200, message
            wallet_balance = json.loads(wallet_balance.text)
        elif balance < int(balance_in_wallet):
            get_balance = (balance_in_wallet) - balance
            id_tran_debit = random.randint(1000000000000000,9999999999999999)
            time_debit = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+03:00")
            post_data = json.dumps({"id": id_tran_debit, "amount": get_balance, "surrogate_name": surrogate_name, "region_id": "39", "app_id": "46f2f45b-8ca4-4517-a03d-d73d88d3bbce", "organisation_id": tsp, "time": time_debit})
            wallet_spisenie = context.nko_url.wallet_write(post_data)
            message = assert_error_message('Не удалось списать средства с кошелька', wallet_spisenie)
            assert wallet_spisenie.status_code == 200, message
            wallet_spisenie = json.loads(wallet_spisenie.text)


@When('Отправим {option} запрос v2 на резервирование денежных средств с {node} {status}')
def step_impl(context, option, node, status):
    if node == 'непереданным' and status == 'магазином':
        merchant_auth = '0'
    else:
        merchant_auth = context.sh_code
    if node == 'непереданной' and status == 'кассой':
        terminal_auth = '0'
    else:
        terminal_auth = context.term_code
    if node == 'непереданной' and status == 'соц.программой':
        soc_prgm = '0'
    elif node == 'отсутствующей' and status == 'соц.программой':
        soc_prgm = None
    else:
        soc_prgm = context.social_program_code
    card = context.hash_pan
    batch_id = str(uuid4())
    if node == 'повторным' and status == 'кодом':
        batch_id = context.orig_reserv
    else:
        context.orig_reserv = batch_id
    batch_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
    context.batch_time = batch_time
    product = context.product_in_catalog
    product = random.choice(context.product_in_catalog)
    product_code = product['code']
    if node == 'непереданным' and status == 'товаром':
        prod_cod = 0
    else:
        prod_cod = product_code
    context.product = product
    post_data = json.dumps({"merchantId": merchant_auth, "terminalId": terminal_auth, "socialProgramId": soc_prgm, "paymentType": 0, "card": {"pan": card}, "batch": {"id": batch_id, "dateTime": batch_time, "amount":product['price']}, "products": [{"type": 0, "code": prod_cod, "name": product['name'], "unit": "PIEC", "quantity": str(float(product['price'])),"price": str(float(product['price'])), "amount": str(float(product['price']))}]})
    auth_reserve = context.terminal_v2_api.batch_auth(context.auth_key, post_data)
    if option == 'успешный':
        message = assert_error_message('Не удалось отправить запрос резервирования', auth_reserve)
        assert auth_reserve.status_code == 200, message
    else:
        message = assert_error_message('Удалось отправить запрос резервирования, ожидалась ошибка', auth_reserve)
        assert auth_reserve.status_code != 200, message
    auth_reserve = json.loads(auth_reserve.text)
    context.reserve_mes = auth_reserve
    context.auth_code = auth_reserve['authCode']

@Then('В теле ответа на запрос v2 резервирования получим {option} {code}')
def step_impl(context, option, code):
    response_code = context.reserve_mes['responseCode']
    response_message = context.reserve_mes['responseMessage']
    if option == 'успех':
        assert response_code == 0, 'Резервирование прошло с кодом {0} и текстом: {1}'.format(response_code, response_message)
    else:
        assert response_code == int(code), 'Резервирование прошло с ошибкой {0} и текстом: ошибки {1}'.format(response_code, response_message)

@When('Отправим {option} запрос v2 на списание денежных средств с {node} {status}')
def step_impl(context, option, node, status):
    if node == 'непереданным' and status == 'магазином':
        merchant_trans = 0
    else:
        merchant_trans = context.sh_code
    if node == 'отсутствующей' and status == 'кассой':
        terminal_trans = 0
    else:
        terminal_trans = context.term_code
    orig_res = context.orig_reserv
    if node == 'непереданным' and status == 'кодом':
        authCode = '0'
    else:
        authCode = context.auth_code
    prod = context.product
    prct = prod['price']
    trans_id = str(uuid4())
    if node == 'повторным' and status == 'отправлением':
        trans_id = context.trans_batch
    else:
        context.trans_batch = trans_id
    trans_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
    context.trans_time = trans_date
    post_data = json.dumps({"merchantId": merchant_trans, "terminalId": terminal_trans, "authCode": authCode, "authBatchId": orig_res, "batch": {"id": trans_id, "dateTime": trans_date, "amount": str(float(prct))}})
    transfer = context.terminal_v2_api.batch_transfer(context.auth_key, post_data)
    if option == 'успешный':
        message = assert_error_message('Не удалось отправить запрос списания', transfer)
        assert transfer.status_code == 200, message
    else:
        message = assert_error_message('Удалось отправить запрос списания, ожидалась ошибка', transfer)
        assert transfer.status_code != 200, message
    transfer = json.loads(transfer.text)
    context.transfer_data = transfer

@Then('В теле ответа на списание по v2 получим {option} {code}')
def step_impl(context, option, code):
    trans_code = context.transfer_data['responseCode']
    trans_message = context.transfer_data['responseMessage']
    if option == 'успех':
        assert trans_code == 0, 'Списание прошло с кодом {0} и текстом: {1}'.format(trans_code, trans_message)
    else:
        assert trans_code == int(code), 'Списание не прошло, код ошибки {0}, текстом: {1}'.format(trans_code, trans_message)

@When('Отправим {option} запрос v2 на отмену ранее зарезервированных средств')
def step_impl(context, option):
    merchant_cancell = context.sh_code
    terminal_cancell = context.term_code
    card_hash = context.hash_pan
    cancell_batch = str(uuid4())
    auth_c = context.auth_code
    date_cancell = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
    prct = context.product
    product = prct['price']
    time_res = context.batch_time
    orig_resrv = context.orig_reserv
    post_data = json.dumps({"merchantId": merchant_cancell, "terminalId": terminal_cancell, "authCode": auth_c, "card": {"pan": card_hash}, "batch": {"id": cancell_batch, "dateTime": date_cancell, "amount": product}, "originalBatch": {"id": orig_resrv, "dateTime": time_res, "merchantId": merchant_cancell, "terminalId": terminal_cancell}})
    cancell = context.terminal_v2_api.batch_cancell(context.auth_key, post_data)
    if option == 'успешный':
        message = assert_error_message('Не удалось отправить запрос отмены резерва', cancell)
        assert cancell.status_code == 200, message
    else:
        message = assert_error_message('Удалось отправить запрос отмены резерва, ожидалась ошибка', cancell)
        assert cancell.status_code != 200, message
    cancell = json.loads(cancell.text)
    context.cancelletion = cancell

@Then('В теле ответа на отмену v2 ранее зарезервированных средств получим {option} ответ')
def step_impl(context, option):
    cancell_batch_code = context.cancelletion['responseCode']
    cancell_batch_message = context.cancelletion['responseMessage']
    if option == 'успешный':
        assert cancell_batch_code == 0, 'Отмена не прошла, код ошибки {0}, текст ошибки {1}'.format(cancell_batch_code, cancell_batch_message)
    else:
        assert cancell_batch_code != 0, 'Операция отмена не прошла, код ошибки {0}, текст ошибки {1}'.format(cancell_batch_code, cancell_batch_message)

@When('Отправим {option} запрос v2 на возврат денежных средств')
def step_impl(context, option):
    merchant_refund = context.sh_code
    terminal_refund = context.term_code
    soc_prg = context.social_program_code
    card_hash_refund = context.hash_pan
    refund_batch = str(uuid4())
    date_refund = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
    prct = context.product
    orig_trans = context.trans_batch
    orig_time_trans = context.trans_time
    post_data = json.dumps({"merchantId": merchant_refund, "terminalId": terminal_refund, "socialProgramId": soc_prg, "card": {"pan": card_hash_refund}, "batch": {"id": refund_batch, "dateTime": date_refund, "amount": prct['price']}, "originalBatch": {"id": orig_trans, "dateTime": orig_time_trans, "merchantId": merchant_refund, "terminalId":terminal_refund}, "products": [{"type": 0, "code": prct['code'], "name": prct['name'], "unit": "PIEC", "quantity": str(float(prct['price'])), "price": str(float(prct['price'])), "amount": str(float(prct['price']))}]})
    refund = context.terminal_v2_api.batch_refund(context.auth_key, post_data)
    if option == 'успешный':
        message = assert_error_message('Не удалось отправить запрос возврата ДС', refund)
        assert refund.status_code == 200, message
    else:
        message = assert_error_message('Удалось отправить запрос возврата ДС, ожидалась ошибка', refund)
        assert refund.status_code != 200, message
    refund = json.loads(refund.text)
    context.refund_trans = refund

@Then('В теле ответа на возврат v2 денежных средств получим {option} операции')
def step_impl(context,option):
    refund_code = context.refund_trans['responseCode']
    refund_message = context.refund_trans['responseMessage']
    if option == 'успех':
        assert refund_code == 0, 'Операция возврат не прошла, код ошибки {0}, текст ошибки {1}'.format(refund_code, refund_message)
    else:
        assert refund_code != 0, 'Операция возврат не прошла, код ошибки {0}, текст ошибки {1}'.format(refund_code, refund_message)

@When('Отправка запроса v2 на получение социальных программ')
def step_impl(context):
    ref_soc_prog = context.terminal_v2_api.reference_sog_prog(context.auth_key)
    message = assert_error_message('Не удалось отправить запрос получения соц.программ', ref_soc_prog)
    assert ref_soc_prog.status_code == 200, message
    ref_soc_prog = json.loads(ref_soc_prog.text)
    context.ref_soc = ref_soc_prog

@Then('Проверим что полученный список соц программ не пуст')
def step_impl(context):
    ref_soc_code = context.ref_soc['responseCode']
    ref_soc_message = context.ref_soc['responseMessage']
    if ref_soc_code == 0:
        assert ref_soc_message == 'Успешно', 'Запрос не прошел, код ошибки {0}, с текстом: {1}'.format(ref_soc_code, ref_soc_message)
    else:
        assert ref_soc_message != 'Успешно', 'Запрос не прошел, код ошибки {0}, с текстом: {1}'.format(ref_soc_code, ref_soc_message)

@When('Отправка запроса v2 на получение списка категорий предмета расчета')
def step_impl(context):
    ref_prod = context.social_program_code
    ref_prct_cat = context.terminal_v2_api.reference_prod_cat(context.auth_key, ref_prod)
    message = assert_error_message('Не удалось отправить запрос получения списка категорий предмета расчета', ref_prct_cat)
    assert ref_prct_cat.status_code == 200, message
    ref_prct_cat = json.loads(ref_prct_cat.text)
    context.reference = ref_prct_cat

@Then('Проверим что список категорий предмета расчета не пуст')
def step_impl(context):
    ref_prct_code = context.reference['responseCode']
    ref_prct_message = context.reference['responseMessage']
    if ref_prct_code == 0:
        assert ref_prct_message == 'Успешно', 'Запрос на список категорий не прошел, код ошибки {0}, текст {1}'.format(ref_prct_code, ref_prct_message)
    else:
        assert ref_prct_message != 'Успешно', 'Запрос на список категорий не прошел, код ошибки {0}, текст {1}'.format(ref_prct_code, ref_prct_message)

@When('Отправка запроса v2 на импорт категорий')
def step_impl(context):
    soc_prog = context.social_program_code
    code = ''.join(random.choice('1234567890') for i in range (4))
    external_code = ''.join(random.choice('1234567890') for i in range(8))
    external_name = 'Тестовый товар' + external_code
    post_data = json.dumps({"socialProgramId": soc_prog, "productCategories": [{"code": code, "externalCode": external_code, "externalName": external_name}]})
    import_cat = context.terminal_v2_api.import_product_categories(post_data, context.auth_key)
    message = assert_error_message('Не удалось отправить запрос импорта категорий', import_cat)
    assert import_cat.status_code == 200, message
    import_cat = json.loads(import_cat.text)
    context.import_categories = import_cat

@When('Отправка запроса v2 на импорт предметов расчета')
def step_impl(context):
    social_pr = context.social_program_code
    type_id = 1
    external_code = ''.join(random.choice('1234567890') for i in range(8))
    external_name = 'Тестовый предмет расчета' + external_code
    external_cat_code = ''.join(random.choice('1234567890') for i in range(8))
    external_cat_name = 'Тест' + external_cat_code
    category_code = 1
    post_data = json.dumps({"socialProgramId": social_pr, "products": [{"typeId": type_id, "externalCode": external_code, "externalName": external_name, "externalCategoryCode": external_cat_code, "externalCategoryName": external_cat_name, "categoryCode": category_code}]})
    import_prod = context.terminal_v2_api.import_products(post_data, context.auth_key)
    message = assert_error_message('Не удалось отправить запрос импорта предметов расчета', import_prod)
    assert import_prod.status_code == 200, message
    import_prod = json.loads(import_prod.text)
    context.import_produtcs = import_prod

@When('Отправка запроса v2 на импорт терминалов')
def step_impl(context):
    merchant = context.sh_code
    id_id = ''.join(random.choice('1234567890') for i in range (4))
    name = 'Тестовый терминал' + id_id
    post_data = json.dumps({"terminals": [{"merchantId": merchant, "id": id_id, "name": name}]})
    import_term = context.terminal_v2_api.import_terminals(post_data, context.auth_key)
    message = assert_error_message('Не удалось отправить запрос импорта терминалов', import_term)
    assert import_term.status_code == 200, message
    import_term = json.loads(import_term.text)
    context.import_terminal = import_term

@Then('Проверим полученный {node} ответ по импорту категорий')
def step_impl(context, node):
    import_res_code = context.import_categories['responseCode']
    import_res_mes = context.import_categories['responseMessage']
    if node == 'успешный':
        assert import_res_code == 0, 'Импорт не прошел с кодом {0} и текстом: {1}'.format(import_res_code, import_res_mes)
    else:
        assert import_res_code != 0, 'Импорт прошел с кодом {0} и текстом: {1}'.format(import_res_code, import_res_mes)

@Then('Проверим полученный {node} ответ по импорту предметов расчета')
def step_impl(context, node):
    import_res_code = context.import_produtcs['responseCode']
    import_res_mes = context.import_produtcs['responseMessage']
    if node == 'успешный':
        assert import_res_code == 0, 'Импорт не прошел с кодом {0} и текстом: {1}'.format(import_res_code, import_res_mes)
    else:
        assert import_res_code != 0, 'Импорт прошел с кодом {0} и текстом: {1}'.format(import_res_code, import_res_mes)

@Then('Проверим полученный {node} ответ по импорту терминалов')
def step_impl(context, node):
    import_res_code = context.import_terminal['responseCode']
    import_res_mes = context.import_terminal['responseMessage']
    if node == 'успешный':
        assert import_res_code == 0, 'Импорт не прошел с кодом {0} и текстом: {1}'.format(import_res_code, import_res_mes)
    else:
        assert import_res_code != 0, 'Импорт прошел с кодом {0} и текстом: {1}'.format(import_res_code, import_res_mes)

