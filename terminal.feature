@fixture.management_super_auth
@fixture.ensure_executive_authoritie_false
@fixture.ensure_benefit_types
@fixture.ensure_social_program_true
@fixture.ensure_merchant
@fixture.ensure_shop
@fixture.ensure_terminal
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true
@fixture.ensure_merchant_edit
@fixture.ensure_shop_edit
@fixture.ensure_terminal_edit

Feature: Проверка функциональности администрирования сущности терминал
  
  Background: Проверка авторизации СуперАдмина, получение списка терминалов, проверка списка
    Given Пользователь авторизован с ролью "Superadmin"
    When Успешно получим список терминалов
    Then Проверим что не пустой список терминалов

  @success @terminal_success
  Scenario: TSTFLO-1092 Получение списка терминалов при авторизации за Superadmin
    When Успешно получим информацию по тестовому терминалу
  
  @success @terminal_success
  Scenario: TSTFLO-680 Создание тестового терминала за Superadmin
    When Успешно cоздадим тестовый терминал
    When Успешно получим список терминалов
    Then Проверим в списке созданный тестовый терминал
  
  @success @terminal_success
  Scenario: TSTFLO-1093 Редактирование тестового терминала за Superadmin
    When Успешно получим информацию по тестовому терминалу
    And Успешно редактируем тестовый терминал
  
  @success @terminal_success
  Scenario: TSTFLO-1094 Удаление тестового терминала за Superadmin без привязанных сущностей
    Then Удалим тестовый терминал

