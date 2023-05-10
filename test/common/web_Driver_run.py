import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

from selenium.common import exceptions
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

from test.common.gamilCode import selectGmail
from utils.config import TimeMethod


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

        # 保存判断语句的参数为list
        self.value = []

        # 保存运行日志
        self.runlog = ""

    def iselement(self, xpath):
        """
        基本实现判断元素是否存在
        :param browser: 浏览器对象
        :param xpaths: xpaths表达式
        :return: 是否存在
        """
        try:
            self.chrlist[self.chrindex].find_element(By.XPATH, xpath)
            return True
        except exceptions.NoSuchElementException:
            return False

    # seleium 点击，输入，获取文本操作方法需要运行的步骤(获取当前运行的浏览器，校验xpath是否存在)
    def webPageif(self, name, xpath, type, value, valuename):
        """
        :param name: 执行的web name
        :param xpath:
        :param type: 1 Click  2 Input  3 Value
        :return:
        """
        # 获取当前运行的流量
        self.chrIndex(name)

        # 处理xpath中\\符号
        xpath = xpath[1:-1].replace("\\", "")

        # 重试次数
        for i in range(3):
            if self.iselement(xpath):
                if type == 1:
                    self.webPageElementClick(xpath)
                elif type == 2:
                    self.webPageElementInput(xpath, value)
                elif type == 3:
                    self.webElementValue(xpath, valuename)
                else:
                    print(f"类型不正确:{type}")
                break
            else:
                if i == 2:
                    self.runlog += f"\n 没有定位到元素位置：{xpath}  -----------------------------------------------"
                time.sleep(3)
                pass

    # 获取当前打开chrome
    def chrIndex(self, name):
        self.chrindex = self.chrstrlist.index(name)

    # 打开浏览器
    def webBrowserPage(self, name, url):
        option = webdriver.ChromeOptions()
        # 无头模式
        option.add_argument('headless')
        # 沙盒模式运行
        option.add_argument('no-sandbox')
        # 大量渲染时候写入/tmp而非/dev/shm
        option.add_argument('disable-dev-shm-usage')

        # 判断当前打开的浏览器是否保存在chrstrlist
        if name not in self.chrstrlist:
            self.chrstrlist.append(name)
            self.chrIndex(name)
            self.chrlist.append(self.chrindex)
        else:
            self.chrIndex(name)
        self.chrlist[self.chrindex] = webdriver.Chrome(options=option)
        self.chrlist[self.chrindex].get(url[1:-1])

    # 点击元素
    def webPageElementClick(self, xpath):
        time.sleep(2)
        self.chrlist[self.chrindex].find_element(By.XPATH, xpath).click()

    # 输入信息
    def webPageElementInput(self, xpath, value):
        # 判断输入内容是否有拼接
        if value[5] == "str":
            value = value[6:]
            values = ""
            for i in range(len(value)):
                value1 = value[i].replace("(", "")
                value2 = value1.replace(")", "")
                if "@" in value2:
                    # 替换变量值
                    values += self.globalVariable[value2]
                else:
                    values += value2
        else:
            # 有变量符 且不是邮箱地址
            if "@" in value[5] and "com" not in value[5]:
                values = self.globalVariable[value[5]]
            else:
                values = value[5][1:-1]
        time.sleep(2)
        # 清除输入框内容
        self.chrlist[self.chrindex].find_element(By.XPATH, xpath).clear()
        self.chrlist[self.chrindex].find_element(By.XPATH, xpath).send_keys(values)

    # 关闭浏览器
    def webquit(self):
        # 结束运行时关闭所有开启的浏览器
        for i in range(len(self.chrstrlist)):
            self.chrlist[i].quit()
        # 重置全局变量
        self.chrstrlist = []
        self.chrlist = []
        self.globalVariable = {}
        self.ifstat = 0
        self.value = []


    # 获取元素值
    def webElementValue(self, xpath, globalkey):
        # 把获取的值保存到全局参数self.globalVariable
        self.globalVariable[globalkey] = self.chrlist[self.chrindex].find_element(By.XPATH, xpath).get_attribute('innerText')

    # 分派指令
    def assign(self, value):
        if value[1] == "dateTimeFormat":  # 获取当前时间
            if "-" in value[3]:  # 有日期格式的
                self.globalVariable[value[0]] = TimeMethod().newTimeDate()
            else:  # 转数字的
                self.globalVariable[value[0]] = TimeMethod().intNowTimeDate()
        elif value[1] == "fileRun":  # 获取短信验证码
            self.globalVariable[value[0]] = selectGmail(1)
        elif value[1] == "webElementValue":  # 获取元素值
            self.webPageif(value[2][1:], value[4], 3, "", value[0])
        else:
            print("未找到或者不执行", value)

    # 判断方法处理
    def ifelse(self, equal, values):
        # 保存判断参数
        valist = [values[1][1:], values[2][1:-7], values[5], values[6][3:-3]]

        # 去重
        self.value = list(set(valist))

        # 处理参数中变量
        for i in range(len(self.value)):
            if "@" in self.value[i]:
                self.value[i] = self.globalVariable[self.value[i]]

        if self.value[0] == self.value[1]:  # 执行判断
            # 保存结果
            self.runlog += f"\n{values[4][2:-1]} {self.value[0]} == {self.value[1]}-----------------------------------"
        else:
            # 修改判断状态为1 不通过
            self.ifstat = 1

    # 脚本中调用的方法处理
    def main(self, key, value):
        if key == "webBrowserPage":
            # 打开浏览器
            self.webBrowserPage(value[0], value[1])
        elif key == "webPageElementClick":
            # 点击事件
            self.webPageif(value[0], value[2], 1, "", "")
        elif key == "webPageElementInput":
            # 输入事件
            self.webPageif(value[0], value[2], 2, value, "")
        elif key == "assign":
            # 变量
            self.assign(value)
        elif key == "if":
            self.ifelse(value[0], value)
        elif key == "elif":
            pass
        elif key == "else":
            if self.ifstat == 1:
                self.runlog += f"\n{str(value[2][2:-1])} {str(self.value[0])} != {str(self.value[1])} -------------" \
                               f"--------------"
        elif key == "sleep":
            time.sleep(int(value[0]))
        elif key == "args":
            pass
        else:
            print("未找到方法:", key)


if __name__ == "__main__":
    pass