#!/usr/bin/python3
# -*- coding:utf-8 -*-
#Author: Pang Yapeng

import datetime
import csv
from sub_common import *

# 特定参数
conf = get_conf()
LOCAL_PATH = conf.get("FTP_GET_FILE", "LOCAL_PATH")
PROCESS_FILE_PATH = conf.get("FTP_GET_FILE", "AMDB_PROCESS_INFO")
COREFILE_FILE_PATH = conf.get("FTP_GET_FILE", "AMDB_COREFILE_INFO")
PORT_FILE_PATH = conf.get("FTP_GET_FILE", "AMDB_PORT_INFO")

# 设置log
logger = get_logger("ftp-get.log")

def main():
    logger.info("Begin to ftp from AMDB ftp server!")
    ftp_getfile(PROCESS_FILE_PATH,LOCAL_PATH)
    ftp_getfile(COREFILE_FILE_PATH,LOCAL_PATH)
    ftp_getfile(PORT_FILE_PATH,LOCAL_PATH)

def ftp_getfile(FTP_FILE,LOCAL_PATH):

    #获取文件名称
    v_date_para = re.findall(r"\[(.*)\]", FTP_FILE)[0]
    new_date = datetime.datetime.now().strftime(v_date_para)
    FTP_FILE_NEW = re.sub("\[.*\]", new_date, FTP_FILE)

    #本地文件全路径
    filename = os.path.basename(FTP_FILE_NEW)
    filename_full = os.path.join(LOCAL_PATH,filename)
    filename_full = os.path.abspath(filename_full).replace('\\','/')

    # 从服务器获取文件
    try:
        ftp = get_amdb_ftp()
    except:
        logger.info("Connect ftp server failed !")
        return False

    with open(filename_full, "wb") as handle:
        try:
            ftp.retrbinary("RETR %s" % FTP_FILE_NEW, handle.write, 1024)
            logger.info("Success ftp get the file:%s.", FTP_FILE_NEW)
        except:
            logger.info("Failed ftp get the file: %s" , FTP_FILE_NEW)
        finally:
            handle.close()
            ftp.quit()

if __name__ == '__main__':
    main()