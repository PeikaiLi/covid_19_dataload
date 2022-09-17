"""
@ProjectName: DXY-2019-nCoV-Crawler
@FileName: script.py
@Author: Jiabao Lin
@Date: 2020/1/31

@modify by peikai on Wed May 25 22:11:28 2022
"""


from github3 import login
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import json
import time
import logging
import datetime
from pack_mail.zip_email import make_zip, send_mail


# Load environment parameters
load_dotenv()  # 补充一些环境变量 从 .env 文件里面


# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


# Database connection
# uri = 'localhost:27017'
# client = MongoClient(uri)
# MongoClient(None) == MongoClient() == MongoClient('localhost:27017')
# if os.getenv('MONGO_URI') == None：
#  --> MongoClient(os.getenv('MONGO_URI')) == MongoClient(None)
# else:
    # type(os.getenv('MONGO_URI')) == <class 'str'>
    

client = MongoClient(os.getenv('MONGO_URI'))
db = client['2019-nCoV']


collections = {
    'DXYOverall': 'overall',
    'DXYArea': 'area',
    'DXYNews': 'news',
    'DXYRumors': 'rumors',
    'DXYArea_f': 'area_with_Asymptomatic'
}


files = (
    'json/DXYOverall.json', 'json/DXYArea.json', 'json/DXYNews.json', 'json/DXYRumors.json',
    'json/DXYArea_f.json'
)


time_types = ('pubDate', 'createTime', 'modifyTime', 'dataInfoTime', 'crawlTime', 'updateTime')


class DB:
    def __init__(self):
        self.db = db

    def count(self, collection: str):
        """
        未使用的方法
        """
        return self.db[collection].count_documents(filter={})

    def dump(self, collection: str):
        """
        """
        return self.db[collection].aggregate(
            pipeline=[
                {
                    '$sort': {
                        'updateTime': -1,
                        'crawlTime': -1
                    }
                }
            ],
            allowDiskUse=True
        )


class Listener:
    def __init__(self, just_run_once = True):
        self.db = DB()
        self.just_run_once = just_run_once

    def run(self):
        while True:
            self.updater()
            if self.just_run_once:
                break
            time.sleep(
                (
                    # Update every data 00点00分00秒
                    datetime.timedelta(hours=24) - (datetime.datetime.now() - datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
                ).total_seconds()
            )


    # @staticmethod
    # def github_manager():
    #     """
    #     一个把从mongo导出的数据发布到github的函数，我们不需要
    #     """
    #     # GitHub connection
    #     github = login(token=os.getenv('GITHUB_TOKEN'))
    #     github.session.default_read_timeout = 20
    #     github.session.default_connect_timeout = 20

    #     repository = github.repository(owner='BlankerL', repository='DXY-COVID-19-Data')
    #     release = repository.create_release(
    #         tag_name='{tag_name}'.format(
    #             tag_name=datetime.datetime.today().strftime('%Y.%m.%d')
    #         )
    #     )
    #     for file in files:
    #         logger.info('Uploading: ' + file.split('/')[-1])
    #         release.upload_asset(
    #             content_type='application/text',
    #             name=file.split('/')[-1],
    #             asset=open(
    #                 file=os.path.join(
    #                     os.path.split(os.path.realpath(__file__))[0], file
    #                 ),
    #                 mode='rb'
    #             )
    #         )


    def updater(self):
        for collection in collections:
            cursor = self.db.dump(collection=collection)
            self.db_dumper(collection=collection, cursor=cursor)
            logger.info(collection + '.json dumped!')


        # self.github_manager()
        logger.info(f'Upload session complete for {datetime.datetime.today().date()}.')


    @staticmethod
    def db_dumper(collection: str, cursor):
        data = list()
        if collection != 'DXYArea':
            for document in cursor:
                document.pop('_id')
                # if document.get('comment'):
                #     document.pop('comment')
                data.append(document)
        else:
            for document in cursor:
                document.pop('_id')
                # 下面 key 不存在时，pop 返回 None
                document.pop('statisticsData', None) 
                # statisticsData 是省level的历史记录
                document.pop('showRank', None) 
                document.pop('operator', None)
                data.append(document)

        # print(os.path.realpath(__file__)) # 打印文件根目录
        dirs =  os.path.join(os.path.split(os.path.realpath(__file__))[0], 'json')
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        with open(os.path.join(dirs, collection + '.json'),'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    listener = Listener()
    listener.run()
    dirs =  os.path.join(os.path.split(os.path.realpath(__file__))[0], 'json')
    make_zip(dirs, dirs+'.zip')
    send_mail(dirs+'.zip', ['jaminmei.cn@gmail.com', 'peikai_li@163.com'])

