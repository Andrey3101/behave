@all @auth_v2

@fixture.management_super_auth # Авторизация за супер администратора
@fixture.ensure_executive_authoritie_edit_false  # Создание социального учреждения
@fixture.ensure_benefit_edit # Создание категории льгот
@fixture.ensure_social_program_edit_false # Создание социальной программы
@fixture.ensure_merchant_edit # Создание ТСП
@fixture.ensure_shop_edit # Создание магазина
@fixture.ensure_terminal_edit # Создание терминала
@fixture.ensure_category_edit # Создание категории продуктов
@fixture.ensure_product_catalog # Создание каталога продуктов
@fixture.dicktion_cache # Чистка кэша
@fixture.generate_api_key #Генерация ключа для ТСП (который создавался выше)
@fixture.get_merchant_key # Получение ключа от ТСП

@fixture.auth_tsp 																						# Авторизация в терминальном сервисе (Эвотор) с использованием полученного от ТСП ключа
@fixture.ensure_card_NKO_true                                                                           # создание соцсчета и пополнение

Feature: batch/Auth (terminalsystem_v2)
Успешное резервирование и ошибки резервирования по протоколу Эвотор

Background:
Given Запрос на резервирование "auth_request_v2"

    @success @auth_v2_success
    Scenario: Успешное резервирование средств на соцсчете
    When Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
    Then Получен ответ "responseCode: 0"

    @fail @206_v2
    Scenario: Отсутствие магазина в СП (206)
    When Значение магазина "merchant_id" из запроса отсутствует в СП                                    # параметр merchantId
    And Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
    Then Получен ответ "responseCode: 206"

    @fail @207_v2
    Scenario: Отсутствие кассы в СП (207)
    When Значение кассы "terminal_id" из запроса отсутствует в СП                                       # параметр terminalId
    And Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
    Then Получен ответ "responseCode: 207"

#    @fail @210_v2
#    Scenario: Отсутствие счета в НКО (210)
#    When Значение карты "panhash" из запроса отсутствует в НКО                                     # параметр card.pan
#    And Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
#    Then Получен ответ "responseCode: 210"

    # @fail @214_v2
    # Scenario: Отсутствие категории товара в каталоге товаров (214)
    # When Значение категории товара "product_category" из запроса отсутствует в СП  					# параметр products.categoryCode
    # And Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
    # Then Получен ответ "responseCode: 214"

#    @fail @214_v2
#    Scenario: Отсутствие социальной категории из запроса в классификаторе по социальной программе (214)
#    When Значение социальной категории предприятия "social_category" из запроса отсутствует в СП  		# параметр products.socialCategoryCode
#    And Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
#    Then Получен ответ "responseCode: 214"

#    @fail @217_v2
#    Scenario: Сумма резервирования больше баланса на счету (217)
#    When Значение суммы резервирования "auth_amount" из запроса больше баланса на счету                 # параметр batch.amount 
#    And Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
#    Then Получен ответ "responseCode: 217"

#    @fail @227_v2
#    Scenario: Транзакция обработана ранее (227)
#    When Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
#    And Запрос на резервирование "auth_request_v2" повторно отправлен в терминальную службу
#    Then Получен ответ "responseCode: 227"

#    @fail @230_v2
#    Scenario: Переданная соцпрограмма отсутствует в СП (230)
#    When Значение "social_program" из запроса отсутствует в СП                                         # параметр socialProgramId
#    And Запрос на резервирование "auth_request_v2" отправлен в терминальную службу
#    Then Получен ответ "responseCode: 230"
