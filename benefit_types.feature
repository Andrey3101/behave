@fixture.management_super_auth
@fixture.management_tsp_auth
@fixture.management_oiv_auth
@fixture.ensure_benefit_types
@fixture.ensure_benefit_edit

Feature: Проверка функциональности администрирования сущности категория льгот

  Background: Проверка авторизации СуперАдмина, получение списка категорий льгот, проверка списка
    Given Пользователь авторизован с ролью "Superadmin"
    When Успешно получим список категорий льгот
    Then Проверим что список категорий льгот не пустой

  @success @benefit_types_success
  Scenario: TSTFLO-1224 Получение списка категорий льгот при авторизации за Superadmin
    When Успешно получим информацию по тестовой категории льгот

  @success @benefit_types_success
  Scenario: TSTFLO-1216 Создание тестовой категории льгот при авторизации за Superadmin
    When Успешно создадим тестовую категорию льгот
    And Успешно получим список категорий льгот
    Then Проверим в списке созданную категорию льгот

  @success @benefit_types_success
  Scenario: TSTFLO-1220 Редактирование тестовой категории льгот при авторизации за Superadmin
    When Успешно получим информацию по тестовой категории льгот
    And Успешно редактируем тестовую категорию льгот

  @success @benefit_types_success
  Scenario: TSTFLO-1236 Успешное удаление тестовой категории льгот за Superadmin без привязанных сущностей
    When Успешно получим информацию по тестовой категории льгот
    And Успешно удалим тестовую категорию льгот
  
  @fail @benefit_types_fail
  @fixture.ensure_executive_authoritie_edit_false
  @fixture.ensure_benefit_edit
  @fixture.ensure_social_program_edit_true
  Scenario: TSTFLO-1234 Неуспешное удаление тестовой категории льгот за Superadmin с привязкой к социальной программе
    When Успешно получим информацию по тестовой категории льгот
    And Неуспешно удалим тестовую категорию льгот