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

    # 获取当前年月日
    def newTimeDay(self):
        import datetime
        strnow = datetime.datetime.now().strftime("%Y-%m-%d")
        return strnow

    # 获取当前日期年月日时分秒
    def newTimeDates(self):
        import datetime
        strnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return strnow

    # 获取年月日时分秒，去除字符保留数字
    def intNowTimeDate(self):
        import datetime
        strnow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return strnow

    # 获取当前时间搓
    def intNewTimeUtc(self):
        import datetime
        strnow = str(int(datetime.datetime.now().timestamp()))
        return strnow

    # 数据库日期转字符串
    def dayStrftime(self, time):
        import datetime
        if isinstance(time, datetime.datetime):
            time = time.strftime('%Y-%m-%d %H:%M:%S')
        return time


# 数据处理
class DataType:

    # 去除字符串中的引号
    def updateStrMake(self, data):
        if data[0: 1] == "'" or data[0: 1] == '"':
            data = eval(data)
        return data




# 获取文件信息
class FileDate:

    # 获取文件路径
    def osFilePath(self):
        # 获取工作目录
        import os
        script_path = os.path.abspath(__file__)[:-16]
        return script_path

    # 获取目录中符合条件的文件返回路径加文件名
    def osFilePathList(self, fileName):
        import os
        script_path = self.osFilePath()
        paths = f"{script_path}/data/test_picture"

        # os.listdir()方法获取文件夹名字，返回数组
        file_name_list = os.listdir(paths)
        pathlist = []
        for name in file_name_list:
            if fileName in name:
                pathlist.append(f"{paths}/{name}")
        return pathlist



if __name__ == "__main__":
    pass
    print(DataType().updateStrMake('"//*[@id=\\"index_rides_mgmt\\"]//*[@id=\\"finished-top-title\\"]"'))
    # FileDate().osFilePathList("test.mqt_1683712400")

    # data = TimeMethod().intNewTimeUtc()