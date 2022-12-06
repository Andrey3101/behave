@all @auth


@fixture.management_super_auth
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true
@fixture.ensure_merchant_edit
@fixture.ensure_shop_edit
@fixture.ensure_terminal_edit
@fixture.ensure_category_edit
@fixture.ensure_product_catalog
@fixture.ensure_card_NKO_true
@fixture.dicktion_cache                                                                           # создание соцсчета и пополнение

Feature: acceptorAuthorisation (terminalsystem)
Успешное резервирование и ошибки резервирования по протоколу Мегар

Background:
Given Запрос на резервирование "auth_request"

    @success @auth_success
    Scenario: Успешное резервирование средств на соцсчете
    When Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "APPR" на запрос резервирования

    @fail @204
    Scenario: Отсутствие предприятия в СП (204)
    When Значение предприятия "organisation_id" из запроса "резервирования" отсутствует в СП
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/204" на запрос резервирования

    @fail @205
    Scenario: Отсутствие блока о магазине в запросе (205)
    When Значение блока "merchant_id" из запроса "резервирования" отсутствует в СП
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/205" на запрос резервирования

    @fail @206
    Scenario: Отсутствие магазина в СП (206)
    When Значение магазина "merchant_id" из запроса "резервирования" отсутствует в СП
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/206" на запрос резервирования

    @fail @207
    Scenario: Отсутствие кассы в СП (207)
    When Значение кассы "terminal_id" из запроса "резервирования" отсутствует в СП
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/207" на запрос резервирования

    @fail @210
    @fixture.ensure_card_NKO_false
    Scenario: Отсутствие счета в НКО (210)
    When Значение карты "panhash" из запроса отсутствует в НКО
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/210" на запрос резервирования

    @fail @214
    Scenario: Отсутствие товара в каталоге социальных товаров (214)
    When Значение товара "social_product" из запроса "резервирования" отсутствует в СП
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/214" на запрос резервирования

    @fail @217
    Scenario: Сумма резервирования больше баланса на счету (217)
    When Значение суммы резервирования "auth_amount" из запроса больше баланса на счету
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/217" на запрос резервирования

    @fail @227
    Scenario: Транзакция обработана ранее (227)
    When Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/227" на запрос резервирования

    @fail @230
    Scenario: Переданная соцпрограмма отсутствует в СП (230)
    When Значение соц.программы "social_program" из запроса "резервирования" отсутствует в СП
    And Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "DECL/230" на запрос резервирования