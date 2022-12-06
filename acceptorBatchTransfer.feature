@all @bt

@fixture.management_super_auth
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true
@fixture.ensure_merchant_edit
@fixture.ensure_shop_edit
@fixture.ensure_terminal_edit
@fixture.ensure_category_edit
@fixture.ensure_product_catalog
@fixture.dicktion_cache                                                                                                                       # создание соцсчета и пополнение

@fixture.ensure_card_NKO_true

Feature: acceptorBatchTransfer (terminalsystem)
Успешное списание и ошибки списания

Background:
Given Запрос на резервирование "auth_request"
When Запрос на резервирование  "auth_request"  отправлен в терминальную службу
Given Запрос на списание "bt_request" с теми же реквизитами покупки, что и запрос на резервирование "auth_request", и кодом авторизации "auth_code" из ответа на резервирование "auth_response"

    @success @bt_success
    Scenario: Успешное списание средств с соцсчета
    When Запрос на списание "bt_request" отправлен в терминальную службу
    Then Получен ответ "APPR" на запрос списания
 
    @fail @304
    Scenario: Отсутствие предприятия в СП (304)
    When Значение предприятия "organisation_id" из запроса "bt_request" отсутствует в СП
    # тег <InitgPty><Id>
    And Запрос на списание "bt_request" отправлен в терминальную службу
    Then Получен ответ "304/APPR" на запрос списания

    @fail @309
    Scenario: Отсутствие магазина в СП (309)
    When Значение магазина "merchant_id" из запроса "bt_request" отсутствует в СП
    # тег <Mrchnt><Id><Id>
    And Запрос на списание "bt_request" отправлен в терминальную службу
    Then Получен ответ "309/APPR" на запрос списания

    @fail @310
    Scenario: Отсутствие магазина в СП (310)
    When Значение магазина "terminal_id" из запроса "bt_request" отсутствует в СП
    # тег <Mrchnt><Id><Id>
    And Запрос на списание "bt_request" отправлен в терминальную службу
    Then Получен ответ "310/APPR" на запрос списания

    @fail @331
    Scenario: Транзакция обработана ранее (331)
    When Запрос на списание "bt_request" отправлен в терминальную службу
    And Запрос на списание "bt_request" отправлен в терминальную службу
    Then Получен ответ "331/APPR" на запрос списания

    @fail @387
    Scenario: Код авторизации не соответствует полученному при резервировании (387)
    When Значение кода "r_auth_code" из запроса "bt_request" произвольное в списании
    When Запрос на списание "bt_request" отправлен в терминальную службу
    # тег <AuthstnCd> блока <TxRspn> ответа
    Then Получен ответ "387/APPR" на запрос списания

