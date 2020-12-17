from atApiBasicLibrary.supper import at_execute_many_sql
from robot.libraries.BuiltIn import _Variables
from robot.api import logger

ROBOT_LISTENER_API_VERSION = 2
test_case_result = ""
config = None
flag = True
sql_list = [

    "delete from bss_service_package where app_id not in (select app_id from bss_app)",
    "delete from sys_resourceset where app_id not in (select app_id from bss_app)",
    "delete from sys_resource where app_id not in (select app_id from bss_app)",
    "delete from sys_org_struct where tenant_id not in (select tenant_id from bss_tenant)",
    "delete from sys_org_user_rel where user_id not in (select user_id from sys_user)",
    "delete from sys_org_user_rel where tenant_id not in (select tenant_id from bss_tenant)",
    "delete from sys_user where tenant_id not in (select tenant_id from bss_tenant)",
    "delete from sys_user where account_id not in (select account_id from sys_sass_account)",
    "delete from bss_tenant_secret where tenant_id not in (select tenant_id from bss_tenant)",
    "delete from sys_role where tenant_id not in (select tenant_id from bss_tenant) and tenant_id > 0",
    "delete from sys_role_resourceset_rel where role_id not in (select role_id from sys_role)",
    "delete from sys_role_resourceset_rel where resouseset_id not in (select resourceset_id from sys_resourceset)",
    "delete from sys_resourceset_resource_rel where resourceset_id not in (select resourceset_id from sys_resourceset)",
    "delete from sys_resourceset_resource_rel where resource_id not in (select resource_id from sys_resource)",
    "delete from bss_service_resourceset_rel where service_package_id not in (select service_package_id from bss_service_package)",
    "delete from bss_service_resourceset_rel where resourceset_id not in (select resourceset_id from sys_resourceset)",
    "delete from sys_resource_api_rel where resource_id not in (select resource_id from sys_resource)",
    "delete from sys_resource_api_rel where service_api_id not in (select service_api_id from sys_service_api)",
    "delete from sys_role_user_rel where role_id not in (select role_id from sys_role)",
    "delete from sys_role_user_rel where user_id not in (select user_id from sys_user)",
    "delete from sys_sass_account where account_id not in (select account_id from sys_user)",
    "delete from sys_user_tag where user_id not in (select user_id from sys_user)",
    "delete from bss_tenant_company_rel where company_id not in (select company_id from bss_company)",
    "delete from bss_tenant_company_rel where tenant_id not in (select tenant_id from bss_tenant)",
    "delete FROM bss_company_service_rel where company_id is null",
    "delete FROM bss_company_service_rel where company_id not in (select company_id from bss_company)",
    "delete FROM bss_company_service_rel where service_package_id not in (select service_package_id from bss_service_package)"
]


def end_test(name, attrs):
    global flag
    if flag:
        try:
            variable = _Variables()
            global config
            config = variable.get_variable_value("${数据库配置}")
            flag = False
        except Exception:
            pass
    global test_case_result
    test_case_result += name + " , " + attrs['status'] + "\n"


def close():
    if config is None:
        logger.error("数据库最后没有删除", html=True)
        return
    at_execute_many_sql(sql_list, config)
    logger.info("数据库最后没有删除", html=True, also_console=True)
    global test_case_result
    report_txt = "report.txt"
    import os
    if os.path.exists(report_txt):
        import shutil
        shutil.rmtree(report_txt)
    with open('report_txt', 'a') as f:
        f.write(test_case_result)
