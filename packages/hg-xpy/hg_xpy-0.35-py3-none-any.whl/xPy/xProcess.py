
'''
Date: 2023-03-04
Description:
LastEditTime: 2023-03-04
LastEditors: xushuwei
'''
import psutil  # 导入模块
import sys
import os
from os import path
sys.path.append('./')


class Process:
    # 找到第一个匹配的进程则返回true，cmd_line部分匹配
    @staticmethod
    def IsExistByCmdLine(exe_name, cmd_line):
        for pid in psutil.pids():
            p = psutil.Process(pid)
            s = path.basename(p.name())
            if not s == exe_name:
                continue
            for c in p.cmdline():
                if not cmd_line in c:
                    continue
                return True
        return False

    # 找到第一个匹配的进程则返回true，title部分匹配
    # @staticmethod
    # def IsExistByTitle(exe_name, title):
    #     for pid in psutil.pids():
    #         p = psutil.Process(pid)
    #         s = path.basename(p.name())
    #         if not s == exe_name:
    #             continue
    #         for c in p.cmdline():
    #             if not cmd_line in c:
    #                 continue
    #             return True
    #     return False

    @staticmethod
    def IsExist(exe_name):
        for pid in psutil.pids():
            p = psutil.Process(pid)
            s = path.basename(p.name())
            if not s == exe_name:
                continue
            return True
        return False


def Run(exe_path: str, Once: bool = False, Sync: bool = True):
    if not path.exists(exe_path):
        return False
    exe_name = path.basename(exe_path)
    exe_dir = path.abspath(path.dirname(exe_path))
    if Once and Process.IsExist(exe_name):
        return True
    os.chdir(exe_dir)
    if Sync:
        os.system(exe_path)
    else:
        os.startfile(exe_path)
    return True


def NoWait(exe_path: str, Once: bool = False):
    return Run(exe_path, Once, False)


def Wait(exe_path: str, Once: bool = False):
    return Run(exe_path, Once, True)


if __name__ == "__main__":
    # print(Process.IsExistByCmdLine('devenv.exe', 'ml2-'))
    print(Run(r'D:\xsw\tools\v2rayN2\v2rayN.exe', True))
