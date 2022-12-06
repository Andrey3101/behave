@fixture.management_super_auth
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true

Feature: Проверка функциональности социальные счета

  Background: Авторизация Админа
    Given Пользователь авторизован с ролью "SuperAdmin"
    
  @success @import_succes @social_accounts_success
  Scenario: TSTFLO-2542 Импорт социального счета
    Given Подготовлен тестовый csv файл соц.счетов с 1 НКО записью и блокировкой 0 активного счета(ов)
    When Успешно импортируем файл соц.счетов
    Then Проверим статус импорта соц.счетов на отсутствие ошибок
    And Проверим импорт соц.счетов

  @success @import_succes @social_accounts_success
  Scenario: TSTFLO-2542 Импорт пяти социальных счетов
    Given Подготовлен тестовый csv файл соц.счетов с 5 НКО записями и блокировкой 0 активного счета(ов)
    When Успешно импортируем файл соц.счетов
    Then Проверим статус импорта соц.счетов на отсутствие ошибок
    And Проверим импорт соц.счетов

  @success @import_succes @social_accounts_success @import_block_success
  Scenario: TSTFLO-2539 Импорт одного социального счета и блокировка одного счета 
    Given Подготовлен тестовый csv файл соц.счетов с 1 НКО записями и блокировкой 1 активного счета(ов)
    When Успешно импортируем файл соц.счетов
    Then Проверим статус импорта соц.счетов на отсутствие ошибок
    And Проверим импорт соц.счетов