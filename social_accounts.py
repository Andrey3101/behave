from datetime import datetime, timedelta
import json
import random
from gen.inn import inn as gen_inn
from gen.snils import snils as gen_snils
from gen.gen_credit_card_number import credit_card_number as gen_card
from check_data import check_socials_benefeciaries, check_socials_acc_import, check_socials_catalog
from fixtures import assert_error_message

@Given('Подготовлен тестовый csv файл соц.счетов с {counts} НКО {string} и блокировкой {block_counts} {option} счета(ов)')
def step_impl(context, counts, string, block_counts, option):
    # Заголовоки столбцов
    block_counts = int(block_counts)
    counts = int(counts)
    context.import_social_acc_data = {'sheets':[]}
    sheet = {'data': []}
    sheet['header'] = ['Счет', 'ХЭШ', 'ИНН', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'СНИЛС', 'Дата регистрации']
    # генерация данных
    datas = []

    if block_counts >= 1:
        context.block_import_social_data = []
        if option == 'активного':
            request = json.dumps({"enabled":True,"page":1,"pageSize":block_counts,"column":"id","direction":2})
            block_data = context.management.search_socialaccount(context.management_super_token, request)
            message = assert_error_message('Соц.счета не получены при заполнении csv файла для установки флага блокировки счетов', block_data)
            assert block_data.status_code == 200, message
            block_data = json.loads(block_data.text)
            assert len(block_data['data']) >= block_counts, 'Активных соц.счетов не хватает для блокировки, всего активных счетов {0} в системе'.format(block_data['elementCount'])
        for data in block_data['data']:
            if data['birthdate'] != None:
                birthday = datetime.strptime(data['birthdate'], "%Y-%m-%dT%H:%M:%S").strftime('%d.%m.%Y')
            else:
                birthday = None
            datas.append([data['number'], '_XXXXXXXXXX_', data['inn'], data['lastName'], data['firstName'], data['middleName'], birthday, data['snils'], data['registredDate'][:-9]])

    for count in range(counts): 
        code = ''.join(random.choice('1234567890') for i in range (15))
        inn = gen_inn(12)
        snils = gen_snils()
        hash_card = gen_card(16, 1)[0]
        social_program = context.social_program_code
        surrogate_name = hash_card + social_program
        # phone = '+7' + '-' + '921' + str(random.randint(100,999)) + '-' + str(random.randint(10,99)) + '-' + str(random.randint(10,99))
        # date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00'
        date = datetime.now().strftime('%d.%m.%Y')
        code_name = datetime.now().strftime('%S%f')[:-3]
        burthday = (datetime.now()-timedelta(days=random.randint(18,99)*365)).strftime('%d.%m.%Y')
        datas.append([str(code), str(surrogate_name), str(inn), 'Behave'+code_name, 'Test'+code_name, 'Тестович'+code_name, burthday, str(snils), date])
    sheet['data'] = datas
    context.import_social_acc_data['sheets'].append(sheet)
    context.csv_file = context.csv.create_nko(context.import_social_acc_data)
    pass

@When('{status} импортируем файл соц.счетов')
def step_impl(context, status):
    assert context.csv_file, 'Файл не был сгенерирован автотестом, проверьте шаг "Дано"(Given) Подготовлен тестовый xlsx файл соц.счетов с 1 или более записью'.format()
    create_nko = context.management.import_social(context.management_super_token, context.csv_file)
    if status == 'Успешно':
        message = assert_error_message('Файл соц.счетов успешно не импортирован', create_nko)
        assert create_nko.status_code == 200, message
        response = json.loads(create_nko.text)
        assert response['errorDataCount'] == 0, 'Импорт содержит {0} ошибку или ошибок, ожидался импорт без ошибок'.format(response['errorDataCount'])
        context.status_import = response

@Then('Проверим статус импорта {type_import} на {option} ошибок')
def step_impl(context, type_import, option):
    id_log = context.status_import['importLogId']
    status_import = context.management.get_import_log(context.management_super_token, id_log)
    assert status_import.status_code == 200, 'Ошибка получения каталога с id {1}. {0}'.format(status_import.text, id_log)
    status_import = json.loads(status_import.text)
    assert status_import['id'] == id_log, 'Полученный id лога {0} не совпадает с запрошенным {1}'.format(status_import['id'], id_log)
    if type_import == 'соц.счетов':
        assert status_import['typeName'] == 'Социальные счета', 'Получен не верный статус импорта, ожидался {0} получили {1}. id лога {2}'.format('Социальные счета', status_import['typeName'], id_log)
    elif type_import == 'потребителей':
        assert status_import['typeName'] == 'Потребители', 'Получен не верный статус импорта, ожидался {0} получили {1}. id лога {2}'.format('Социальные счета', status_import['typeName'], id_log)
    elif type_import == 'каталога':
        assert status_import['typeName'] == 'Каталог товаров', 'Получен не верный статус импорта, ожидался {0} получили {1}. id лога {2}'.format('Социальные счета', status_import['typeName'], id_log)
    if option == 'отсутствие':
        assert status_import['errorDataCount'] == 0, 'В импорте {0} присутствуют ошибки'.format(status_import['typeName'])
    elif option == 'наличие':
        assert status_import['errorDataCount'] != 0, 'В импорте {0} отсутствуют ошибки'.format(status_import['typeName'])

@Then('Проверим импорт {type_import}')
def step_impl(context, type_import):
    if type_import == 'соц.счетов':
        check_socials_acc_import(context)
    elif type_import == 'потребителей':
        check_socials_benefeciaries(context)
    elif type_import == 'каталога':
        check_socials_catalog(context)