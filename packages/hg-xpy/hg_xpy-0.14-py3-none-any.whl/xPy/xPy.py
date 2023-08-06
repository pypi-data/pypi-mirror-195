import platform
import subprocess
import sys
import time
import shutil
import os
import logging
import stat

try:
    sys.path.append('./')
    import xString
except Exception:
    import func.xString as xString
finally:
    pass

# 实时输出但不可显示彩色，可以返回结果


def GetCharset(file_path):
    import chardet
    from chardet.universaldetector import UniversalDetector
    with open(file_path, "rb") as f:
        data = f.read(1024)
        charset = chardet.detect(data)['encoding']
    if charset == 'ascii':
        return 'gbk'
    return charset


def GetCharsetSlow(file_path):
    import chardet
    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector()
    detector.reset()
    for each in open(file_path, 'rb'):
        detector.feed(each)
        if detector.done:
            break
    detector.close()
    enc = detector.result['encoding']
    if enc is None:
        logging.error('%s charset is None' % file_path)
    return enc


def cmd(command, print_msg=True, print_cmd=True, env=None):
    if print_cmd:
        show_msg(command)
    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    lines = []
    for line in iter(p.stdout.readline, b''):
        try:
            line = line.rstrip().decode('utf8')
        except:
            line = line.rstrip().decode('gbk')

        if print_msg:
            show_msg(line, False)
        lines.append(line)
    p.wait()
    # print('p.returncode=%d' % p.returncode)
    ret = None if p.returncode == 0 else p.returncode
    return lines, ret


def pause(str):
    show_msg(str)
    if is_win():
        os.system("pause")
    else:
        os.system('read -p "按任意键继续！"')


def cmd_e(command, print_msg=True):
    _, retcode = cmd(command, print_msg)
    if retcode == 0 or retcode == None:
        return 0

    if retcode != None:
        pause("发生错误")
        raise Exception('执行命令失败了:%s' % command)

    return retcode


def my_mkdirs(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


def my_mkdir(target_dir):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)


class MyDir:
    @ staticmethod
    def DelEndFlag(m):
        if(len(m) <= 1):
            return m
        if m.endswith('/') or m.endswith('\\'):
            return m[0:len(m)-1]
        return m

    @ staticmethod
    def AddEndFlag(m):
        if not (m.endswith('/') or m.endswith('\\')):
            m += '/'
        return m


class FileFilter:
    @ staticmethod
    def SplitList(include=[]):
        path_lst = []
        file_lst = []
        # 所有\或者/结尾的认为是目录
        for m in include:
            if m.endswith('/') or m.endswith('\\'):
                v = m[0:len(m)-1]
                path_lst.append(MyDir.DelEndFlag(v))
            else:
                file_lst.append(m)
        return file_lst, path_lst

    @ staticmethod
    def IsMatchFile(str, include=[]):
        for m in include:
            if m in str:
                return True
        return False

    @ staticmethod
    def IsMatchDir(str, include=[]):
        str = MyDir.DelEndFlag(str)
        for m in include:
            m = MyDir.DelEndFlag(m)
            if m in str:
                return True
        return False


class Explorer:
    @ staticmethod
    def Open(path, select_file):
        cmd = 'explorer /select,"%s\\%s"' % (
            path.replace('/', '\\'), select_file)
        # print(cmd)
        os.system(cmd)


class MyFile:
    # 根据给定条件，查找匹配到的第一个文件
    @staticmethod
    def FindFile(path, include=[]):
        for f in os.listdir(path):
            if FileFilter.IsMatchFile(f, include):
                return os.path.join(path, f)
        return ''


def del_file(path):
    # 可删除文件和文件夹
    if(os.path.isdir(path)):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


def copy_files(src_dir, files, target_dir):
    target_dir = MyDir.AddEndFlag(target_dir)
    my_mkdirs(target_dir)
    for f in files:
        file_path = os.path.join(src_dir, f)
        shutil.copy(file_path, target_dir)


def copy_dir(src_dir, target_dir, include=[], exclude=[]):
    return _my_copy_dir(src_dir, target_dir, include, exclude)


