import logging
import sys
import json
import os.path
from behave import use_fixture
from API.terminal_system_v2 import terminalApi_v2
from fixtures import *
from API.management import ManagementApi
from API.terminal_system import terminalApi
from API.dictionary_data import dictionaryApi
from gen.gen_csv import csv_gen
from gen.gen_xml_transaction import xml_gen
from API.NKO import nkoApi
from gen.gen_exel import exel_gen
import os

def before_tag(context, tag):
    if tag == "fixture.management_super_auth":
        use_fixture(management_super_auth, context, timeout=10)
    if tag == "fixture.management_tsp_auth":
        use_fixture(management_tsp_auth, context, timeout=10)
    if tag == "fixture.management_oiv_auth":
        use_fixture(management_oiv_auth, context, timeout=10)
    if tag == "fixture.ensure_executive_authoritie_false":
        use_fixture(ensure_executive_authoritie, context, type_pseudocoail = False, timeout=10)
    if tag == "fixture.ensure_executive_authoritie_true":
        use_fixture(ensure_executive_authoritie, context, type_pseudocoail = True, timeout=10)
    if tag == "fixture.ensure_benefit_types":
        use_fixture(ensure_benefit_types, context, timeout=10)
    if tag == "fixture.ensure_social_program_false":
        use_fixture(ensure_social_program, context, social_account_nko = False,timeout=10)
    if tag == "fixture.ensure_social_program_true":
        use_fixture(ensure_social_program, context, social_account_nko = True,timeout=10)
    if tag == "fixture.ensure_merchant":
        use_fixture(ensure_merchant, context, timeout=10)
    if tag == "fixture.ensure_shop":
        use_fixture(ensure_shop, context, timeout=10)
    if tag == "fixture.ensure_terminal":
        use_fixture(ensure_terminal, context, timeout=10)
    if tag == "fixture.ensure_product_category":
        use_fixture(ensure_product_category, context, timeout=10)
    if tag == "fixture.ensure_product_catalog":
        use_fixture(ensure_product_catalog, context, timeout=10)
    if tag == "fixture.ensure_product_empty_catalog":
        use_fixture(ensure_product_empty_catalog, context, timeout=10)
    if tag == "fixture.ensure_executive_authoritie_edit_false":
        use_fixture(ensure_executive_authoritie_edit, context, type_pseudocoail = False, timeout=10)
    if tag == "fixture.ensure_executive_authoritie_edit_true":
        use_fixture(ensure_executive_authoritie_edit, context, type_pseudocoail = True, timeout=10)
    if tag == "fixture.ensure_benefit_edit":
        use_fixture(ensure_benefit_edit, context, timeout=10)
    if tag == "fixture.ensure_social_program_edit_false":
        use_fixture(ensure_social_program_edit, context, type_pseudocoail = False, timeout=10)
    if tag == "fixture.ensure_social_program_edit_true":
        use_fixture(ensure_social_program_edit, context, type_pseudocoail = True, timeout=10)
    if tag == "fixture.ensure_merchant_edit":
        use_fixture(ensure_merchant_edit, context, timeout=10)
    if tag == "fixture.ensure_shop_edit":
        use_fixture(ensure_shop_edit, context, timeout=10)
    if tag == "fixture.ensure_terminal_edit":
        use_fixture(ensure_terminal_edit, context, timeout=10)
    if tag == "fixture.ensure_category_edit":
        use_fixture(ensure_category_edit, context, timeout=10)
    if tag == "fixture.ensure_card_NKO_true":
        use_fixture(ensure_card, context, check_nko=True, timeout=10)
    if tag == "fixture.ensure_card_NKO_false":
        use_fixture(ensure_card, context, check_nko=False, timeout=10)
    if tag == "fixture.cache":
        use_fixture(cache, context, timeout=10)
    if tag == "fixture.dicktion_cache":
        use_fixture(dicktion_cache, context, timeout=10)
    if tag == "fixture.get_merchant_key":
        use_fixture(get_merchant_key, context, timeout=10)
    if tag == "fixture.generate_api_key":
        use_fixture(generate_api_key, context, timeout=10)
    if tag == "fixture.auth_tsp":
        use_fixture(auth_tsp, context, timeout=10)
    if tag == 'fixture.ensure_beneficiary':
        use_fixture(ensure_beneficiary, context, timeout=10)
    if tag == 'fixture.ensure_beneficiary_edit':
        use_fixture(ensure_beneficiary_edit, context, timeout=10)

def before_all(context):
    userdata = context.config.userdata
    stage = userdata.get('stage', 'stage').lower()
    configfile = 'appsettings.'+stage+'.json'
    assert os.path.exists(configfile), 'Конфигурационный файл {0} не найден, проверьте его наличие в корневом каталоге автотестов'.format(configfile)
    more_userdata = json.load(open(configfile, mode="r", encoding="utf-8"))
    context.config.update_userdata(more_userdata)
    context.man_url = context.config.userdata.get('url')
    context.auth_data = context.config.userdata.get('auth_managment_api')
    context.management = ManagementApi(context.config.userdata['management_url'])
    context.terminal_api = terminalApi(context.config.userdata['terminalsystem'])
    context.nko_url = nkoApi(context.config.userdata['test_nko'])
    context.dictionary_api = dictionaryApi(context.config.userdata['dictionarydata'])
    context.management_api = ManagementApi(context.config.userdata['management_url'])
    context.terminal_v2_api = terminalApi_v2(context.config.userdata['terminalsystem_v2'])
    context.gen = xml_gen()
    context.exel = exel_gen()
    context.csv = csv_gen()
    logging_level = context.config.userdata.get('logging_level')
    if (logging_level != None and logging_level.lower() == "debug"):
        context.config.setup_logging(stream=sys.stdout,level=logging.DEBUG)
    else:
        context.config.setup_logging(stream=sys.stdout,level=logging.INFO)
    context.behave_log = logging.getLogger("behave")
    context.scenarios_name = []

def before_scenario(context, scenario):
    if "@runner.continue_after_failed_step" in scenario.effective_tags:
        scenario.continue_after_failed_step = True

# def after_scenario(context, scenario):
#     context.scenarios_name.append(context.scenario.name)

# def after_all(context):
#     for entry in os.listdir(context.config.junit_directory):
#         result = json.load(open(context.config.junit_directory+'/'+entry, mode="r", encoding="utf-8"))
#         if result['name'] not in context.scenarios_name:
#             os.remove(context.config.junit_directory+'/'+entry)