import redis
import pymysql
import json
import time


def get_data():
    while 1:
        try:
            # print('111')
            time.sleep(5)

            r = redis.Redis(host='127.0.0.1', port=6379,decode_responses=True)
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK',database='sj', connect_timeout=36000)
            cursor = conn.cursor()
            while 1:
                try:
                    sql = 'select * from hz_ada'
                    cursor.execute(sql)
                    a = cursor.fetchall()
                    a = a[-3:]
                    #print(a)
                    a =json.dumps(a,ensure_ascii = False, indent = 4)
                    r.set('data',a)
                    conn.close()
                    time.sleep(30)

                except:
                    time.sleep(10)
                    break
        except:
            time.sleep(10)


if __name__ == '__main__':
    get_data()