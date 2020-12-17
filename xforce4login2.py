import atApiBasicLibrary.requestLib as requestLib
import atApiBasicLibrary.jsonLib as jsonLib
import atApiBasicLibrary.log as log
import re
from atApiXforce4Login.encrypt import EncryptDate

HEADER_COOKIE='Set-Cookie'
HEADER_COOKIE_STR='x-access-token'
EXPECT_RESP_JSON_PART={"code": 1, "message": "成功"}
NAME='xforce'
_AES_KEY='Key#password%Key'

def encrypt_password(password):
    aes = EncryptDate(_AES_KEY.encode(encoding="utf-8"))  # 这里密钥的长度必须是16的倍数
    res = aes.encrypt(password)
    return res

def at_xforce4_login2(url,username,password, timeout=None, header_cookie_str=HEADER_COOKIE_STR):
    '''
    票易通4.0登录
    :param url:
    :param username:
    :param password:
    :param timeout:
    :return:
    '''
    password=encrypt_password(password)
    resp = requestLib.at_http_post_json(url, json={"username": username, "password": password}, timeout=timeout)
    status_code = requestLib.at_get_http_response_status_code(resp)
    if status_code != 200:
        raise AssertionError( NAME + "4.0登录返回码不是200")
    resp_json_body = requestLib.at_get_http_response_json_body(resp)
    jsonLib.json_contain_sub_json(EXPECT_RESP_JSON_PART, resp_json_body)
    header = requestLib.at_get_http_response_header(resp)
    if HEADER_COOKIE not in header:
        raise AssertionError( NAME + '4.0登录返回header里不存在'+HEADER_COOKIE)
    cookie = header[HEADER_COOKIE]
    if header_cookie_str + '=' not in cookie:
        raise AssertionError( NAME + '4.0登录返回header里不存在' + header_cookie_str)
    re_search = re.search(header_cookie_str + '(\S+)', cookie)
    if re_search is None:
        raise AssertionError( NAME + '4.0登录 ' + header_cookie_str + '无法通过正则获取')
    xforce_saas_token_arr = re_search.group(0).split('=')
    if len(xforce_saas_token_arr) != 2:
        raise AssertionError( NAME + '4.0登录 ' + header_cookie_str + '无法通过正则获取')
    log.info( NAME + "4.0登录成功", also_console=True, html=True)
    return {xforce_saas_token_arr[0]: xforce_saas_token_arr[1]}

def at_xforce4_client_login(url,client_id,secret,timeout=None):
    '''
    通过客户端，票易通4.0登录
    :param url:
    :param client_id:
    :param secret:
    :param timeout:
    :return:
    '''
    resp = requestLib.at_http_post_json(url, json={"clientId" : client_id,"secret" : secret}, timeout=timeout)
    status_code = requestLib.at_get_http_response_status_code(resp)
    if status_code != 200:
        raise AssertionError(NAME + "4.0客户端登录返回码不是200")
    resp_json_body=requestLib.at_get_http_response_json_body(resp)
    jsonLib.json_contain_sub_json(EXPECT_RESP_JSON_PART, resp_json_body)
    if 'data' not in resp_json_body:
        raise AssertionError(NAME + "4.0客户端登录返回json不存在data")
    return {"x-app-token" : resp_json_body['data']}

