import json
from time import sleep
from datetime import datetime

def check_socials_acc_import(context):
    if len(context.import_social_acc_data) > 0:
                assert context.import_social_acc_data, 'Импорт не был произведён, context.import_social_acc_data не задан'
                assert len(context.import_social_acc_data) > 0, 'context.import_social_acc_data не содержит данных, массив пустой'
                for data in context.import_social_acc_data['sheets'][0]['data']:
                    request = json.dumps({"snils":str(data[7]),"page":1,"pageSize":1})
                    for x in range(4):
                        check_data = context.management.search_socialaccount(context.management_super_token, request)
                        assert check_data.status_code == 200, 'Соц.счет по снилсу {1} не получен, ошибка {0}'.format(check_data.text, str(data[7]))
                        check_data = json.loads(check_data.text)
                        try:
                            assert check_data['elementCount']!= 0, 'Соц.счет по снилсу {0} не найден'.format(str(data[7]))
                            check_data = check_data['data'][0]
                            assert data[0] == check_data['number'], 'Номер счета аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[0], check_data['number'])
                            if data[1] == '_XXXXXXXXXX_':
                                assert check_data['enabled'] == False, 'При импорте не сработала блокировка счета с id {1} загружаемая строка {0}'.format(data, check_data['id'])
                            else:
                                assert check_data['enabled'] == True, 'При импорте не сработал активация счета с id {1} загружаемая строка {0}'.format(data, check_data['id'])
                                assert data[1] == check_data['accountNumber'], 'ХЭШ аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[1], check_data['accountNumber'])
                            assert data[2] == check_data['inn'], 'ИНН аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[2], check_data['inn'])
                            assert data[3] == check_data['lastName'], 'Фамилия аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[3], check_data['lastName'])
                            assert data[4] == check_data['firstName'], 'Имя аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[4], check_data['firstName'])
                            assert data[5] == check_data['middleName'], 'Отчетство аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[4], check_data['firstName'])
                            assert datetime.strptime(data[6], "%d.%m.%Y") == datetime.strptime((check_data['birthdate']), "%Y-%m-%dT%H:%M:%S"), 'Дата рождения аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[6], check_data['birthdate'])
                            assert data[7] == check_data['snils'], 'СНИЛС аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[7], check_data['snils'])
                            assertation = True
                            break
                        except:
                            context.behave_log.info('Запись соц.счета по снилсу {1} в системе не найдена или статус не верен, после 20 секунд ожидания будет повторная попытка №{0} из 5'.format(x+2, data[7]))
                            assertation = False
                            sleep(20)
                    assert assertation == True, ('Запись соц.счета по снилсу {0} в системе не найдена или статус не верен'.format(data[7]))

def check_socials_benefeciaries(context):
    if len(context.import_data_beneficiarie['sheets'][0]['data']) > 0:
        for data in context.import_data_beneficiarie['sheets'][0]['data']:
            request = json.dumps({"snils":str(data[0]),"page":1,"pageSize":1})
            for x in range(4):
                check_data = context.management.search_beneficiarys(context.management_super_token, request)
                assert check_data.status_code == 200, 'Потребитель по снилсу {1} не получен, ошибка {0}'.format(check_data.text, str(data[0]))
                check_data = json.loads(check_data.text)
                try:
                    assert check_data['elementCount']!= 0, 'Потребитель по снилсу {0} не найден'.format(str(data[0]))
                    check_data = check_data['data'][0]
                    assert data[0] == check_data['snils'], 'СНИЛС потребителя {0} из файла и полученного из системы {1} не совпадают'.format(data[0], check_data['snils'])
                    assert data[1] == check_data['inn'], 'ИНН аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[1], check_data['inn'])
                    assert data[2] == check_data['lastName'], 'Фамилия аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[2], check_data['lastName'])
                    assert data[3] == check_data['firstName'], 'Имя аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[3], check_data['firstName'])
                    assert data[4] == check_data['middleName'], 'Отчетство аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[4], check_data['firstName'])
                    assert datetime.strptime(data[5], "%d.%m.%Y") == datetime.strptime((check_data['birthdate']), "%Y-%m-%dT%H:%M:%S"), 'Дата рождения аккаунта {0} из файла и полученного из системы {1} не совпадают'.format(data[5], check_data['birthdate'])
                    assertation = True
                except:
                    context.behave_log.info('Запись потребителя по снилсу {1} в системе не найдена или статус не верен, после 20 секунд ожидания будет повторная попытка №{0} из 5'.format(x+2, data[0]))
                    assertation = False
                    sleep(20)
            assert assertation == True, ('Запись потребителя по снилсу {0} в системе не найдена или статус не верен'.format(data[0]))

def check_socials_catalog(context):
    if len(context.import_data_catalog['sheets'][0]['data']) > 0:
        request = json.dumps({"merchantIds":[context.merch_id],"socialProgramIds":[context.soc_program],"page":1,"pageSize":1,"column":"ChangeDate","direction":2,"showCancelled":False,"type":1})
        try:
            catalog_id = context.empty_product_catalog_id
        except:
            for x in range(4):
                try:
                    create_catalogs = context.management.search_product_catalog(context.management_super_token, request)
                    assert create_catalogs.status_code == 200, 'Список каталога не получен по merchantIds {1} и socialProgramIds {2}, ошибка {0}'.format(create_catalogs.text, context.merch_id, context.soc_program, context.soc_program)
                    catalog_id = json.loads(create_catalogs.text)['data'][0]['id']
                    break
                except:
                    context.behave_log.info('Каталог не найден, или статус не верен, после 20 секунд ожидания будет повторная попытка №{0} из 5'.format(x+2))
                    error = ('Каталог не найден, или статус не верен'.format())
                    sleep(20)
        for data in context.import_data_catalog['sheets'][0]['data']:
            try:
                catalog_id
            except UnboundLocalError:
                raise UnboundLocalError('Каталог не был найден или статус не верный, в ответ на поиск каталогов по merchantIds {1} и socialProgramIds {2} получили ответ {0}'.format(create_catalogs.text, context.merch_id, context.soc_program))
            request = json.dumps({"page":1,"pageSize":1,"column":"ChangeDate","direction":2,"productCatalogId":catalog_id, "code": data[3]})
            for x in range(4):
                check_data = context.management.search_product_catalog_product(context.management_super_token, request)
                assert check_data.status_code == 200, 'Товар в каталоге не получен по артикулу {1}, ошибка {0}'.format(check_data.text, str(data[3]))
                check_data = json.loads(check_data.text)
                try:
                    assert check_data['elementCount']!= 0, 'Товар по артикулу {0} не найден'.format(str(data[3]))
                    check_data = check_data['data'][0]
                    assert data[2] == check_data['name'], 'Наименование {0} товара из файла и наименование {1} в каталоге не совпадают'.format(data[2], check_data['name'])
                    assert data[3] == check_data['code'], 'Артикул {0} товара из файла и артикул {1} в каталоге не совпадают'.format(data[3], check_data['code'])
                    assert int(data[4])*100 == check_data['price'], 'Артикул {0} товара из файла и артикул {1} в каталоге не совпадают'.format(data[3], check_data['code'])
                    assertation = True
                    break
                except:
                    context.behave_log.info('Запись товара по артикулу {1} в каталоге не найдена или статус не верен, после 20 секунд ожидания будет повторная попытка №{0} из 5'.format(x+2, data[3]))
                    assertation = False
                    error = ('Запись товара по артикулу {0} в каталоге не найдена или статус не верен'.format(data[3]))
                    sleep(20)
            assert assertation == True, error

