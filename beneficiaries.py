from gen.inn import inn as gen_inn
from gen.snils import snils as gen_snils
from datetime import datetime, timedelta
from time import sleep
from fixtures import assert_error_message
import random
import json
from gen.gen_credit_card_number import credit_card_number


@Given('Подготовлен тестовый xlsx файл потребителей с {counts} {string}')
def step_impl(context, counts, string):
    context.import_data_beneficiarie = {'sheets':[]}
    sheet = {'data': []}
    sheet['name'] = 'Import beneficiaries'
    sheet['header'] = ['СНИЛС', 'ИНН', 'Фамилия', 'Имя', 'Отчество', 'Дата_рождения', 'Категории_льгот', 'Дата_регистрации']
    data = []
    for i in range(int(counts)):
        inn = gen_inn(12)
        snils = gen_snils()
        burthday = (datetime.now()-timedelta(days=random.randint(18,99)*365)).strftime('%d.%m.%Y')
        code_name = datetime.now().strftime('%S%f')[:-3]
        date_export = (datetime.now()).strftime('%d.%m.%Y')
        sheet['data'].append([snils, inn, 'Behave'+code_name, 'Test'+code_name, 'Тестович'+code_name, burthday, context.benefit_type_code, date_export])
    context.import_data_beneficiarie['sheets'].append(sheet)
    for x in range(3):
        try:
            context.import_excel_beneficiaries = context.exel.generate_excel(context.import_data_beneficiarie)
            break
        except:
            context.behave_log.info('Генерация xlsx файла прошла с ошибкой, будет повторная попытка №{0}'.format(x+2))
            sleep(2)

@When('"{status}" импортируем файл потребителей')
def step_impl(context, status):
    assert context.import_excel_beneficiaries, 'Файл не был сгенерирован автотестом, проверьте шаг "Дано"(Given) Подготовлен тестовый xlsx файл потребителей с 1 или более записью'.format()
    create_benefitciaries = context.management.import_beneficiaries(context.management_super_token, context.import_excel_beneficiaries, context.soc_program)
    if status == 'Успешно':
        message = assert_error_message('Файл успешно не импортирован', create_benefitciaries)
        assert create_benefitciaries.status_code == 200, message
        response = json.loads(create_benefitciaries.text)
        assert response['errorDataCount'] == 0, 'Импорт содержит {0} ошибку или ошибок, ожидался импорт без ошибок'.format(response['errorDataCount'])
        context.status_import = response


@When('{status} создадим сотрудника')
def step_impl(context,status):
    code = ''.join(random.choice('1234567890') for i in range(6))
    f_name = 'Test' + code
    l_name = 'l_Test' + code
    p_code = ''.join(random.choice('1234567890') for i in range(5))
    type_id = 2
    executive_ids = context.executive_id
    benfit_t_id = context.benefit_id
    social_prog = context.soc_program
    post_data = json.dumps({"typeId": type_id, "firstName": f_name, "lastName": l_name, "benefitTypeIds": [benfit_t_id], "divisionCode": code, "executiveAuthorityIds": [executive_ids], "personalNumber": p_code, "socialProgramIds": [social_prog], "enabled": True})
    create_benefic = context.management.create_beneficiary(context.management_super_token, post_data)
    if status == 'Успешно':
        message = assert_error_message('Сотрудника не удалось создать', create_benefic)
        assert create_benefic.status_code == 200, message
        create_benefic = json.loads(create_benefic.text)
        context.beneficiary_id = create_benefic['id']
    elif status == 'Неуспешно':
        message = assert_error_message('Сотрудника создать удалось. ожидалась ошибка', create_benefic)
        assert create_benefic.status_code != 200, message

