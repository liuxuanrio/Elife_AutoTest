# 数据库
class MYSQL_starter_test:
    # 连接数据库地址，如需连接其他库时可参数化连接参数
    def __init__(self):
        import pymysql
        self.db = pymysql.connect(
        host="rideprod.c9y2b7qgnkr8.us-east-2.rds.amazonaws.com",
        user="dev_user",
        passwd="0TAnwLmMzDbCYMuf",
        db=f"ride",  # 库名
        charset="utf8"
    )
    # 传入sql语句查询所有值
    def ExecQuery(self, sql):
        cur=self.db.cursor()
        cur.execute(sql)
        resList = cur.fetchall()
        cur.close()
        return resList

    # 修改数据库信息
    def ExecNonQuery(self, sql):
        try:
            cur = self.db.cursor()
            cur.execute(sql)
            self.db.commit()
            cur.close()
        except:
            try:
                cur = self.db.cursor()
                cur.execute(sql)
                self.db.commit()
                cur.close()
            except:
                cur = self.db.cursor()
                cur.execute(sql)
                self.db.commit()
                cur.close()

    # 创建数据
    def ExecInstallQuery(self, sql, val):
        print(sql)
        print(val)
        try:
            cur = self.db.cursor()
            cur.executemany(sql, val)
            self.db.commit()
            cur.close()
        except:
            try:
                cur = self.db.cursor()
                cur.executemany(sql, val)
                self.db.commit()
                cur.close()
            except:
                cur = self.db.cursor()
                cur.executemany(sql, val)
                self.db.commit()
                cur.close()

# 日期方法
class TimeMethod:
    # 获取当前日期年月日时分
    def newTimeDate(self):
        import datetime
        strnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return strnow

    # 获取年月日时分秒，去除字符保留数字
    def intNowTimeDate(self):
        import datetime
        strnow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return strnow