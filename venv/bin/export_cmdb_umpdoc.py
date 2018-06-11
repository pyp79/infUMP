1  #!/usr/bin/python3
2  # -*- coding:utf-8 -*- 
3  #Author: Pang Yapeng

import datetime
import csv
from sub_common import *

# 特定参数
conf = get_conf()
EXPORT_FILE = conf.get("EXPORT_FILE", "UMP_DOC_FILE")
TABLE_NAME = "UMP_DOC"

# 设置log
logger = get_logger("export.log")

def main():
    logger.info("Begin to export from table:%s",TABLE_NAME)

    v_date_para = re.findall(r"\[(.*)\]", EXPORT_FILE)[0]
    new_date = datetime.datetime.now().strftime(v_date_para)
    EXPORT_FILE_NEW = re.sub("\[.*\]", new_date, EXPORT_FILE)

    # 查数据
    conn = get_conn()
    cursor = conn.cursor();
    sql = "SELECT APP_NAME,IP_ADDRESS,POLICY_NAME,POLICY_DESC,COMPONENT_TYPE,MONITOR," \
          "SEV1_CONDITION,SEV2_CONDITION,SEV3_CONDITION FROM {0}".format(TABLE_NAME)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    # 生成csv文件
    csv_file = open(EXPORT_FILE_NEW,'w',newline='',encoding='UTF-8')
    writer = csv.writer(csv_file)
    writer.writerow(['APP_NAME','IP_ADDRESS','POLICY_NAME','POLICY_DESC','COMPONENT_TYPE','MONITOR','SEV1_CONDITION','SEV2_CONDITION','SEV3_CONDITION'])
    writer.writerows(rows)
    csv_file.close()
    logger.info("Success write file:%s.",EXPORT_FILE_NEW)

    # ftp到服务器
    ftp = get_cmdb_ftp()
    filename = os.path.basename(EXPORT_FILE_NEW)
    handle = open(EXPORT_FILE_NEW, "rb")
    ftp.storbinary("STOR /attachment/" + filename, handle, 1024)
    handle.close()

    logger.info("Success ftp the file:%s.",EXPORT_FILE_NEW)

if __name__ == '__main__':
    main()