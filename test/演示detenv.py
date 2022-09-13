# -*- coding: utf-8 -*-
"""
Created on Thu May 26 09:23:30 2022

@author: Peikai_Li
"""


import os

def p():
    env_dist = os.environ
    for key in env_dist:
        print (key + ' : ' + env_dist[key])
    print("*"*10)
    print(os.getenv('test111'))
    print("MONGO_URI",type(os.getenv('MONGO_URI')))


 
p() # 第一次run 没有 TEST111 : just test111

print("*"*100)
from dotenv import load_dotenv
load_dotenv()
# Load environment parameters
# # 一、自动搜索 .env 文件
# load_dotenv(verbose=True)


# # 二、与上面方式等价
# load_dotenv(find_dotenv(), verbose=True)

# # 三、或者指定 .env 文件位置
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path, verbose=True)



p() # 运行load_dotenv()后就有了  TEST111 : just test111

# 不重启kernel 的话 导入的环境变量一直都在





