@fixture.management_super_auth
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true
@fixture.ensure_merchant_edit
@fixture.ensure_category_edit
#@fixture.ensure_executive_authoritie
#@fixture.ensure_benefit_types
#@fixture.ensure_social_program
#@fixture.ensure_merchant
#@fixture.ensure_product_category

Feature: Проверка функциональности администрирования сущности категория продуктов

  Background: Проверка авторизации СуперАдмина, получение списка продуктов, проверка списка
    Given Пользователь авторизован с ролью "Superadmin"
    When Успешно получим список категорий продуктов
    Then Проверим что не пустой список категорий продуктов

  @success @product_category_success
  Scenario: TSTFLO-1078 Получение списка категорий продуктов при авторизации за Superadmin
    When Успешно получим информацию по тестовой категории продуктов

  @success @product_category_success
  Scenario: TSTFLO-672 Создание тестовой категории продуктов за Superadmin
    When Успешно cоздадим тестовую категорию продуктов
    When Успешно получим список категорий продуктов
    Then Проверим в списке созданную тестовую категорию продуктов

  @success @product_category_success
  Scenario: TSTFLO-1077 Редактирование тестовой категории продуктов за Superadmin
    When Успешно получим информацию по тестовой категории продуктов
    And Успешно редактируем тестовую категорию продуктов

  @success @product_category_success
  Scenario: TSTFLO-1079 Успешное удаление тестовой категории продуктов за Superadmin без привязанных сущностей
    When Успешно удалим тестовую категорию продуктов

  @fail @product_category_fail
  @fixture.ensure_executive_authoritie_edit_false
  @fixture.ensure_benefit_edit
  @fixture.ensure_social_program_edit_true
  @fixture.ensure_merchant_edit
  @fixture.ensure_category_edit
  @fixture.ensure_product_catalog
  Scenario: TSTFLO-1469 Неуспешное удаление тестовой категории продуктов с привязнными сущностями категории льгот и социальным учреждением
    When Неуспешно удалим тестовую категорию продуктов