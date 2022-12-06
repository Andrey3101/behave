@fixture.management_super_auth
@fixture.ensure_executive_authoritie_false
@fixture.ensure_benefit_types
@fixture.ensure_social_program_true
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true

Feature: Проверка функциональности администрирования сущности соц программа

  Background: Проверка авторизации СуперАдмина, получение списка соц.программ, проверка списка
    Given Пользователь авторизован с ролью "Superadmin"
    When Успешно получим список социальных программ
    Then Проверим что не пустой список социальных программ

  @success @social_programm_success
  Scenario: TSTFLO-1075 Получение списка социальных программ при авторизации за Superadmin
    When Успешно получим информацию по тестовой социальной программе

  @success @social_programm_success
  Scenario: TSTFLO-1071 Создание тестовой социальной программы за Superadmin
    When Успешно cоздадим тестовую социальную программу
    When Успешно получим список социальных программ
    Then Проверим в списке созданную тестовую социальную программу

  @success @social_programm_success
  Scenario: TSTFLO-1073 Редактирование социальной программы за Superadmin
    When Успешно получим информацию по тестовой социальной программе
    And Успешно редактируем тестовую тестовую социальную программу

  @success @social_programm_success
  Scenario: TSTFLO-1140 Успешное удаление тестовой социальной программы за Superadmin без привязанных сущностей
    When Успешно удалим тестовую социальную программу

  @fail @social_programm_fail
  @fixture.ensure_executive_authoritie_edit_false
  @fixture.ensure_benefit_edit
  @fixture.ensure_social_program_edit_true
  @fixture.ensure_merchant_edit
  Scenario: TSTFLO-1141 Неуспешное удаление тестовой социальной программы с привязнными сущностями категории льгот и социальным учреждением
    When Неуспешно удалим тестовую социальную программу