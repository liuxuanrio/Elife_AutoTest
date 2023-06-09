import json
import traceback
from selenium.common import exceptions
from selenium import webdriver
import time
import csv
from selenium.webdriver.common.by import By

from test.common.gamilCode import selectGmail
from utils.config import TimeMethod, MYSQL_starter_test, DataType


class WebDriverRun:
    def __init__(self):
        # 打开的浏览器名称，多个浏览器保存为list
        self.chrstrlist = []

        # 保存打开的浏览器为int
        self.chrlist = []

        # 保存用例中的变量
        self.globalVariable = {}

        # 判断语句状态 0 通过  1 不通过
        self.ifstat = 0

        # 保存运行日志
        self.runlog = ""

        # 断言结果
        self.assertLog = ""

        # 获取当前运行的环境  0 本地环境  1 服务器
        self.system_test = 0

        # 保存utc
        self.caseutc = ""

        # 保存path
        self.path = ""

        # 获取项目运行的测试数据路径
        self.testData = ""

    def iselement(self, xpath):
        """
        判断元素是否存在
        """
        try:
            self.chrlist[self.chrindex].find_element(By.XPATH, xpath)
            return True
        except exceptions.NoSuchElementException:
            return False

    """
    seleium 点击，输入，获取文本操作
    """
    def webPageif(self, value, type):
        """
        type: 1 Click  2 Input  3 Value
        """
        # 获取当前运行的浏览器
        if type == 3:
            self.chrIndex(value[2][0])
        else:
            self.chrIndex(value[0])

        # 获取xpath路径
        xpath = value[2]

        # 重试次数
        for i in range(3):
            try:
                xpath = self.strValue(xpath)
                if self.iselement(xpath):
                    if type == 1:
                        self.webPageElementClick(xpath)
                    elif type == 2:
                        self.webPageElementInput(xpath, value)
                    elif type == 3:
                        self.webElementValue(value)
                    else:
                        print(f"类型不正确:{type}")
                    break
                else:
                    if i == 2:
                        self.logs(f"没有定位到元素位置：{xpath}  -----------------------------------------------")
                    time.sleep(1)
                    pass
            except:
                errorlog = traceback.print_exc()
                self.logs(f"执行报错：{xpath}{errorlog}  -----------------------------------------------")

    # 获取当前打开chrome
    def chrIndex(self, name):
        self.chrindex = self.chrstrlist.index(name)

    # 启动google浏览器
    def webBrowser(self, value):
        name = value[0]

        # 判断当前打开的浏览器是否保存在chrstrlist
        if name not in self.chrstrlist:
            self.chrstrlist.append(name)
            self.chrIndex(name)
            self.chrlist.append(self.chrindex)
        else:
            self.chrIndex(name)
        # 打开浏览器
        if self.system_test == 1:
            option = webdriver.ChromeOptions()
            # 无头模式
            option.add_argument('headless')
            # 沙盒模式运行
            option.add_argument('no-sandbox')
            # 大量渲染时候写入/tmp而非/dev/shm
            option.add_argument('disable-dev-shm-usage')
            option.add_argument('--disable-gpu')

            self.chrlist[self.chrindex] = webdriver.Chrome(options=option)
            self.chrlist[self.chrindex].execute_script("""navigator.geolocation.getCurrentPosition = function(success, failure) { 
                  success({ 
                    coords: {latitude: -43.5333, longitude: 172.633}, 
                    timestamp: Date.now(), 
                  }); 
                }""")
        else:
            self.chrlist[self.chrindex] = webdriver.Chrome()

        # 窗口最大化
        # self.chrlist[self.chrindex].minimize_window()
        # self.chrlist[self.chrindex].maximize_window()

    # 打开url
    def webBrowserPage(self, value):
        if value[1] == "str":
            url = self.strValue(value[2])
        else:
            url = self.strValue(value[1])
        # 打开链接
        self.chrlist[self.chrindex].get(url)
        time.sleep(5)

    # 点击元素
    def webPageElementClick(self, xpath):
        if "photo-upload-modal" in xpath and "select-from-album" in xpath:
            self.photoUpload(xpath)
        else:
            time.sleep(1)
            self.chrlist[self.chrindex].find_element(By.XPATH, xpath).click()

    # 上传图片
    def photoUpload(self, xpath):
        self.chrlist[self.chrindex].find_element(By.XPATH, xpath).send_keys(f"{self.testData}test.jpg")

    # 输入信息
    def webPageElementInput(self, xpath, value):
        if value[5] == "str":  # 判断参数中是否有拼接
            values = self.strValue(value[6])
        else:
            if len(value[5:]) > 1:
                values = ""
                for x in value[5:]:
                    values += x
                values = DataType().updateStrMake(values) + "\n"
            else:
                values = self.strValue(value[5])


        # 清除输入框内容
        try:
            self.chrlist[self.chrindex].find_element(By.XPATH, xpath).clear()
        except:
            pass
        if "ride-id-search-fld" in xpath:
            self.chrlist[self.chrindex].find_element(By.XPATH, xpath).send_keys(f"{values}\n")
        else:
            self.chrlist[self.chrindex].find_element(By.XPATH, xpath).send_keys(values)


    # 关闭浏览器
    def webquit(self, path, caseutc):
        # 结束运行时关闭所有开启的浏览器
        for i in range(len(self.chrstrlist)):
            time = TimeMethod().newTimeDates()
            pngName = path + "_" +caseutc + "_" + time + f"_{self.chrstrlist[i]}.png"
            self.chrlist[i].save_screenshot(pngName)
            self.chrlist[i].quit()
        # 重置全局变量
        self.chrstrlist = []
        self.chrlist = []
        self.globalVariable = {}
        self.ifstat = 0
        self.runlog = ""
        self.assertLog = ""
        self.system_test = 0
        self.caseutc = ""
        self.path = ""
        self.testData = ""

    # 截图
    def screenshot(self):
        for i in range(len(self.chrstrlist)):
            time = TimeMethod().newTimeDates()
            pngName = self.path + "_" + self.caseutc + "_" + time + f"_{self.chrstrlist[i]}.png"
            self.chrlist[i].save_screenshot(pngName)
            print("截图===========================================")

    # 获取元素值
    def webElementValue(self, value):
        # 把获取的值保存到全局参数self.globalVariable
        self.chrIndex(value[2][0])
        try:
            if value[2][-1] == "value":
                self.globalVariables(value[0], self.chrlist[self.chrindex].find_element(By.XPATH, value[2][2]).get_attribute('value'))
                self.logs(f"获取元素成功：{value[0]}={self.globalVariable[value[0]]}")
            else:
                self.globalVariables(value[0], self.chrlist[self.chrindex].find_element(By.XPATH, value[2][2]).\
                    get_attribute('innerText'))
                self.logs(f"获取元素成功：{value[0]}={self.globalVariable[value[0]]}")
        except:
            try:
                self.globalVariables(value[0], self.chrlist[self.chrindex].find_element(By.XPATH, value[2][2]).text)
            except:
                try:
                    self.globalVariables(value[0], self.chrlist[self.chrindex].find_element(By.XPATH, value[2][2]). \
                        get_attribute('innerText'))
                except:
                    self.logs(f"获取元素失败：{value}")
                    self.globalVariables(value[0], "")

    # 获取元素json
    def webElementInfo(self, value):
        self.chrIndex(value[2][0])
        try:
            displayed = self.chrlist[self.chrindex].find_element(By.XPATH, value[2][2]).is_displayed()
            self.globalVariables(value[0], {"displayed": displayed})
            self.logs(f"获取元素成功：{value[0]}={self.globalVariable[value[0]]}")
        except:
            self.logs(f"获取元素失败：{value}")
            self.globalVariables(value[0], "")
    def DBmysql(self, value):
        sqlvalue = value[2][1][1]
        if sqlvalue == "str":
            sqlvalue = self.strValue(value[2][1][2])
        else:
            sqlvalue = self.strValue(sqlvalue)
        if ("select" in sqlvalue or "SELECT" in sqlvalue) and ("update" not in sqlvalue or "delete" not in sqlvalue):
            valuelist = MYSQL_starter_test().ExecQuery(sqlvalue)
            retlist = []
            for i in valuelist:  # 循环读取list，替换日期格式为str
                retlist1 = []
                for x in i:
                    retlist1.append(TimeMethod().dayStrftime(x))
                retlist.append(retlist1)
            self.globalVariables(value[0], retlist)
        else:
            self.globalVariables(value[0], MYSQL_starter_test().ExecNonQuery(sqlvalue))

    # 执行sql
    def tableStream(self, value):
        if value[1][1] == "str":
            sqlvalue = self.strValue(value[1][2])
        else:
            sqlvalue = value[1][1]
        self.logs(sqlvalue)
        ret = MYSQL_starter_test().ExecNonQuery(sqlvalue.strip())
        self.logs(ret)

    # 分派指令
    def assign(self, value):
        if value[1] == "dateTimeFormat":  # 获取当前时间
            if "-" in value[2][1]:  # 有日期格式的
                if 'ss' in value[2][1]:
                    self.globalVariables(value[0], TimeMethod().newTimeDates())
                else:
                    self.globalVariables(value[0], TimeMethod().newTimeDate())
            else:  # 转数字的
                self.globalVariables(value[0], TimeMethod().intNowTimeDate())
        elif value[1] == "fileRun":  # 获取短信验证码
            if "gmailcode" in value[2][0]:
                self.globalVariable[value[0]] = selectGmail(1)
            else:
                self.logs("未找到当前打开文件的方法")
        elif value[1] == "fileReadOpen":
            self.globalVariables(value[0], f"{self.testData}{value[2][0].split('/')[-1]}")
        elif value[1] == "webElementValue":  # 获取元素值
            self.webElementValue(value)
        elif value[1] == "webElementInfo":  # 获取元素状态
            self.webElementInfo(value)
        elif value[1] == "webPageElements":
            self.webPageif(value, 3)
        elif value[1] == "webBrowser":  # 打开浏览器
            self.webBrowser(value)
        elif value[1] == "tableStream":  # 查询数据库
            self.DBmysql(value)
        elif value[1] == "selInPlace":  # 获取list中的值
            if value[2][0] in self.globalVariable.keys():
                self.globalVariables(value[0], self.globalVariable[value[2][0]][int(value[2][1])][int(value[2][2])])
            else:
                self.globalVariables(value[0], "")
        elif value[1] == "strSub":  # 截断字符串
            if value[2][0] == "str":
                self.globalVariables(value[0], self.strValue(value[2][1])[int(value[2][-2]):int(value[2][-1])])
            elif value[2][0] in self.globalVariable.keys():
                indexValue = int(value[2][1]) + int(value[2][2])
                lenValue = len(self.globalVariable[value[2][0]])
                if indexValue > lenValue:
                    indexValue = lenValue
                self.globalVariables(value[0], self.globalVariable[value[2][0]][int(value[2][1]):indexValue])
            else:
                self.globalVariables(value[0], "")

        elif value[1] == "sel":  # 获取list中对应的值
            if value[2][0] in self.globalVariable.keys():
                if value[2][1] in self.globalVariable.keys():
                    selindex = self.globalVariable[value[2][1]]
                else:
                    selindex = value[2][1]
                if str(selindex).isdigit():
                    self.globalVariables(value[0], self.globalVariable[value[2][0]][int(selindex)])
                else:
                    self.globalVariables(value[0], self.globalVariable[value[2][0]][selindex])
            else:
                self.globalVariables(value[0], "")

        elif value[1] == "valueOf":
            if len(value[2]) == 1:
                self.globalVariables(value[0], self.strValue(value[2][0]))
            elif len(value[2]) > 1:
                self.globalVariables(value[0], self.strValue(value[2][1]))
            else:
                self.logs(f"不执行:{value}")

        elif value[1] == "split":
            if value[2][0] in self.globalVariable.keys():
                self.globalVariables(value[0], self.globalVariable[value[2][0]].split(value[2][1]))
            else:
                self.logs(f"未找到参数:{value}")
        else:
            self.logs(f"未找到运行方法或者不执行:{value}")

    # 判断方法处理
    def ifelse(self, value):
        # 处理参数
        if value[0] == "equal" or value[0] == "greaterEqual":
            if value[1][0] == "str":
                ifvalue1 = self.strValue(value[1][1])
            else:
                ifvalue1 = self.strValue(value[1][0])
            if value[1][1] == "str":
                ifvalue2 = self.strValue(value[1][2])
            else:
                ifvalue2 = self.strValue(value[1][1])
            if value[0] == "equal":  # 相等
                if str(ifvalue1) == str(ifvalue2):  # 判断通过
                    self.ifstat = 0
                    self.ifForRun(value[2:])
                else:
                    self.ifstat = 1

            elif value[0] == "greaterEqual":  # 大于等于
                if int(ifvalue1) >= int(ifvalue2):  # 判断通过
                    self.ifstat = 0
                    self.ifForRun(value[2:])
                else:
                    self.ifstat = 1
        elif value[0] == "assign":
            if self.globalVariable[value[1][0]]:
                self.ifstat = 0
                self.ifForRun(value[2:])
            else:
                self.ifstat = 1
        else:
            self.logs(f"未找到判断方法：{value[0]}")

    # for循环
    def loopStream(self, value):
        if value[1] == "streamRange":  # 循环range
            for i in range(int(value[2][1])):
                self.globalVariables(value[0], i)
                self.ifForRun(value[3:])
        elif value[1] == "streamFileCsv":
            filename = self.globalVariable[value[2][0]]
            fileList = []
            with open(filename, "r") as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    fileList.append(row)
            csvfile.close()
            for i in fileList[1:]:
                self.globalVariables(value[0], i)
                self.ifForRun(value[3:])
        else:
            self.logs(f"循环方法：{value[1]}")

    # 嵌套中的方法处理
    def ifForRun(self, valueList):
        key = ""
        for value in valueList:
            if type(value) == list:
                self.main(key, value)
            else:
                key = value

    # 全局参数处理
    def args(self, kvlist):
        for kv in kvlist:
            if type(kv) == list:
                self.globalVariables(kv[0], kv[1])

    # str中参数处理
    def strValue(self, value):
        if type(value) == list:  # 判断参数中是否有拼接
            values = ""
            for s in value:
                if s[0: 1] == "@":
                    if s in self.globalVariable.keys():
                        info = str(self.globalVariable[s])
                        if info == "True" or info == "False":
                            values += info.lower()
                        else:
                            values += info
                    else:
                        # 获取参数不存在
                        self.logs(f"获取参数失败：{str(value)}---{s}")
                else:
                    values += str(s)
        elif value[0:1] == "@":  # 判断是否为变量
            if value in self.globalVariable.keys():  # 判断变量是否在全局变量中
                info = str(self.globalVariable[value])
                if info == "True" or info == "False":
                    values = info.lower()
                else:
                    values = info
            else:
                values = str(value)
        else:
            values = str(value)
        return values

    # 保存变量
    def globalVariables(self, key, value):
        self.logs(f"保存变量：{str(key)}:{str(value)}")
        self.globalVariable[key] = value

    def logs(self, logs):
        newTime = TimeMethod().newTimeDates()
        print(f"\n[{newTime}] {logs}")
        self.runlog += f"\n[{newTime}] {logs}"


    # 脚本中调用的方法处理
    def main(self, key, value):
        print(key, value)
        self.logs(f"{key}:{value}")
        if key == "webBrowserPage":  # 打开浏览器
            self.webBrowserPage(value)
        elif key == "webPageElementClick":  # 点击事件
            self.webPageif(value, 1,)
        elif key == "webPageElementInput":  # 输入事件
            self.webPageif(value, 2)
        elif key == "assign":  # 变量
            self.assign(value)
        elif key == "args":  # 全局变量
            self.args(value)
        elif key == "loopStream":  # for 循环
            self.loopStream(value)
        elif key == "tableStream":  # 执行sql
            self.tableStream(value)
        elif key == "if":
            self.ifelse(value)
        elif key == "elseIf":
            if self.ifstat == 1:
                self.ifelse(value)
        elif key == "else":
            if self.ifstat == 1:
                self.ifForRun(value)
                self.ifstat = 0
        elif key == "print":
            if value[0] == "str":
                value = self.strValue(value[1])
                self.logs(f"print:{value}")
                if "PASS" in value or "FALSE" in value:
                    self.assertLog += f"\n{value}"
            else:
                self.logs(f"print:{str(value[0])}")
        elif key == "sleep":
            if value[1][0] == "str":
                timeValue = self.strValue(value[1])
            else:
                timeValue = self.strValue(value[0])
            self.logs(f"强制等待:{str(timeValue)}")
            if timeValue != None:
                if int(timeValue) > 0:
                    if int(timeValue) > 60:
                        sumtime = int(timeValue)
                        for i in range(5):
                            if sumtime > 60:
                                time.sleep(60)
                                sumtime -= 60
                            else:
                                time.sleep(sumtime)
                                break
                    else:
                        time.sleep(int(timeValue))
                else:
                    self.logs(f"等待时间超时：{str(timeValue)}")
            else:
                self.logs(f"等待时间超时：{timeValue}")
        else:
            self.logs(f"未找到方法:{key} {value}")


if __name__ == "__main__":
    pass
    test = ["SELECT TIMESTAMPDIFF(Second,'", '@time', "', '", '@rideTime', ":00');"]
    data = WebDriverRun()
    data.globalVariable = {"@time": "2023-05-16 15:37:10", "@rideTime": "2023-05-16 15:37:50"}
    print(data.strValue(test))