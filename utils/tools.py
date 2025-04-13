
import json
import re

import requests

from django.contrib.auth import get_user_model
Users = get_user_model()

from utils.custom_log   import log_start
logger = log_start('utils')

def get_request_ip(request):
    """
    获取请求用户IP
    :param request: request请求对象
    :return: ip
    """
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


def get_ip_address(ip):
    """
    获取IP所在地理位置 (耗时操作暂未使用, 后续可能考虑celery)
    :param ip: ip地址
    :return: address位置信息
    """
    res = requests.request('get', f'http://ip-api.com/json/{ip}')
    if res.status_code == 200:
        dict_data = json.loads(res.text)
        country = dict_data.get('country')
        region_name = dict_data.get('regionName')
        city = dict_data.get('city')
        address = country + ' ' + region_name + ' ' + city
    else:
        address = '未知'
    return address


def get_request_browser(request):
    """
    获取请求用户浏览器信息
    :param request: request请求对象
    :return: 浏览器信息
    """
    family = request.user_agent.browser.family
    version_string = request.user_agent.browser.version_string
    return family + ' ' + version_string


def get_request_os(request):
    """
    获取请求用户系统信息
    :param request: request请求对象
    :return: 系统信息
    """
    family = request.user_agent.os.family
    version_string = request.user_agent.os.version_string
    return family + ' ' + version_string
