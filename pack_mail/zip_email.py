# -*- coding: utf-8 -*-
# @Author: DELL
# @Date:   2022-09-14 09:47:19
# @Last Modified by:   DELL
# @Last Modified time: 2022-09-14 09:47:19


import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import datetime
# import logging
import zipfile


def make_zip(source_dir, output_filename):
    f = zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED)
    for parents, _, file_list in os.walk(source_dir):
        print(parents, file_list)
        for file in file_list:
            file_path = os.path.join(parents, file)
            f.write(file_path)
    f.close()


def send_mail(dir_, recv):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    # 创建一个带附件的邮件实例
    message = MIMEMultipart()

    # 邮件的其他属性
    message['From'] = 'worklpk@163.com'
    message['Subject'] = Header(f'Covid from DXY__{today}', 'utf8').encode()
    message['To'] = ','.join(recv)
    # 邮件正文内容
    attr2 = MIMEText('file attachment test', 'plain', 'utf-8')
    message.attach(attr2)
    # 附件
    zipFile = dir_
    zipApart = MIMEApplication(open(zipFile, 'rb').read())
    zipApart.add_header('Content-Disposition', 'attachment', filename=zipFile)
    message.attach(zipApart)

    server = smtplib.SMTP('smtp.163.com', 25)
    server.login('worklpk@163.com', 'VYMNMGLQAJICGBOU')
    server.sendmail('worklpk@163.com', recv, message.as_string())


    # logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    #                 level=logging.DEBUG,
    #                 filename=f'log/log_{today}.log',
    #                 filemode='a')

    # logging.debug('邮件发送成功!')


if __name__ == '__main__':
    os.chdir('F:/CUHK/RA/covid_mjm/covid_19_email')
    # send_mail(['jaminmei.cn@gmail.com'])
    make_zip('attach_file', 'res.zip')
