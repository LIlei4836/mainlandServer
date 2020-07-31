import json
import pymysql


try:
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='BXrXpK7Z7dSEK9lK', database='sj')

    # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='huihuang', charset='utf8')
    cursor = conn.cursor()

    sql = "select * from qm_information ORDER BY id "
    cursor.execute(sql)
    a = cursor.fetchall()
    L = {}
    for i in range(0, len(a)):
        # dict = {'id':a[i][0],'addtime': a[i][1],'title': a[i][2], 'content': a[i][3]}
        dict = {}
        dict['id'] = str(a[i][0])
        dict['addtime'] = a[i][1]
        dict['title'] = str(a[i][2])
        dict['content'] = str(a[i][3])
        L[i] = dict
        print(dict['title'])
    # 关闭mysql链接
    cursor.close()
    conn.close()
except Exception as e:
    print(e)