@fixture.management_super_auth
@fixture.ensure_executive_authoritie_edit_false
@fixture.ensure_benefit_edit
@fixture.ensure_social_program_edit_true
@fixture.ensure_merchant_edit
@fixture.ensure_category_edit

Feature: Проверка функциональности администрирования сущности каталог продуктов

  Background: Проверка авторизации СуперАдмина, получение спсика каталога
    Given Пользователь авторизован с ролью "Superadmin"
    When Успешно получим список каталогов товаров

  @success @product_catalog_success
  Scenario: TSTFLO-1107 Создание каталога товаров при авторизации за Superadmin
    Then Проверим что список каталогов не пустой
    When Успешно создадим тестовый каталог товаров
    Then Проверим созданный тестовый каталог

  @success @product_catalog_success
  @fixture.ensure_product_catalog
  Scenario: TSTFLO-1109 Редактирование каталога товаров при авторизации за Superadmin
    Then Проверим тестовый каталог товаров
    When Успешно редактируем тестовый каталог товаров
    Then Проверим отредактированный тестовый каталог
  
  @success @product_catalog_success
  @fixture.ensure_product_catalog
  Scenario: TSTFLO-1149 Просмотр тестового каталога товаров при авторизации за Superadmin
    Then Проверим что список каталогов не пустой
    And Проверим тестовый каталог товаров

  @success @product_catalog_success
  Scenario: TSTFLO-1111 Добавление товара в тестовый каталог товаров с последующей отправкой на согласование и согласование, при авторизации за Superadmin
    Then Проверим что список каталогов не пустой
    And Проверим тестовый каталог товаров
    When Успешно добавим тестовый товар в каталог товаров
    Then Отправим тестовый каталог товаров на согласование
    And Полностью согласуем тестовый каталог товаров
    And Проверим согласованный тестовый каталог 

  @success @import_succes @product_catalog_success
  Scenario: TSTFLO-2208 Импорт тестового файла каталога с 1 товаром
    Given Подготовлен тестовый xslx файл каталога товаров c 1 записью
    When Успешно импортируем каталог товаров в новый каталог
    Then Проверим статус импорта каталога на отсутствие ошибок
    Then Проверим импорт каталога
  
  @success @import_succes @product_catalog_success
  Scenario: TSTFLO-2208 Импорт тестового файла каталога с 5 товарами
    Given Подготовлен тестовый xslx файл каталога товаров c 5 записями
    When Успешно импортируем каталог товаров в новый каталог
    Then Проверим статус импорта каталога на отсутствие ошибок
    Then Проверим импорт каталога
  
  @success @import_succes @product_catalog_success
  @fixture.ensure_product_empty_catalog
  Scenario: TSTFLO-1492 Импорт тестового файла каталога с 5 товарами в существующий каталог созданный
    Given Подготовлен тестовый xslx файл каталога товаров c 5 записями
    When Успешно импортируем каталог товаров в созданный каталог
    Then Проверим статус импорта каталога на отсутствие ошибок
    Then Проверим импорт каталога