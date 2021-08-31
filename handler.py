try:
    import unzip_requirements
except ImportError:
    pass

import json, sys
sys.path.append('./requirements')
import json
import pymongo
import os
import datetime

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ["DB_PASSWARD"]
DB_NAME = os.environ["DB_NAME"]
COLLECTION_NAME = os.environ["COLLECTION_NAME"]

client = pymongo.MongoClient("mongodb+srv://{user}:{pw}@{host}".format(user=DB_USER, pw=DB_PASSWORD, host=DB_HOST))
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_daily_movies(event, context): # 일별 랭킹 box office 가져오기
    params = event['queryStringParameters']
    if params == None:
        base_datetime = datetime.datetime.now()
        dt = datetime.datetime(base_datetime.year, base_datetime.month, base_datetime.day,0,0,0)
    else:
        dt = datetime.datetime.strptime(params['dt'], "%Y%m%d")
    res = collection.find_one({'datetime': dt},{"_id":0, "datetime":0})
    response = {
        "statusCode": 200,
        "body": json.dumps(res)
    }
    return response

# 지정날짜 기준 1주일 랭킹 box office 가져오기
def get_weekly_movies(event, context):
    params = event['queryStringParameters']
    if params == None:
        base_datetime = datetime.datetime.now()
        dt = datetime.datetime(base_datetime.year, base_datetime.month, base_datetime.day)
    else:
        dt = datetime.datetime.strptime(params['dt'], "%Y%m%d")
    res = list(collection.find({'datetime': {"$lte":dt}},{"_id":0, "datetime":0}).sort("datetime", -1).limit(7))


    response = {
        "statusCode": 200,
        "body": json.dumps(res)
    }

    return response

