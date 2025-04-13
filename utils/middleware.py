
import json
import time

from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.response import Response
from utils.tools import get_request_browser, get_request_os, get_request_ip
from utils.custom_log  import log_start


class ResponseMiddleware(MiddlewareMixin):
    """
    自定义响应数据格式
    """
    


    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_exception(self, request, exception):
        pass

    def process_response(self, request, response):

        if isinstance(response, Response) and response.get('content-type') == 'application/json':
            if response.status_code >= 400:
                msg = '请求失败'
                if isinstance(response.data, dict):
                    if response.data.get('non_field_errors') :
                        detail = response.data.get('non_field_errors')
                    elif response.data.get('detail') :
                        detail = response.data.get('detail')
                    else:
                        detail = response.data
                else:
                    detail = "其他错误" + response.data
                
                code = 10000
                data = {}

            elif response.status_code == 200 or response.status_code == 201:
                msg = 'success'
                detail = ''
                code = 20000
                data = response.data
            else:
                return response
            response.data = {'msg': msg, 'errors': detail, 'code': code, 'data': data}
            response.content = response.rendered_content
        
        else:
            pass
        
        return response
    



class OperationLogMiddleware:
    """
    操作日志Log记录
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.operation_logger =  log_start('operation')  # 记录非GET操作日志
        self.query_logger = log_start('query')  # 记录GET查询操作日志

    def __call__(self, request):
        try:
            request_body = json.loads(request.body)
        except Exception:
            request_body = dict()
        if request.method == "GET":
            request_body.update(dict(request.GET))
            logger = self.query_logger
        else:
            request_body.update(dict(request.POST))
            logger = self.operation_logger
        # 处理密码, log中密码已******替代真实密码
        for key in request_body:
            if 'password' in key:
                request_body[key] = '******'
        response = self.get_response(request)
        
        try:
            response_body = response.data
            # 处理token, log中token已******替代真实token值
            if response_body['data'].get('token'):
                response_body['data']['token'] = '******'
            # info = '\n\n {}'.format(response_body)
            # logger.error(info)
        except Exception:
            response_body = dict()

        request_ip = get_request_ip(request)
        log_info = f'[{request.user}@{request_ip} [Request: {request.method} {request.path} {request_body}] ' \
                   f'[Response: {response.status_code} response_reason_phrase: {response.reason_phrase} { response_body} ]]'
        if response.status_code >= 500:
            logger.error(log_info)
        elif response.status_code >= 400:
            logger.warning(log_info)
        else:
            logger.info(log_info)
        return response