import re
import time

from ats_base.common import func
from ats_base.log.logger import logger
from ats_base.service import app, pro, acd

from ats_case.case.context import Context
from ats_case.common.enum import ProClazz, OperationClazz
from ats_case.common.error import APIError

"""
    常用操作命令
"""


def send(context: Context, todo: dict, types=2, retry_times: int = 3):
    """
    发送操作命令 - 向测试端app
    :param context:         上下文
    :param todo:            任务
    :param types:
    :param retry_times:     失败重试次数（默认：3次）
    :return:
    """
    result = None

    try:
        data = {
            'type': types,
            'exec_time': func.sys_current_time(),
            'test_sn': context.test_sn,
            'case_id': context.case.id,
            'meter_pos': context.meter.pos,
            'step_id': context.runtime.step,
            'todo': todo
        }

        logger.info('~ @TCC-SEND-> client:{} data:{}'.format(context.tester.api, data))
        result = app.send(context.tester.api, data)
        logger.info('~ @TCC-SEND<- result:{}'.format(result))
    # except requests.exceptions.MissingSchema as me:
    #     logger.error(str(me))
    #     raise AssertionError(str(me))
    except Exception as ae:
        logger.error(str(ae))

        retry_times -= 1
        if retry_times <= 0:
            raise APIError(context.tester.api)
        else:
            sleep(5)
            send(context, todo, types, retry_times)

    return result


def sleep(seconds: float):
    """
    休眠
    :param seconds:     秒
    :return:
    """
    logger.info('~ @TCC-SLEEP-> {}secs'.format(seconds))
    time.sleep(seconds)


def offbench(context: Context, disabled=1):
    """
    脱表台
    :param context:
    :param disabled:     秒
    :return:
    """
    clazz = OperationClazz(context.case.steps[str(context.runtime.step)].get('type'))

    if disabled == 1:
        if clazz == OperationClazz.BENCH:
            return True

    return False


def cache(context: Context, data):
    """
    缓存
    :param context:
    :param data:
    :return:
    """
    pass


"""
    通讯协议篇
"""


def meter(protocol: str):
    return Meter(protocol)


class Meter(object):
    def __init__(self, protocol):
        self._protocol = ProClazz(protocol)
        self._comm_addr = None
        self._operation = None
        self._element = None
        self._parameter = None
        self._frame = None
        self._func = None
        self._func_module = None
        self._func_parameter = {}

    def comm_addr(self, addr: str):
        self._comm_addr = addr
        return self

    def operation(self, key: str):
        self._operation = key
        return self

    def element(self, di: str):
        self._element = di
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def frame(self, hexStr: str):
        self._frame = hexStr
        return self

    def encode(self):
        logger.info(
            '~ @PRO-ENCODE-> protocol:{} comm_addr:{} operation:{} element:{}'.format(self._protocol,
                                                                                      self._comm_addr,
                                                                                      self._operation,
                                                                                      self._element))
        parse = pro.encode(func.to_dict(protocol=self._protocol.name, comm_addr=self._comm_addr,
                                        operation=self._operation, element=self._element, parameter=self._parameter))
        logger.info('~ @PRO-ENCODE<- protocol:{} frame:{}'.format(self._protocol, parse.get('frame')))

        return parse.get('frame')

    def decode(self):
        logger.info('~ @PRO-DECODE-> protocol:{} frame:{}'.format(self._protocol, self._frame))
        data = pro.decode(func.to_dict(protocol=self._protocol.name, frame=self._frame))
        logger.info('~ @PRO-DECODE<- protocol:{} parse:{}'.format(self._protocol, data))

        return data.get('parse').get('link_data').get('mission').get('result')

    def function(self, data):
        self._func = data.get('code')
        self._func_module = data.get('module')
        self._func_parameter = data.get('parameter', {})

        return self

    def acv(self):
        logger.info('~ @ACD-HANDLE-> module:{} function:{} parameter:{}'.format(
            self._func_module, self._func, self._func_parameter))
        result = acd.handle(module=self._func_module, function=self._func, data=self._func_parameter)
        logger.info('~ @ACD-HANDLE<- module:{} function:{} result:{}'.format(self._func_module, self._func, result))

        return result

    def exec(self, context: Context):
        self._frame = self.encode()

        result = send(context,
                      todo={'meter:comm': {'channel': {'type': 'RS485', 'baudrate': 9600}, 'frame': self._frame}})

        self._frame = result.get('result')

        self._func_parameter['return_result'] = self.decode()

        fps = str(self._func_parameter)
        re_list = re.findall(r"#(.+?)\'", fps)
        for r in re_list:
            v = eval(r)
            fps = fps.replace('#{}'.format(r), v)

        self._func_parameter = eval(fps)

        send(context, todo={'app:show': {'msg': self.acv()}})


"""
    加密机篇
"""


def encrypt(clazz: str):
    pass


class Encryptor(object):
    def __init__(self, clazz):
        self._clazz = clazz
        pass

    def operation(self, key: str):
        pass

    def parameter(self, **param):
        pass

    def exec(self):
        pass


"""
    表台篇
"""


def bench(manufacture: str):
    pass


class Bench(object):
    def __init__(self, manufacture):
        self._manufacture = manufacture
        self._operation = None
        self._parameter = None
        self._command = None
        self._result = None

    def operation(self, command: str):
        self._operation = command
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def encode(self):
        logger.info(
            '~ @BENCH-> manufacture:{} operation:{} parameter:{}'.format(self._manufacture, self._operation,
                                                                         self._parameter))
        self._command = {'{}'.format(self._operation): self._parameter}

        return self._command

    def decode(self):
        logger.info('~ @BENCH<- manufacture:{} operation:{} result:{}'.format(self._manufacture,
                                                                              self._operation, self._result))

        return self._result

    def exec(self, context: Context):
        self.encode()
        result = send(context, todo=self._command)
        self._result = result.get('result')

        return self.decode()


"""
    测试终端篇
"""


def client():
    return App()


class App(object):
    def __init__(self):
        self._name = 'app'
        self._operation = None
        self._message = None
        self._parameter = None
        self._command = None

    def operation(self, command: str):
        self._operation = command
        return self

    def message(self, msg: str):
        self._message = msg
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def encode(self):
        logger.info('~ @APP-> operation:{} message:{}'.format(self._operation, self._message))
        self._command = {'{}:{}'.format(self._name, self._operation): self._message}

        return self._command

    def decode(self):
        pass

    def exec(self, context: Context):
        self.encode()
        send(context, todo=self._command)


"""
    平台篇
"""


def ats():
    return ATS()


class ATS(object):
    def __init__(self):
        self._name = 'ats'
        self._operation = None
        self._parameter = None

    def operation(self, command: str):
        self._operation = command
        return self

    def parameter(self, param=None):
        self._parameter = param
        return self

    def exec(self, context: Context):
        logger.info('~ @ATS-> operation:{} parameter:{}'.format(self._operation, self._parameter))
        return eval('{}(context, {})'.format(self._operation, self._parameter))
