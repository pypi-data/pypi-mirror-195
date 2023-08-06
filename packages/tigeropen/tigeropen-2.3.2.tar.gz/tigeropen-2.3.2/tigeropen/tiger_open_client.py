# -*- coding: utf-8 -*-
"""
Created on 2018/9/20

@author: gaoan
"""
import datetime
import json
import logging
import uuid
from threading import Timer

import backoff

from tigeropen import __VERSION__
from tigeropen.common.consts import OPEN_API_SERVICE_VERSION, THREAD_LOCAL
from tigeropen.common.consts.params import P_TIMESTAMP, P_TIGER_ID, P_METHOD, P_CHARSET, P_VERSION, P_SIGN_TYPE, \
    P_DEVICE_ID, P_NOTIFY_URL, COMMON_PARAM_KEYS, P_SIGN
from tigeropen.common.consts.service_types import USER_LICENSE, PLACE_ORDER, CANCEL_ORDER, MODIFY_ORDER, \
    USER_TOKEN_REFRESH
from tigeropen.common.exceptions import ResponseException, RequestException
from tigeropen.common.request import OpenApiRequest
from tigeropen.common.response import TigerResponse
from tigeropen.common.util.common_utils import has_value
from tigeropen.common.util.signature_utils import get_sign_content, sign_with_rsa, verify_with_rsa
from tigeropen.common.util.web_utils import do_post

try:
    from getmac import get_mac_address
except ImportError:
    def get_mac_address():
        return ':'.join(("%012x" % uuid.getnode())[i:i + 2] for i in range(0, 12, 2))

LOG_FORMATTER = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
SKIP_RETRY_SERVICES = {PLACE_ORDER, CANCEL_ORDER, MODIFY_ORDER}


_SCHEDULE_STATE = {'is_running': False}


