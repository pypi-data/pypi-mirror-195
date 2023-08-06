import pytest

from ats_case.case.context import Context


def pytest_addoption(parser):
    """
    命令行pytest传递的参数
    :param parser:
    :return:
    """
    parser.addoption(
        "--sn",
        default="",
        help="script sequence number"
    )
    parser.addoption(
        "--cid",
        default="",
        help="case id"
    )
    parser.addoption(
        "--rerun",
        default="",
        help="break then run"
    )


@pytest.fixture(scope='session')
def sn(request):
    """
    当前测试序列号
    :param request:
    :return:
    """
    return request.config.getoption("--sn")


@pytest.fixture(scope='session')
def cid(request):
    """
    当前测试序列号
    :param request:
    :return:
    """
    return request.config.getoption("--cid")


@pytest.fixture(scope='session')
def rerun(request):
    """
    断点重运行
    :param request:
    :return:
    """
    return request.config.getoption("--rerun")


@pytest.fixture(scope='session', autouse=True)
def CaseContext(sn, cid, rerun):
    """
    测试用例上下文
    :param sn:
    :param cid:
    :param rerun:
    :return:
    """
    return Context(sn, cid, rerun)
