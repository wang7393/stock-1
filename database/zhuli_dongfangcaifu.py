#-*- coding:utf8 -*-
import json
import pymysql
import csv
import requests
from xueqiu import headers
headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Cookie':'ct=h0v7J0zFBKLTFYu9cxyPvMnLtyA_kMCGu7yOxKzLvOD9wNbnXTbmj1moMkOlFj1lDBv-ErhnOpWL2iFqB6SCaNGxVGCicHe7XMCmGjc1kNHhaOY-i3LMByo1HNGHL-2oJfs4d9IVAeU-PktmpCgQVCnOp-cqdyzqF5TpRVYtnLM; ut=FobyicMgeV7bodPh3F8eYm7uuAYUIIiuDQ2yv0JtbXDQGAJjj4T9wMdK9wduzfHo-bvbQO05hHOPdxjKBYnBj4MfNa5chQhmzKRv2_VZ64ifE_VFK05Hkq6N9-t0o6XeeJ46Xu_wN63ZEVZgpp0jytKCE9zfpSQD6_DirESMTgxvz54rIT3L0T7WKrbw3Gfsi6jUQ_I9jxIbwQrszDRdNUnca1tezk8hSA1DmnZhqjE4f5YN3soLylwma-NIOT8_D0FJHJKbUUTVZB-IIklntWnF_jHN-gGT; sid=127228827; uidal=2171045336142634%e8%82%a1%e5%8f%8bmu7cr3; pi=2171045336142634%3bo2171045336142634%3b%e8%82%a1%e5%8f%8bmu7cr3%3bFnktn1nptEtOYWUx6eXx7H7%2bShZ1rBu%2bSaWgU5fXNcqO8h0WJvmTUVHoyaBhFyZlquCtcT5WkvPX3ZMFtbZ1YfM2lYUTe9%2bCvombfB9VF1qc2pRv%2bw9U5M8dHMWUvAkO5XKGp7oc8pJsUUG74Ephh6l7imMOuBNl69UzwaokxHfRM%2fyIB%2buArs8qnv4cZcjouFGBl50n%3bQUoGI%2bKQiCGU6zkG4VCaEXbdnA8aUKA0PIYYtQauR1yU31TJyzdbDuedKCDAhWvIWIheM8Ahwyrjplw%2bWNj%2fNoEoZFbXso2LpJiWzs9vBFt2FHHWrVLY9M0oOTr2YCWiG47C29SknLc1JnnzSj865obr0kCt9Q%3d%3d; vtpst=|; em_hq_fls=js; emshistory=%5B%22%E4%BA%BA%E6%B0%91%E7%BD%91%22%5D; st_si=32011905537124; st_asi=delete; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-000750-%u56FD%u6D77%u8BC1%u5238%2Ca-sz-000557-%u897F%u90E8%u521B%u4E1A%2Ca-sh-600722-%u91D1%u725B%u5316%u5DE5%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Ca-sh-603000-%u4EBA%u6C11%u7F51%2Ca-sz-000630-%u94DC%u9675%u6709%u8272%2Ca-sz-000713-%u4E30%u4E50%u79CD%u4E1A%2Ca-sh-603989-%u827E%u534E%u96C6%u56E2; qgqp_b_id=fa10817535d1bfdff03c00cab867b24a; st_pvi=35849832564120; st_sp=2019-02-21%2009%3A00%3A07; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2Flist%2C002181.html; st_sn=23; st_psi=20190321012805706-113200301201-0752711243'}
 
db = pymysql.connect("127.0.0.1","root","yungege_test","stock" )
cursor = db.cursor()

def get_info(id):
    zone="1"
    if id[:2]=="sz":
        zone="2"
#    url = "http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js=({data:[(x)]})&cb=var%20aff_data=&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id="+id[2:]+"&_=1553102917623"
    url = "http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js=({data:[(x)]})&cb=var%20aff_data=&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id="+id[2:]+zone+"&_=1553102917623"
    print(url)
    r = requests.get(url,headers=headers)
    s = r.text
    print(s)
    return
    fields = [
        "opendate",
        "trade",
        "changeratio",
        "turnover",
        "netamount",
        "ratioamount",
        "r0_net",
        "r0_ratio",
        "r0x_ratio",
        "cnt_r0x_ratio",
        "cate_ra",
        "cate_na"
    ]
    s = s.replace("cnt_r0x_ratio","aabbccdd")
    for f in fields:
        s = s.replace(f,"\""+f+"\"")
    s = s.replace("aabbccdd","\"cnt_r0x_ratio\"")
    l = json.loads(s)
    for v in l:
        values = []
        for field in fields:
            value = 0
            if field in v:
                value = v[field]
            if value is None:
                value = 0
            values.append(value)
        sql = "insert into zhuli(id,%s) values('%s',%s);" % (','.join(fields),id,','.join("'"+str(i)+"'" for i in values))
        try:
            cursor.execute(sql)
        except BaseException as e:
            print(sql,e)

with open('list.csv','r',encoding='utf-8') as csvfile:
    read = csv.reader(csvfile)
    title = True
    for v in read:
        if title:
            title = False
            continue
        id = v[0]
        get_info(id)
db.commit()
db.close()