def _my_copy_dir(src_dir, target_dir, include=[], exclude=[], bDirOK=False):
    if not src_dir.endswith('\\') and not src_dir.endswith('/'):
        # 如果src_dir不以/结尾，则会复制到target_dir/src_dir目录名
        b = os.path.basename(src_dir)
        target_dir = os.path.join(target_dir, b)
    if not os.path.isdir(src_dir):
        show_msg("copy_dir({}) not exists".format(src_dir))
        return False

    file_include_list, path_include_list = FileFilter.SplitList(include)
    file_exclude_list, path_exclude_list = FileFilter.SplitList(exclude)
    bCreateDir = False
    for files in os.listdir(src_dir):
        file_name = os.path.join(src_dir, files)
        target_path = os.path.join(target_dir, files)
        if os.path.isfile(file_name):
            if (len(file_include_list) <= 0 and len(path_include_list) > 0 and not bDirOK):
                # 没有文件包含规则，但是有目录包含规则，就需要额外判断目录
                continue
            if(len(file_include_list) > 0 and (not FileFilter.IsMatchFile(file_name, file_include_list))):
                continue
            if FileFilter.IsMatchFile(file_name, file_exclude_list):
                continue
            if not bCreateDir:
                my_mkdirs(target_dir)
                bCreateDir = True
                show_msg("copy_dir({},{},{},{})".format(
                    src_dir, target_dir, include, exclude))

            shutil.copy(file_name, target_path)
            show_msg(file_name + "\t==>\t" + target_path)
        else:
            if (len(path_include_list) > 0 and (not FileFilter.IsMatchDir(file_name, path_include_list))):
                continue
            if FileFilter.IsMatchDir(file_name, path_exclude_list):
                continue
            # if not os.path.isdir(file_name):
            #     my_mkdirs(file_name)
            if not file_name.endswith('\\') and not file_name.endswith('/'):
                file_name += '/'
            _my_copy_dir(file_name, target_path, include, exclude, True)
    return True


def is_win():
    return ("Windows" in platform.platform())


def is_root():
    import ctypes
    return ctypes.windll.shell32.IsUserAnAdmin()


class MySvn:
    @staticmethod
    def Update(path):
        cmd('svn update "{}"'.format(path))


def show_msg(str, t=True):
    try:
        if(t):
            print("%s\t%s" % (time.strftime("%H:%M:%S", time.localtime()), str))
        else:
            print(str)
    except:
        pass


class Timer:
    def __init__(self):
        self.Start()

    def Start(self):
        self.start = time.time()

    def GetPass(self):
        self.end = time.time()
        return '%d:%d' % ((self.end - self.start)/60, (self.end - self.start) % 60)


def CreateQuickLaunchPy(path):
    if(not os.path.exists(path)):
        logging.error('%s not exists' % path)
        return False

    file_name = os.path.basename(path)
    file_name, _ = os.path.splitext(file_name)
    if is_win():
        file_name += '.bat'
    else:
        file_name += '.sh'
    if(os.path.exists(file_name)):
        os.remove(file_name)
    logging.info('%s create success' % file_name)
    fp = open(file_name, 'w')
    if is_win():
        fp.write(
            'cd /d %%~dp0 && echo ================================= && python %s %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9' % path)
    else:
        fp.write(
            '#!/bin/bash\ncd "$(dirname "$0")" && echo ================================= && python %s "$@"' % path)

    fp.close()
    os.chmod(file_name, stat.S_IRWXU)
    return True


def IsInstalled(tool: str):
    cmd = "where" if platform.system() == "Windows" else "which"
    return cmd_retcode(cmd + ' ' + tool)


def cmd_retcode(cmd):
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = proc.communicate()

    sys.stdout.write(xString.DecodeByte(output))
    if len(err) > 0:
        sys.stdout.flush()
        sys.stderr.write(xString.DecodeByte(err))
    return len(err) <= 0 or proc.returncode == 0


if __name__ == "__main__":
    # copy_dir('D:/xsw/code_gs/ml2/ml2_trunk/ModuleRes',
    #          'D:/xsw/code_gs/ml2/ml2_trunk/wb/ml2_trunk_20210528_1947', ['1.cq_clear.sql'])
    # path = 'd:/xsw/code_gs/ml2/ml2_trunk/x64_Temp/tmp_ml2_trunk_Visual Studio 16 2019_Debug'
    # f = MyFile.FindFile(path, ['.sln'])
    # Explorer.Open(path, os.path.basename(f))

    pass