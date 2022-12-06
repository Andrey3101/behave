@fixture.management_super_auth
@fixture.ensure_executive_authoritie_false
@fixture.ensure_benefit_types
@fixture.ensure_social_program_true
@fixture.ensure_merchant
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true
@fixture.ensure_merchant_edit

Feature: Проверка функциональности администрирования сущности торговое предприятие
  
  Background: Проверка авторизации СуперАдмина, получение списка торг.предприятий, проверка списка
    Given Пользователь авторизован с ролью "Superadmin"
    When Успешно получим список торговых предприятий
    Then Проверим что не пустой список торговых предприятий

  @success @merchants_success
  Scenario: TSTFLO-1078 Получение списка торговых предприятий при авторизации за Superadmin
    When Успешно получим информацию по тестовому торговому предприятию
    
  @success @merchants_success
  Scenario: TSTFLO-672 Создание тестового торгового предприятия за Superadmin
    When Успешно cоздадим тестовое торговое преприятие
    When Успешно получим список торговых предприятий
    Then Проверим в списке созданное тестовое торговое преприятие
    
  @success @merchants_success
  Scenario: TSTFLO-1077 Редактирование тестового торгового предприятия за Superadmin
    When Успешно получим информацию по тестовому торговому предприятию
    And Успешно редактируем тестовое торговое предприятие
    
  @success @merchants_success
  Scenario:  TSTFLO-1079 Успешное удаление тестового торгового предприятия за Superadmin без привязанных сущностей
    When Успешно удалим тестовое торговое предприятие
    
  @fail @merchants_fail
  @fixture.ensure_executive_authoritie_edit_false
  @fixture.ensure_benefit_edit
  @fixture.ensure_social_program_edit_true
  @fixture.ensure_merchant_edit
  @fixture.ensure_shop_edit
  @fixture.ensure_terminal_edit
  @fixture.ensure_category_edit
  @fixture.ensure_product_catalog
  @fixture.dicktion_cache
  @fixture.ensure_card_NKO_true
  Scenario: TSTFLO-1469 Неуспешное удаление тестового торгового предприятия с привязнными сущностями категории льгот и социальным учреждением
    Given Проверим баланс в НКО, там он равен 1000
    And Запрос на резервирование "auth_request"
    When Запрос на резервирование  "auth_request"  отправлен в терминальную службу
    Then Получен ответ "APPR" на запрос резервирования
    When Неуспешно удалим тестовое торговое предприятие