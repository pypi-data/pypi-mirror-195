# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:42:40
# @Author  : Pane Li
# @File    : tools.py
"""
tools

"""
import logging
import os.path
import subprocess
import time
import datetime
import pytz
import requests
from inhandtest.file import file_hash


def loop_inspector(flag='status', timeout=90, interval=5, assertion=True):
    """装饰器，期望接收函数返回的值为True，如果为False时进行轮询，直至超时失败，如果正确就退出

    :param flag:  功能名称，用以输出日志，如果不填  默认为’状态’二字
    :param timeout:  循环检测超时时间
    :param interval:  循环检测时间间隔
    :param assertion: 默认期望断言，如果为False时 返回值
    :return:  assertion为False时，返回函数的值
    """

    def timeout_(func):
        def inspector(*args, **kwargs):
            for i in range(0, timeout + 1, interval):
                result = func(*args, **kwargs)
                if not result:
                    logging.info(f'{flag} assert failure, wait for {interval}s inspection')
                    time.sleep(interval)
                    continue
                else:
                    logging.info(f'{flag} assert normal')
                    return result
            else:
                if assertion:
                    raise AssertionError(f'{flag} assert timeout failure')

        return inspector

    return timeout_


def dict_merge(*dicts):
    """合并多个字典

    :param dicts:
    :return:
    """
    result = {}
    for dict_ in dicts:
        if dict_ is not None:
            result.update(dict_)
    return result


def dict_flatten(in_dict, separator=":", dict_out=None, parent_key=None):
    """ 平铺字典

    :param in_dict: 输入的字典
    :param separator: 连接符号
    :param dict_out:
    :param parent_key:
    :return: dict
    """
    if dict_out is None:
        dict_out = {}

    for k, v in in_dict.items():
        k = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            dict_flatten(in_dict=v, dict_out=dict_out, parent_key=k)
            continue

        dict_out[k] = v

    return dict_out


def timezone_change(time_str, src_timezone, dst_timezone=None, time_format=None):
    """
    将任一时区的时间转换成指定时区的时间
    如果没有指定目的时区，则默认转换成当地时区  时区参考https://www.beijing-time.org/shiqu/

    :param time_str:
    :param src_timezone: 要转换的源时区，如"Asia/Shanghai" 即东八区， 'Europe/London' 零时区  'Canada/Eastern' 西五区 UTC-5
    :param dst_timezone: 要转换的目的时区，如"Asia/Shanghai", 如果没有指定目的时区，则默认转换成当地时区
    :param time_format: 默认格式"%Y-%m-%d %H:%M:%S"
    :return: str, 字符串时间格式
    """
    if not time_format:
        time_format = "%Y-%m-%d %H:%M:%S"

    # 将字符串时间格式转换成datetime形式
    old_dt = datetime.datetime.strptime(time_str, time_format)

    # 将源时区的datetime形式转换成GMT时区(UTC+0)的datetime形式
    dt = pytz.timezone(src_timezone).localize(old_dt)
    utc_dt = pytz.utc.normalize(dt.astimezone(pytz.utc))

    # 将GMT时区的datetime形式转换成指定的目的时区的datetime形式
    if dst_timezone:
        _timezone = pytz.timezone(dst_timezone)
        new_dt = _timezone.normalize(utc_dt.astimezone(_timezone))
    else:
        # 未指定目的时间，默认转换成当地时区
        new_dt = utc_dt.astimezone()
    # 转换成字符串时间格式
    return new_dt.strftime(time_format)


def check_windows_process(process: str or int or list, kill=False) -> bool or list:
    """ 检测进程是否运行
    :param process: str|int|list, 进程名称或进程pid(不一定是应用程序名称！), eg:'3CDaemon'|'mosquitto'|49040 如果有多个时使用list传入
    :param kill: True|False 当为True时，将检测到的进程杀死
    :return: boolean
    """

    def _search(process_):
        if process_:
            if isinstance(process_, str) or isinstance(process_, int):
                command = f'tasklist |findstr {process_}'
            else:
                raise Exception("not support process type")
            logging.info(command)
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
            task_result = p.communicate()[0]
            logging.info(f'find {process_} process is: {task_result}')
            if task_result:
                return True
            else:
                return False
        else:
            return False

    if not kill:
        if isinstance(process, list):
            return [_search(name_) for name_ in process]
        else:
            return _search(process)
    else:
        process = process if isinstance(process, list) else [process]
        [_search(name_) for name_ in process]
        for name_ in process:
            if isinstance(name_, str):
                p = subprocess.Popen(f'taskkill /F /IM {name_}', shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='gbk')
            elif isinstance(name_, int):
                p = subprocess.Popen(f'taskkill /pid {name_} /F', shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='gbk')
            else:
                raise Exception("not support process type")
            logging.info(p.communicate()[0])


def download_svn_firmware(svn: dict, file_path, check_firmware=True):
    """

    :param svn: dict {'url': $url, 'username': $username, 'password': $password} 固件全路径
    :param file_path: 本地存放固件文件夹路径
    :param check_firmware: True|False 支持下载完文件后校验文件正确性
    :return:
    """
    from requests.auth import HTTPBasicAuth
    from requests.adapters import HTTPAdapter

    if svn.get("url") and svn.get('username') and svn.get('password') and file_path:
        url_path = svn.get("url")
        firmware_name = url_path.split('/')[-1]
        local_firmware_path = os.path.join(file_path, firmware_name)
        svn_hash_file_path = url_path.replace(firmware_name, 'sha256.txt')
        auth = HTTPBasicAuth(svn.get('username'), svn.get('password'))
        if not os.path.isfile(local_firmware_path):
            logging.info(f"download {local_firmware_path} from svn and wait for a moment!")
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))  # 本身请求失败会重试3次
            for i in range(3):  # 文件下载错误再继续下载
                r = s.get(url_path, auth=auth)
                if r.status_code == 401:
                    raise Exception("svn username or password error")
                elif r.status_code == 200:
                    with open(local_firmware_path, 'wb') as fi_:  # 覆盖写入
                        fi_.write(r.content)
                    r_hash_file = s.get(svn_hash_file_path, auth=auth)
                    if check_firmware:
                        for co_ in r_hash_file.content.split(b'\n'):
                            if co_.decode('utf-8').endswith(firmware_name):
                                hash_sha256_value = co_.decode('utf-8').split(' ')[0].upper()
                                break
                        else:
                            raise Exception(f'{svn_hash_file_path} not contain {firmware_name} hash_sha256 value')
                        if file_hash(local_firmware_path, 'sha256') == hash_sha256_value:
                            logging.info(f'{local_firmware_path} download success')
                            break
                        else:
                            logging.warning(f'download firmware failed, try {i+1} time')
                else:
                    raise Exception("svn server down error")
            else:
                raise Exception('download firmware failed')


if __name__ == '__main__':
    import sys

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO,
                        stream=sys.stdout)
    # print(timezone_change('2022-02-18 13:39:32', 'Canada/Eastern', 'Asia/Shanghai'))
    # print(check_windows_process('mosquitto.exe', kill=False))
    download_svn_firmware(
        svn={'url': 'http://10.5.1.121/svn/Manufacture/beta/VG710/V1.2.1.r30052/VG7-V1.2.1.r30052.bin',
             'username': 'liwei', 'password': 'liwei'}, file_path='D:\Python_project\pypi_common')
