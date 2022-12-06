from datetime import datetime
import json
from fixtures import assert_error_message


@When('{option} получим список социальных программ')
def step_impl(context, option):
    post_data = json.dumps({"column": None, "direction": None, "page": 1, "pageSize": 1000})
    social_program = context.management.post_social_program(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Список социальных программ не получен', social_program)
        assert social_program.status_code == 200, message
        social_program = json.loads(social_program.text)
        context.social_program_list = social_program['data']
    elif option == 'Неуспешно':
        message = assert_error_message('Список социальных учреждений получен, ожидалась ошибка', social_program)
        assert social_program.status_code != 200, message

@Then('Проверим что не пустой список социальных программ')
def step_impl(context):
    assert context.social_program_list != [], 'Список социальных программ пустой, необходимо проверить корректность выполнения предусловий или шагов'

@When('{option} получим информацию по тестовой социальной программе')
def step_impl(context, option):
    test_soc_proc_name = 'Тестовая социальная программа Behave'
    test_soc_proc_type = context.config.userdata['test_all_data']['typeId']
    test_soc_proc_region = context.config.userdata['test_all_data']['regionId']
    post_data = json.dumps({"name": test_soc_proc_name, "typeId": test_soc_proc_type, "regionId": test_soc_proc_region})
    soc_program = context.management.post_social_program(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Информация по соц.программе не получена', soc_program)
        assert soc_program.status_code == 200, message
        soc_program = json.loads(soc_program.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Информация по соц.программе получена, ожидалась ошибка', soc_program)
        assert soc_program.status_code != 200, message

@When('{option} cоздадим тестовую социальную программу')
def step_impl(context, option):
    add_test_social_program_name = 'Тестовая соц программа Behave'
    add_test_social_program_region = context.config.userdata['test_all_data']['regionId']
    date_create = (datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    add_test_social = context.config.userdata['test_all_data']['check_all']
    post_data = json.dumps({"name": add_test_social_program_name,"dateFrom": date_create ,"dateTo": None ,"description": None, "typeId": 1, "executiveAuthorityId": context.executive_id, "regionId": add_test_social_program_region, "benefitTypeIds": [context.benefit_id], "balanceBurn": add_test_social, "checkBenefitDates": add_test_social, "checkProductCatalogPrice": add_test_social, "checkProductPrice": add_test_social, "checkProductQuantity": add_test_social, "checkReserveAndTransferAmount": add_test_social, "projectTypeId": 0, "socialAccountTypeId": 2})
    soc_proc_add = context.management.add_social_program(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Социальную программу не удалось создать', soc_proc_add)
        assert soc_proc_add.status_code == 200, message
        soc_proc_add = json.loads(soc_proc_add.text)
        context.create_social_program = soc_proc_add['id']
    elif option == 'Неуспешно':
        message = assert_error_message('Социальное учреждение удалось создать, ожидалась ошибка', soc_proc_add)
        assert soc_proc_add != 200, message

@Then('Проверим в списке созданную тестовую социальную программу')
def step_impl(context):
    create_soc_proc = context.create_social_program
    get_social_program = context.management.get_social_program(context.management_super_token, create_soc_proc)
    message = assert_error_message('Не удалось получить информацию по социальной программе', get_social_program)
    assert get_social_program.status_code == 200, message
    get_social_program = json.loads(get_social_program.text)

@When('{option} редактируем тестовую тестовую социальную программу')
def step_impl(context, option):
    up_social_program_id = context.soc_program
    up_social_program_name = 'Тестовая социальная программа behave'
    up_social_program_type = 1
    up_social_program_region = context.config.userdata['test_all_data']['regionId']
    up_social_program_check = context.config.userdata['test_all_data']['check_all']
    date_update = (datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    post_data = json.dumps({"id": up_social_program_id, "name": up_social_program_name, "dateFrom": date_update, "dateTo": None, "description": None, "typeId": up_social_program_type, "executiveAuthorityId": context.executive_id, "regionId": up_social_program_region, "benefitTypeIds": [context.benefit_id],  "balanceBurn": up_social_program_check, "checkBenefitDates": up_social_program_check, "checkProductCatalogPrice": up_social_program_check, "checkProductPrice": up_social_program_check, "checkProductQuantity": up_social_program_check, "checkReserveAndTransferAmount": up_social_program_check, "projectTypeId": 0, "socialAccountTypeId": 2})
    update_social_program_list = context.management.put_social_program(context.management_super_token, post_data)
    if option == 'Успешно':
        message = assert_error_message('Не удалось отредактировать социальную программу', update_social_program_list)
        assert update_social_program_list.status_code == 200, message
        update_social_program_list = json.loads(update_social_program_list.text)
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось отредактировать социальную программу, ожидалась ошибка', update_social_program_list)
        assert update_social_program_list != 200, message

@When('{option} удалим тестовую социальную программу')
def step_impl(context, option):
    delete_social_program = context.soc_program
    del_soc_proc = context.management.delete_social_program(context.management_super_token, delete_social_program)
    if option == 'Успешно':
        message = assert_error_message('Не удалось удалить социальную программу', del_soc_proc)
        assert del_soc_proc.status_code == 200, message
    elif option == 'Неуспешно':
        message = assert_error_message('Удалось удалить социальную программу, ожидалась ошибка', del_soc_proc)
        assert del_soc_proc.status_code == 400, message