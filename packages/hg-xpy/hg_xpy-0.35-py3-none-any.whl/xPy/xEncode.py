# coding=utf-8
'''
Date: 2023-02-28
Description: 
LastEditTime: 2023-03-03
LastEditors: xushuwei
'''
import chardet
import logging
import codecs
from chardet.universaldetector import UniversalDetector


def GetCharset(filePath: str):
    with open(filePath, "rb") as f:
        data = f.read()
        charset = chardet.detect(data)['encoding']
    if charset == 'ascii':
        return 'gbk'
    return charset


def GetCharsetSlow(file_path):
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


def GetFileContent(filePath: str):
    old_encoding = GetCharset(filePath)
    content = ''
    try:
        fd = open(filePath, "r", encoding=old_encoding)
        content = fd.read()
        fd.close()
    except Exception as e:
        raise (e)
        return '', ''
    return content, old_encoding


def Convert2Utf8(filename: str) -> bool:
    content, old_encoding = GetFileContent(filename)
    if old_encoding == None:
        logging.warn(f'detect encoding fail:{filename}')
        return False

    if old_encoding == 'utf-8':
        return True

    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write(content)
    return True