@When('{status} получим список сотрудников')
def step_impl(context, status):
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000, "typeIds": [2]})
    search_ben = context.management.post_beneficiary(context.management_super_token, post_data)
    message = assert_error_message('Список сотрудников не получен', search_ben)
    assert search_ben.status_code == 200, message
    search_ben = json.loads(search_ben.text)
    context.bearch_list_ben = search_ben['data']
    if status == 'Успешно':
        context.bearch_list_ben = search_ben['data']
    elif status == 'Неуспешно':
        message = assert_error_message('Список сотрудников получен, ожидалась ошибка', search_ben)
        assert search_ben.status_code != 200, message

@Then('Проверим в списке созданного сотрудника')
def step_impl(context):

    benefit_id = context.beneficiar_id
    get_benef = context.management.get_beneficiary(context.management_super_token, benefit_id)
    message = assert_error_message('Получить информацию о сотруднике не удалось', get_benef)
    assert get_benef.status_code == 200, message
    get_benef = json.loads(get_benef.text)
    gets_benef_id = get_benef['id']
    

@Then('Проверим что список сотрудников не пустой')
def step_impl(context):
    assert context.bearch_list_ben != [], 'Список сотрудников пуст, необходимо проверить корректность выполнения предусловий или шагов'

@When('"{status}" откроем карточку тестового сотрудника "{benefit_id}"')
def step_impl(context, status, benefit_id):

    if(benefit_id):
        context.benefit_id = benefit_id

    get_benef = context.management.get_beneficiary(context.management_super_token, benefit_id)
    message = assert_error_message('Получить информацию о сотруднике не удалось', get_benef)
    assert get_benef.status_code == 200, message
    context.benef_data = json.loads(get_benef.text)

@Then("Проверим есть ли у тестового сотрудника уже заведенные социальные счета")
def step_impl(context):
    beneficiary_ids = [context.benefit_id]

    request = json.dumps({"beneficiaryIds":beneficiary_ids, "column":"ChangeDate", "direction":2, "page":1, "pageSize":5})
    res = context.management.search_socialaccount(context.management_super_token, request)
    res = res.json()

    first_hash_pan = res['data'][0]['panHash']
    if(first_hash_pan != None):
        context.is_already_set_socialaccount = True
        context.social_accounts_data = res
    else:
        context.is_already_set_socialaccount = False

@When('"{status}" добавим "{activity_status}" социальный счет')
def step_impl(context,status, activity_status):

    social_account_activity = False
    if activity_status == 'активный':
        social_account_activity = True

    generate_card = (credit_card_number(16,1))
    generate_card = ''.join(generate_card)


    requests = json.dumps({"beneficiaryId":context.benefit_id, "comment":"", "enabled":social_account_activity, "pan":generate_card, "panHash":"", "protocolTypeId":3, "socialProgramId":context.benef_data['socialProgramIds'][0]})
    res = context.management.create_socialaccount(context.management_super_token, requests)
    message = assert_error_message('Добавить социальный счет для сотрудника не удалось', res)
    if status == 'Успешно':
        assert res.status_code == 200, message
    elif status == 'Неуспешно':
        assert res.status_code != 200, message


@When("Выберем первый социальный счет")
def step_impl(context):
    assert context.social_accounts_data['data'][0]['id'] is not None
    context.social_account = context.social_accounts_data['data'][0]

@Then("Получим его баланс")
def step_impl(context):
    context.social_account_id =  context.social_account['id']
    res = context.management.get_balance(context.management_super_token, context.social_account_id)
    res = res.json()
    context.cur_benef_balance = res['balance']

@Then('"{status}" пополним его на сумму "{credit_sum}" копеек')
def step_impl(context, status, credit_sum):
    request = json.dumps({"balance":context.cur_benef_balance, "comment":"", "value":credit_sum})
    res = context.management.add_credit(context.management_super_token, request, context.social_account_id)
    message = assert_error_message('Пополнить социальный счет для сотрудника не удалось', res)
    if status == 'Успешно':
        assert res.status_code == 200, message
    elif status == 'Неуспешно':
        assert res.status_code != 200, message
