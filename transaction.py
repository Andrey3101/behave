from datetime import datetime
import json
import random
from uuid import uuid4
from fixtures import assert_error_message

class AcceptorAuthorisationData():
    def __init__(self):
        self.datetime = None
        self.InitgPty = None
        self.Mrchnt = None
        self.POI_id = None
        self.PAN = None
        self.XpryDt = None
        self.AddtlCardData = None
        self.TxDtTm = None
        self.TxRef = None
        self.TxDtls = None

class AcceptorBatchTransferData():
    def __init__(self):
        self.datetime = None
        self.InitgPty = None
        self.Mrchnt = None
        self.POI_id = None
        self.PAN = None
        self.XpryDt = None
        self.AddtlCardData = None
        self.TxDtTm = None
        self.TxRef = None
        self.TxDtls = None
        self.Nm = None
        self.code = None

@Given('Запрос на резервирование "auth_request"')
def step_impl(context):
    context.AcceptorAuthorisationData = AcceptorAuthorisationData()
    context.AcceptorAuthorisationData.TxDtTm = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
    context.AcceptorAuthorisationData.TxRef = str(uuid4())
    Ccy = context.social_program_code
    context.AcceptorAuthorisationData.InitgPty = context.merch_code
    context.AcceptorAuthorisationData.Mrchnt = context.sh_code
    context.AcceptorAuthorisationData.POI_id = context.term_code
    product = context.product_in_catalog
    context.AcceptorAuthorisationData.PAN = context.hash_pan
    product = random.choice(context.product_in_catalog)# этот метод выбора продукта изменим, пока что так оставим
    context.prodct_data = product
    context.AcceptorAuthorisationData.TxDtls = ({'Ccy': Ccy, "TtlAmt": product['price'],"Pdct": [{"PdctCd": product['code'], "UnitOfMeasr": "PIEC", "PdctQty": float(1), "UnitPric": str(float(product['price'])), "PdctAmt": str(float(product['price']))}]})

