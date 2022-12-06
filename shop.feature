@fixture.management_super_auth
@fixture.ensure_executive_authoritie_false
@fixture.ensure_benefit_types
@fixture.ensure_social_program_true
@fixture.ensure_merchant
@fixture.ensure_shop
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true
@fixture.ensure_merchant_edit
@fixture.ensure_shop_edit

Feature: Проверка функциональности администрирования сущности магазин
  
  Background: Проверка авторизации СуперАдмина, получение списка магазинов, проверка списка
    Given Пользователь авторизован с ролью "Superadmin"
    When Успешно получим список магазинов
    Then Проверим что не пустой список магазинов

  # @success @shops_success
  # Scenario: TSTFLO-1089 Получение списка магазинов при авторизации за Superadmin
  #   When Успешно получим информацию по тестовому магазину

  # @success @shops_success
  # Scenario: TSTFLO-675 Создание тестового магазина за Superadmin
  #   When Успешно cоздадим тестовый магазин
  #   When Успешно получим список магазинов
  #   Then Проверим в списке созданный тестовый магазин

  # @success @shops_success
  # Scenario: TSTFLO-677 Редактирование тестового магазина за Superadmin
  #   When Успешно получим информацию по тестовому магазину
  #   And Успешно редактируем тестовый магазин

  # @success @shops_success
  # Scenario: TSTFLO-678 Успешное удаление тестового магазина за Superadmin без привязанных сущностей
  #   When Успешно удалим тестовый магазин


  @fixture.ensure_executive_authoritie_edit_false
  @fixture.ensure_benefit_edit
  @fixture.ensure_social_program_edit_true
  @fixture.ensure_merchant_edit
  @fixture.ensure_shop_edit
  @fixture.ensure_terminal_edit
  @fixture.ensure_category_edit
  @fixture.ensure_product_catalog
  @fixture.ensure_card_NKO_true
  @fixture.dicktion_cache
  @fail @shops_fail
  Scenario: TSTFLO-679 Неуспешное удаление тестового магазина с привязнными сущностями категории льгот и социальным учреждением
    Given Проверим баланс в НКО, там он равен 1000
    And Запрос на резервирование "auth_request"
    When Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "APPR"
    When Успешно отправим запрос на списание денежных средств с корректными данными
    Then В теле ответа на запрос списания получим успех списания
    When Неуспешно удалим тестовый магазин