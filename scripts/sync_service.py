#-*-coding:utf-8-*-

import sys,os
import time
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from common.sql_connect import Mysql


s = Mysql('172.18.3.51', 3601, 'crp_user', 'crpkingdee', 'newmc_rd_mcdb')


sql = "select fnumber,fzkurl,fzkrootpath from t_mc_environment"

for i in s.query(sql):
    if i['fzkrootpath']:
        print i['fnumber'], i['fzkurl'], i['fzkrootpath']