@When('Запрос на резервирование  "auth_request"  отправлен в терминальную службу')
def step_impl(context):
    context.reservation_body = context.gen.AcceptorAuthorisationRequest(context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.InitgPty, context.AcceptorAuthorisationData.Mrchnt, context.AcceptorAuthorisationData.POI_id, '0000000000000000', '2023-09', context.AcceptorAuthorisationData.PAN, context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.TxRef, context.AcceptorAuthorisationData.TxDtls).decode('UTF-8')
    context.acceptor_response = context.terminal_api.add_reserve(context.reservation_body)
    assert context.acceptor_response.status_code == 200, 'Ошибка резерва, в ответ получили {0} с тектом ошибки {1}'.format(context.acceptor_response.status_code, context.acceptor_response.text)
    context.AcceptorAuthorisationData.auth_code_reserve = context.gen.get_text_node(context.acceptor_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01', 'AuthstnCd')
    context.AcceptorAuthorisationData.total_amt = context.gen.get_text_node(context.acceptor_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01', 'TtlAmt')

@Given('Запрос на списание "bt_request" с теми же реквизитами покупки, что и запрос на резервирование "auth_request", и кодом авторизации "auth_code" из ответа на резервирование "auth_response"')
def step_impl(context):
    context.AcceptorBatchTransferData = AcceptorBatchTransferData()
    context.AcceptorBatchTransferData.TxDtTm = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+ '+03:00'
    context.AcceptorBatchTransferData.TxRef = str(uuid4())
    context.AcceptorBatchTransferData.InitgPty = context.merch_code
    context.AcceptorBatchTransferData.Mrchnt = context.sh_code
    context.AcceptorBatchTransferData.PAN = context.hash_pan
    context.AcceptorBatchTransferData.POI_id = context.term_code
    context.AcceptorBatchTransferData.TxDtls = ({'Ccy': context.social_program_code, 'TtlAmt': str(float(context.AcceptorAuthorisationData.total_amt))})

@When('Запрос на списание "bt_request" отправлен в терминальную службу')
def step_impl(context):
    auth_req = {'CardData': str(context.AcceptorBatchTransferData.PAN), 'TtlAmt': str(float(context.AcceptorAuthorisationData.total_amt)) ,'AuthstnCd': context.AcceptorAuthorisationData.auth_code_reserve, 'idref': context.AcceptorAuthorisationData.TxRef, 'TxDtTm': context.AcceptorAuthorisationData.TxDtTm}
    context.tran_batch_body = [context.AcceptorBatchTransferData.TxDtTm, context.AcceptorBatchTransferData.InitgPty, context.AcceptorBatchTransferData.Mrchnt, context.AcceptorBatchTransferData.POI_id, '0000000000000000', '2023-09', auth_req['CardData'], auth_req['TxDtTm'], auth_req['idref'], context.AcceptorBatchTransferData.TxDtls, context.AcceptorBatchTransferData.TxRef, auth_req['AuthstnCd']]
    wallet_transaction = context.gen.AcceptorBatchTransferRequest(context.AcceptorBatchTransferData.TxDtTm, context.AcceptorBatchTransferData.InitgPty, context.AcceptorBatchTransferData.Mrchnt, context.AcceptorBatchTransferData.POI_id, '0000000000000000', '2023-09', auth_req['CardData'], auth_req['TxDtTm'], auth_req['idref'], context.AcceptorBatchTransferData.TxDtls, context.AcceptorBatchTransferData.TxRef, auth_req['AuthstnCd']).decode('utf-8')
    context.wallet_response = context.terminal_api.add_debit(wallet_transaction)
    context.reservation_body = context.gen.AcceptorBatchTransferRequest(context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.InitgPty, context.AcceptorAuthorisationData.Mrchnt, context.AcceptorAuthorisationData.POI_id, '0000000000000000', '2023-09', context.AcceptorAuthorisationData.PAN, context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.TxRef, context.AcceptorAuthorisationData.TxDtls, context.AcceptorBatchTransferData.TxRef, context.AcceptorAuthorisationData.auth_code_reserve).decode('UTF-8')
    context.acceptor_response = context.terminal_api.add_debit(context.reservation_body)

@When('Значение {status} "{code}" из запроса "{action}" {condition} {articul} {SP}')
def step_impl(context, status, code, action, condition, articul, SP):
    if action == 'резервирования':
        data = context.AcceptorAuthorisationData
        if status == 'товара' and code == 'social_product':
            data.TxDtls['Pdct'][0]['PdctCd'] = '0'
        else:
            res_b = context.prodct_data
            data.TxDtls['Pdct'][0]['PdctCd'] = res_b['code']
    elif action == 'bt_request':
        data = context.AcceptorBatchTransferData
    if status == 'кода' and code == 'r_auth_code':
        context.AcceptorAuthorisationData.auth_code_reserve = '0'
    if status == 'предприятия' and code == 'organisation_id':
        data.InitgPty = '0'
    else:
        data.InitgPty = context.merch_code
    if status == 'соц.программы' and code == 'social_program':
        data.TxDtls['Ccy'] = '0'
    else:
        data.TxDtls['Ccy'] = context.social_program_code
    if status == 'магазина' and code == 'merchant_id':
        data.Mrchnt = '0'
    else:
        data.Mrchnt = context.sh_code
    if status == 'кассы' and code == 'terminal_id':
        data.POI_id = '0'
    else:
        data.POI_id = context.term_code
    if status == 'блока' and code == 'merchant_id':
        data.Mrchnt = None
    else:
        data.Mrchnt = context.sh_code
    if action == 'резервирования':
        context.AcceptorAuthorisationData = data
    elif action == 'bt_request':
        context.AcceptorBatchTransferData  = data

@When('Значение суммы резервирования "auth_amount" из запроса больше баланса на счету')
def step_impl(context):
    r = context.AcceptorAuthorisationData.TxDtls['TtlAmt']
    if r > 0:
        reserved = 100000
        r  = reserved
        context.AcceptorAuthorisationData.TxDtls['TtlAmt'] = r
        reser_b = context.gen.AcceptorAuthorisationRequest(context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.InitgPty, context.AcceptorAuthorisationData.Mrchnt, context.AcceptorAuthorisationData.POI_id, '0000000000000000', '2023-09', context.AcceptorAuthorisationData.PAN, context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.TxRef, context.AcceptorAuthorisationData.TxDtls).decode('UTF-8')
        context.acceptor_response = context.terminal_api.add_reserve(reser_b)
        assert context.acceptor_response.status_code == 200, 'Ошибка резерва, в ответ получили {0} с тектом ошибки {1}'.format(context.acceptor_response.status_code, context.acceptor_response.text)
        context.AcceptorAuthorisationData.auth_code_reserve = context.gen.get_text_node(context.acceptor_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01', 'AuthstnCd')
    else:
        reser_b = context.gen.AcceptorAuthorisationRequest(context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.InitgPty, context.AcceptorAuthorisationData.Mrchnt, context.AcceptorAuthorisationData.POI_id, '0000000000000000', '2023-09', context.AcceptorAuthorisationData.PAN, context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.TxRef, context.AcceptorAuthorisationData.TxDtls).decode('UTF-8')
        context.acceptor_response = context.terminal_api.add_reserve(reser_b)
        assert context.acceptor_response.status_code == 200, 'Ошибка резерва, в ответ получили {0} с тектом ошибки {1}'.format(context.acceptor_response.status_code, context.acceptor_response.text)
        context.AcceptorAuthorisationData.auth_code_reserve = context.gen.get_text_node(context.acceptor_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01', 'AuthstnCd')

@When('Значение карты "panhash" из запроса отсутствует в НКО')
def step_impl(context):
    reser_b = context.gen.AcceptorAuthorisationRequest(context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.InitgPty, context.AcceptorAuthorisationData.Mrchnt, context.AcceptorAuthorisationData.POI_id, '0000000000000000', '2023-09', context.AcceptorAuthorisationData.PAN, context.AcceptorAuthorisationData.TxDtTm, context.AcceptorAuthorisationData.TxRef, context.AcceptorAuthorisationData.TxDtls).decode('UTF-8')
    context.acceptor_response = context.terminal_api.add_reserve(reser_b)
    assert context.acceptor_response.status_code == 200, 'Ошибка резерва, в ответ получили {0} с тектом ошибки {1}'.format(context.acceptor_response.status_code, context.acceptor_response.text)
    context.auth_code_reserve = context.gen.get_text_node(context.acceptor_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01', 'AuthstnCd')

@Then('Получен ответ "{status}" на запрос {type_send}')
def step_impl(context, status, type_send):
    if type_send == 'резервирования':
        namespace = 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01'
    elif type_send == 'списания':
        namespace = 'urn:iso:std:iso:20022:tech:xsd:caaa.012.001.01'
    ls = status = status.split('/')
    code = ls[0]
    if code == 'APPR':
        get_rspn = context.gen.get_text_node(context.acceptor_response.text, namespace, 'Rspn')
        get_code = context.gen.get_text_node(context.acceptor_response.text, namespace, 'RspnRsn')
        if ls == 'DECL':
            assert 'DECL' == get_rspn, 'Резерв не прошел, код ошибки {0} от соц.процессинга на запрос резервирования'.format(get_code)
        else:
            assert 'APPR' == get_rspn, 'Резерв не прошел, код ошибки {0} от соц.процессинга на запрос резервирования'.format(get_code)
    if code == 'DECL':
        resp = ls[1]
        get_rspn = context.gen.get_text_node(context.acceptor_response.text, namespace, 'Rspn')
        get_code = context.gen.get_text_node(context.acceptor_response.text, namespace, 'RspnRsn')
        if get_rspn == 'DECL':
            assert code == get_rspn, 'Резерв не прошел, код ошибки {0} от соц.процессинга на запрос резервирования'.format(get_code)
            assert resp == get_code, 'Полученный код {0} не совпал с ожидаемым {1}'.format(get_code, resp)
        else:
            assert 'APPR' == get_rspn, 'Резерв не прошел, код ошибки {0} от соц.процессинга на запрос резервирования'.format(get_code)

@When('{option} отправим запрос на списание денежных средств с {status} {datas}')
def step_impl(context, option, status, datas):
    TxDtTm_batch =  datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
    TxRef_batch = str(uuid4())
    context.TxRef_bat = TxRef_batch
    context.TxDt_batch = TxDtTm_batch
    if status == 'непереданным' and datas == 'тсп':
        InitgPty_batch = '0'
    else:
        InitgPty_batch = context.merch_code
    Ccy = context.social_program_code
    if status == 'непереданным' and datas == 'магазином':
        Mrchnt_batch = '0'
    else:
        Mrchnt_batch = context.sh_code
    if status == 'непереданной' and datas == 'картой':
        hash_pan = 0
    else:
        hash_pan = context.hash_pan
    if status == 'отсутствующей' and datas == 'кассой':
        POI_id_batch = '0'
    else:
        POI_id_batch = context.term_code
    if status == 'непереданным' and datas == 'кодом':
        auth_code = None
    elif status == 'неправильным' and datas == 'кодом':
        auth_code = ''.join(random.choice('1234567890') for i in range (8))
    else:
        auth_code = context.auth_code_reserve
    product_total_amt = context.total_amt
    reserve_id = context.orig_reserv
    date_reserve_id = context.date_reserve
    txDtls = ({'Ccy': Ccy, 'TtlAmt': str(float(product_total_amt))})
    auth_req = {'CardData': str(hash_pan), 'TtlAmt': str(float(product_total_amt)) ,'AuthstnCd': auth_code, 'idref': reserve_id, 'TxDtTm': date_reserve_id}
    wallet_transaction = context.gen.AcceptorBatchTransferRequest(TxDtTm_batch, InitgPty_batch, Mrchnt_batch, POI_id_batch, '0000000000000000', '2023-09', auth_req['CardData'], auth_req['TxDtTm'], auth_req['idref'], txDtls, TxRef_batch, auth_req['AuthstnCd']).decode('utf-8')
    context.wallet_response = context.terminal_api.add_debit(wallet_transaction)
    if option == 'Успешно':
        assert context.wallet_response.status_code == 200, 'Ошибка списания, в ответ получили {0} с тектом ошибки {1}'.format(context.wallet_response.status_code, context.wallet_response.text)
    elif option == 'Неуспешно':
        assert context.wallet_response.status_code != 200, 'Не получили ошибку списания, в ответ получили {0} с тектом {1}'.format(context.wallet_response.status_code, context.wallet_response.text)
    pass

@Then('В теле ответа на запрос списания получим {option} {node}')
def step_impl(context, option, node):
   get_rspn = context.gen.get_text_node(context.wallet_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.012.001.01', 'Rspn')
   get_code = context.gen.get_text_node(context.wallet_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.012.001.01', 'RspnRsn')
   if option == 'ошибку':
       if node == ['304','309', '310', '331','386', '387', '90001']:
           tsp_id = context.merch_id
           shop_id = context.shop_id
           POI_id = context.terminal_id
           terminal_transaction_batch_id = context.orig_reserv
           post_data = json.dumps({"column": "TerminalDateUtc", "direction": 2, "page": 1, "pageSize": 1000, "terminalId": str(terminal_transaction_batch_id)})
           transaction_search = context.management.post_transaction_batch(context.management_super_token, post_data)
           message = assert_error_message('Не удалось отправить запрос поиска транзакции в management', transaction_search)
           assert transaction_search.status_code == 200, message
#            transaction_search = json.loads(transaction_search.text)
           for trasaction_search_data in transaction_search['data']:
               if trasaction_search_data['statusId'] == 4 and trasaction_search_data['terminalId'] == POI_id and trasaction_search_data['shopId'] == shop_id and trasaction_search_data['merchantId'] == tsp_id:
                   get_transaction = trasaction_search_data['id']
                   get_transaction_batch = context.management.get_transaction_batch(context.management_super_token, get_transaction)
                   message = assert_error_message('Не удалось отправить запрос информации транзакции в management', get_transaction_batch)
                   assert get_transaction_batch.status_code == 200, message
                   get_transaction_batch = json.loads(get_transaction_batch.text)
                   assert get_transaction_batch['code'] == node, 'Ожидался у транзакции {2} код {0} по факту {1}'.format(node, get_transaction_batch['code'], trasaction_search_data['id'])
   else:
       assert 'APPR' == get_rspn, 'Операция списания не прошла, код ошибки {0} от соц.процессинга на запрос списания'.format(get_code)
   pass
   

#@When('{option} отправим запрос на отмену зарезервированных денежных средств с {status} {datas}')
#def step_impl(context, option, status, datas):
#    TxDtTm_cancell = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
#    TxRef_cancell = str(uuid4())
#    InitgPty_cancell = context.merch_code
#    Ccy = context.social_program_code
#    Mrchnt_cancell = context.sh_code
#    if status == 'непереданным' and datas == 'терминалом':
#        POI_id_cancell = '0'
#    else:
#        POI_id_cancell = context.term_code
#    if status == 'непереданным' and datas == 'кодом':
#        auth_code = '0'
#    else:
#        auth_code = context.auth_code_reserve
#    prodct_amt = context.total_amt
#    reservation = context.orig_reserv
#    date_reserve = context.date_reserve
#    auth_req = {'CardData': context.hash_pan, 'TtlAmt': str(float(prodct_amt)), 'AuthstnCd': auth_code, 'idref': reservation, 'TxDtTm': date_reserve}
#    cancell_transaction = context.gen.AcceptorCancellationRequest(InitgPty_cancell, Mrchnt_cancell, POI_id_cancell, '0000000000000000', '2023-09', auth_req['CardData'], TxDtTm_cancell, TxRef_cancell, auth_req['idref'], auth_req['TxDtTm'], auth_code, str(Ccy), auth_req['TtlAmt']).decode('utf-8')
#    context.cancell_responce = context.terminal_api.add_cancell(cancell_transaction)
#    if option == 'Успешно':
#        assert context.cancell_responce.status_code == 200, 'Ошибка отмены зарезервированной транзакции, в ответ получили {0} с текстом: {1}'.format(context.cancell_responce.status_code, context.cancell_responce.text)
#    elif option == 'Неуспешно':
#        assert context.cancell_responce != 200 , 'Не получили ошибку отмены зарезервированной транзакции, в ответе получили {0} с текстом: {1}'.format(context.cancell_responce.status_code, context.cancell_responce.text)
#    pass

#@Then('В теле ответа на запрос получим {status} {code}')
#def step_impl(context, status, code):
#    gen_rspn = context.gen.get_text_node(context.cancell_responce.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.006.001.01', 'Rspn')
#    get_code = context.gen.get_text_node(context.cancell_responce.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.006.001.01', 'RspnRsn')
#    if status == 'ошибку':
#        assert 'DECL' == gen_rspn, 'Отмена не прошела, код ошибки {0} от соц.процессинга на запрос отмены'.format(get_code)
#        
#        assert code == get_code, 'Полученный код {0} не совпал с ожидаемым {1}'.format(get_code, code)
#    else:
#        assert 'APPR' == gen_rspn, 'Отмена не прошела, код ошибки {0} от соц.процессинга на запрос отмены'.format(get_code)
#    pass

#@When('{option} отправим запрос на возврат денежных средств с {status} {datas}')
#def step_impl(context, option, status, datas):
#    TxDtTm_refund = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
#    TxRef_refund = str(uuid4())
#    if status == 'непереданным' and datas == 'тсп':
#        InitgPty_refund = None
#    else:
#        InitgPty_refund = context.merch_code
#    Mrchnt_refund = context.sh_code
#    POI_id_refund = context.term_code
#    Ccy = context.social_program_code
#    TtlAmt_refund = context.total_amt
#    prod = context.prodct_data
#    prod_cd = prod['code']
#    prod_qt = str(float(1))
#    prod_unit = str(float(prod['price']))
#    prod_amt = str(float(prod['price']))
    # orig_batch = context.TxRef_bat
#    orig_batch = context.orig_reserv
#    orig_Dt_batch = context.TxDt_batch
#    if status == 'непереданной' and datas == 'картой':
#        card_hash = 0
#    else:
#        card_hash = context.hash_pan
#    auth_req = {'CardData': str(card_hash)}
#    refund_transaction = context.gen.AcceptorRefundRequest(InitgPty_refund, Mrchnt_refund, POI_id_refund, '0000000000000000', '2023/09', auth_req['CardData'], TxDtTm_refund, TxRef_refund, orig_Dt_batch, orig_batch, Ccy, TtlAmt_refund, prod_cd, prod_qt, prod_unit, prod_amt).decode('utf-8')
#    context.refund_response = context.terminal_api.add_refund(refund_transaction)
#    if option == 'Успешно':
#        assert context.refund_response.status_code == 200, 'Ошибка транзакции возврата ДС, в ответ получили {0}, с тестом ошибки {1}'.format(context.refund_response.status_code, context.refund_response.text)
#    elif option == 'Неуспешно':
#        assert context.refund_response.status_code != 200, 'Не получили ошибки возврата ДС, в ответе получили {0}, с текстом: {1}'.format(context.refund_response.status_code, context.refund_response.text)
#    pass

#@Then('В теле ответа на запрос возврата получим {status} {Node}')
#def step_impl(context, status, Node):
#    get_rspn = context.gen.get_text_node(context.refund_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.017.001.01', 'Rspn')
#    get_code = context.gen.get_text_node(context.refund_response.text, 'urn:iso:std:iso:20022:tech:xsd:caaa.017.001.01', 'RspnRsn')
#    if status == 'ошибку':
#        assert 'DECL' == get_rspn, 'Возврат не прошел, код ошибки {0} от соц.процессинга на запрос возврата'.format(get_code)
        
        # assert code == get_code, 'Полученный код {0} не совпал с ожидаемым {1}'.format(get_code, code)
#    else:
#        assert 'APPR' == get_rspn, 'Возврат не прошел, код ошибки {0} от соц.процессинга на запрос возврата'.format(get_code)
#    pass