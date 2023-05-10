import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

import traceback
from test.common.web_Driver_run import WebDriverRun


class AutoFile(WebDriverRun):
    def openFile(self, filename):
        # 定义脚本使用的方法
        self.operlist = ["args", "assign", "pause", "webBrowserPage", "webPageElementInput",
                         "webPageElementClick", "sleep", "if", "else"]

        # 打开脚本文件
        file = open(f'{filename}', 'r', encoding='utf8')

        # 读取文件为list
        lists = file.readlines()[2:-1]
        runlog = f"case title: {filename}"
        valuestr = ""
        key = ""
        for i in range(len(lists)):
            data = lists[i].strip()
            # 如果获取的字符在定义的方法内则执行保存为key，后面的字符保存为value
            if data in self.operlist or i == len(lists) -1:
                if valuestr:  # 判断value是否不为空
                    # 调用执行方法
                    self.transfer(key, valuestr)
                    self.runlog += f"\n {key}:{valuestr}"
                # 执行方法运行后，value设置为空
                valuestr = ""
                # 保存符合条件的字符为key
                key = data
            else:  # 处理字符串
                if data not in "(" and data not in ")":
                    valuestr += f"{data},"
                else:
                    if data in ")" and valuestr[-1] == ",":
                        valuestr = valuestr[:-1] + data
                    else:
                        valuestr += data
        # 关闭文件
        file.close()

        # 全局变量保存到log
        self.runlog += f"\n 打开的浏览器：{str(self.chrstrlist)}" \
                  f"\n 打开的浏览器list：{str(self.chrlist)}" \
                  f"\n 保存的变量信息：{str(self.globalVariable)}" \
                  f"\n 保存的判断结果：{str(self.ifstat)}" \
                  f"\n 保存的判断变量：{str(self.value)}"

        # 关闭开启的浏览器
        self.webquit()
        return self.runlog

    # 处理后的值调用对应的方法
    def transfer(self, key, value):
        if len(value) > 2:  # 值不为空
            value = value[1: -1]
            value = value.split(",")
            print(key, value)
            try:
                self.main(key, value)
            except:
                errorlog = traceback.print_exc()
                self.runlog += f"\n 执行失败：{errorlog}-------------------------------------"
        else:
            print("参数为空:", key, value)

class OpenFile():
    def testFileCase(self, path):
        import os

        # path定义要获取的文件名称的目录
        paths = f"{path}/data"

        # os.listdir()方法获取文件夹名字，返回数组
        file_name_list = os.listdir(paths)
        return file_name_list


if __name__ == "__main__":
    pass
    # case = OpenFile().testFileCase()
    # for i in case:
    #     print(AutoFile().openFile(i))