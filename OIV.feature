@fixture.cache
@fixture.management_super_auth
@fixture.management_tsp_auth
@fixture.management_oiv_auth
@fixture.ensure_executive_authoritie_false
@fixture.ensure_executive_authoritie_edit_false

Feature: Проверка функциональности администрирования сущности соц учреждения
  
  Background: Проверка авторизации СуперАдмина, получение списка соц.учреждений, проверка списка
    Given Пользователь авторизован с ролью "SuperAdmin"
    When Успешно получим список социальных учреждений
    Then Проверим что не пустой список социальных учреждений

  @success @executive_authorities_success
  Scenario: TSTFLO-1453 Получение списка соц учреждений при авторизации за Superadmin
    When Успешно получим информацию по 1 соц.учреждению из списка

  @success @executive_authorities_success
  Scenario: TSTFLO-1459 Создание социального учреждения за Superadmin
    When Успешно cоздадим социальное учреждение
    When Успешно получим список социальных учреждений
    Then Проверим в списке созданное социальное учреждение

  @success @executive_authorities_success
  Scenario: TSTFLO-1461 Редактирование социального учреждения за Superadmin
    When Успешно получим информацию по 1 соц.учреждению из списка
    And Успешно редактируем тестовое социальное учреждение

  @success @executive_authorities_success
  Scenario: TSTFLO-1466 Успешное удаление социального учреждения за Superadmin без привязанных сущностей
    When Успешно удалим тестовое социальное учреждение

  @fail @executive_authorities_fail
  @fixture.ensure_executive_authoritie_edit
  @fixture.ensure_benefit_edit
  @fixture.ensure_social_program_edit_false
  Scenario: TSTFLO-1465 Неуспешное удаление тестового социального учреждения с привязкой категории льгот и социальной программы
    When Неуспешно удалим тестовое социальное учреждение