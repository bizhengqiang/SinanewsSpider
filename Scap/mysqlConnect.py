import pymysql
mysqlconfig = {
    "host": "localhost",
    "port": "3306",
    "user": "bzq",
    "password": "123456",
    "database": "sina",
    "charset": "utf8"
    }
sinaDB = pymysql.Connect("localhost", "bzq", "123456", "sina")
sinacur = sinaDB.cursor()
sql = "INSERT INTO sinanewsinfo(newsTitle,newsSource,newsAuthor,newsPaperfrom,newsTime) VALUES('这个世界会好吗','www.baidu.com','ak1999','青年网','2019-1-23')"
# data = ('这个世界会好吗', 'www.baidu.com', 'ak1999', '青年网', '2019-1-23')
sinacur.execute(sql)
print("数据库连接成功")
sinaDB.commit()
sinaDB.close()
print("数据库关闭连接")