class TigerOpenClient:
    """
    client_config：客户端配置，包含tiger_id、应用私钥、老虎公钥等
    logger：日志对象，客户端执行信息会通过此日志对象输出
    """
    def __init__(self, client_config, logger=None):
        self.__config = client_config
        if not client_config.private_key:
            raise Exception('private key can not be empty')
        if not client_config.tiger_id:
            raise Exception('tiger id can not be empty')
        if logger:
            if client_config.log_level:
                logger.setLevel(logging.getLevelName(client_config.log_level))
            if client_config.log_path:
                file_handler = logging.FileHandler(client_config.log_path)
                file_handler.setFormatter(LOG_FORMATTER)
                logger.addHandler(file_handler)
            self.__logger = logger
        self.__headers = {
            'Content-type': 'application/json;charset=' + self.__config.charset,
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
            "User-Agent": 'openapi-python-sdk-' + __VERSION__
        }
        self.__device_id = self.__get_device_id()
        self.__init_license()
        self.__refresh_server_info()
        if self.__config.token and self.__config.license:
            self.__schedule_thread()

    def __init_license(self):
        if self.__config.license is None and self.__config.enable_dynamic_domain:
            self.__config.license = self.query_license()

    def __refresh_server_info(self):
        self.__config.refresh_server_info()


    """
    内部方法，从params中抽取公共参数
    """

    def __get_common_params(self, params):
        common_params = dict()
        common_params[P_TIMESTAMP] = params[P_TIMESTAMP]
        common_params[P_TIGER_ID] = self.__config.tiger_id
        common_params[P_METHOD] = params[P_METHOD]
        common_params[P_CHARSET] = self.__config.charset
        common_params[P_VERSION] = params[P_VERSION] if params.get(P_VERSION) is not None else OPEN_API_SERVICE_VERSION
        common_params[P_SIGN_TYPE] = self.__config.sign_type
        common_params[P_DEVICE_ID] = self.__device_id
        if has_value(params, P_NOTIFY_URL):
            common_params[P_NOTIFY_URL] = params[P_NOTIFY_URL]
        return common_params

    @staticmethod
    def __get_device_id():
        """
        获取mac地址作为device_id
        :return:
        """
        try:
            return get_mac_address()
        except:
            return None

    """
    内部方法，从params中移除公共参数
    """
    def __remove_common_params(self, params):
        if not params:
            return
        for k in COMMON_PARAM_KEYS:
            if k in params:
                params.pop(k)

    """
    内部方法，通过请求request对象构造请求查询字符串和业务参数
    """
    def __prepare_request(self, request, url=''):
        THREAD_LOCAL.logger = self.__logger
        params = request.get_params()
        params[P_TIMESTAMP] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        common_params = self.__get_common_params(params)
        all_params = dict()
        all_params.update(params)
        all_params.update(common_params)
        sign_content = get_sign_content(all_params)
        try:
            sign = sign_with_rsa(self.__config.private_key, sign_content, self.__config.charset)
        except Exception as e:
            raise RequestException('[' + THREAD_LOCAL.uuid + ']request sign failed. ' + str(e))
        all_params[P_SIGN] = sign

        log_url = url + '?' + sign_content + "&sign=" + sign
        if THREAD_LOCAL.logger:
            THREAD_LOCAL.logger.debug('[' + THREAD_LOCAL.uuid + ']request:' + log_url)

        return all_params

    """
    内部方法，解析请求返回结果并做验签
    """

    def __parse_response(self, response_str, timestamp=None):
        response_str = response_str.decode(self.__config.charset)
        if THREAD_LOCAL.logger:
            THREAD_LOCAL.logger.debug('[' + THREAD_LOCAL.uuid + ']response:' + response_str)

        response_content = json.loads(response_str)

        if not self.__config.tiger_public_key or 'sign' not in response_content or not timestamp:
            return response_content

        sign = response_content.get('sign')

        try:
            verify_res = verify_with_rsa(self.__config.tiger_public_key, timestamp.encode('utf-8'),
                                         sign.encode('utf-8'))
        except Exception as e:
            raise ResponseException('[' + THREAD_LOCAL.uuid + ']response sign verify failed. ' + str(e) + ' '
                                    + response_str)
        if not verify_res:
            raise ResponseException('[' + THREAD_LOCAL.uuid + ']response sign verify failed. ' + response_str)

        return response_content

    def _update_header(self):
        self.__headers['Authorization'] = self.__config.token

    def _get_retry_deco(self, service):
        if service not in SKIP_RETRY_SERVICES and self.__config.retry_max_tries > 0:
            return backoff.on_exception(backoff.fibo,
                                        (RequestException, ResponseException),
                                        max_time=self.__config.retry_max_time,
                                        max_tries=self.__config.retry_max_tries,
                                        logger=self.__logger,
                                        on_giveup=lambda x: self.__logger.error(f'give up after '
                                                                                f'{self.__config.retry_max_tries} retries'),
                                        jitter=None)
        return None

    """
    执行接口请求
    """
    def execute(self, request, url=None):
        if self.__config.token:
            self._update_header()
        if url is None:
            url = self.__config.server_url
        THREAD_LOCAL.uuid = str(uuid.uuid1())
        query_string = None
        params = self.__prepare_request(request, url)

        retry_deco = self._get_retry_deco(request._method)
        if retry_deco is not None:
            response = retry_deco(do_post)(url, query_string, self.__headers, params, self.__config.timeout,
                               self.__config.charset)
        else:
            response = do_post(url, query_string, self.__headers, params, self.__config.timeout,
                               self.__config.charset)
        return self.__parse_response(response, params.get('timestamp'))

    def query_license(self):
        request = OpenApiRequest(method=USER_LICENSE)

        response_content = None
        try:
            response_content = self.execute(request)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
        if response_content:
            response = TigerResponse()
            response.parse_response_content(response_content)
            if response.is_success():
                return json.loads(response.data).get('license')
        self.__logger.error(f"failed to query license, response: {response_content}")

    def query_token(self):
        request = OpenApiRequest(method=USER_TOKEN_REFRESH)

        response_content = None
        try:
            response_content = self.execute(request)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
        if response_content:
            response = TigerResponse()
            response.parse_response_content(response_content)
            if response.is_success():
                return json.loads(response.data).get('token')
        self.__logger.error(f"failed to refresh token, response: {response_content}")
        return None

    def refresh_token(self):
        new_token = self.query_token()
        if new_token:
            self.__logger.info(f"refresh token, old:{self.__config.token}, new:{new_token}")
            self.__config.load_or_store_token(new_token)

    def __token_refresh_task(self):
        try:
            if self.__config.should_token_refresh():
                self.refresh_token()
        except Exception as e:
            self.__logger.error(e, exc_info=True)

    def __schedule_thread(self):
        if not _SCHEDULE_STATE['is_running'] and self.__config.token_refresh_duration != 0:
            _SCHEDULE_STATE['is_running'] = True
            self.__logger.info('Starting schedule thread...')
            daemon = RepeatTimer(self.__config.token_check_interval, self.__token_refresh_task)
            daemon.daemon = True
            daemon.start()


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)