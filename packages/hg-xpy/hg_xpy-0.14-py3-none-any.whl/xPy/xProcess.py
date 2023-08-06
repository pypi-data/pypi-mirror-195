import sys
import os
sys.path.append('./')
import psutil  # 导入模块

class Process:
    # 找到第一个匹配的进程则返回true，cmd_line部分匹配
    @staticmethod
    def IsExistByCmdLine(exe_name, cmd_line):
        for pid in psutil.pids():
            p = psutil.Process(pid)
            s = os.path.basename(p.name())
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
    #         s = os.path.basename(p.name())
    #         if not s == exe_name:
    #             continue
    #         for c in p.cmdline():
    #             if not cmd_line in c:
    #                 continue
    #             return True
    #     return False


if __name__ == "__main__":
    print(Process.IsExistByCmdLine('devenv.exe', 'ml2-'))
