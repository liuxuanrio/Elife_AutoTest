import os,sys
import time

from utils.config import FileDate, TimeMethod, DataType

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

import traceback
from test.common.web_Driver_run import WebDriverRun


class AutoFile(WebDriverRun):

    def openFile(self, filename, caseutc):
        # 获取工作目录
        script_path = FileDate().osFilePath()

        picturePath = f"{script_path}/data/test_picture/{filename}"
        if "jenkins_home" in picturePath:
            self.system_test = 1

        # 打开脚本文件
        file = open(f'{script_path}/test/case/{filename}', 'r', encoding='utf8')

        # 读取文件为list
        lists = file.readlines()[2:-1]
        print(lists)
        tuplesum = 0
        valuelist = []
        key = ""
        for i in range(len(lists)):
            data = lists[i].strip()
            if (tuplesum == 0 and data != "(" and "^" not in data) or i == len(lists) -1:
                if i == len(lists) - 1:
                    valuelist.append(data)
                if len(valuelist) > 0:  # 判断value是否不为空
                    # 调用执行方法
                    if valuelist[0] == "(":
                        pass
                        valuelist = self.for_list(valuelist[1:-1])
                    print(key, valuelist)
                    self.transfer(key, valuelist)
                    self.logs(f"{key}:{valuelist}")
                # 执行方法运行后，value设置为空
                valuelist = []
                # 保存符合条件的字符为key
                key = data
            else:
                if data == "(":
                    tuplesum += 1
                    valuelist.append(data)
                elif data == ")":
                    tuplesum -= 1
                    valuelist.append(data)
                else:
                    if "^" in data:
                        pass
                    else:
                        valuelist.append(DataType().updateStrMake(data))

        # 关闭文件
        file.close()

        # 全局变量保存到log
        self.runlog += f"\n 打开的浏览器：{str(self.chrstrlist)}" \
                       f"\n 打开的浏览器list：{str(self.chrlist)}" \
                       f"\n 保存的变量信息：{str(self.globalVariable)}" \
                       f"\n 保存的判断结果：{str(self.ifstat)}"
        self.logs(self.assertLog)

        assertint = self.assertLog

        # 关闭开启的浏览器
        self.webquit(picturePath, caseutc)

        return self.runlog, assertint

    # 处理list中嵌套方法
    def for_list(self, filelist):
        if "(" in filelist:
            tuplesum = 0
            valuelist = []
            key = ""
            return_list = []
            for i in range(len(filelist)):
                data = filelist[i].strip()
                if (tuplesum == 0 and data != "(" and "^" not in data) or i == len(filelist) - 1:
                    if i == len(filelist) - 1:
                        valuelist.append(data)
                    if len(key) > 0:  # 判断value是否不为空
                        return_list.append(key)
                    if len(valuelist) > 0:
                        if valuelist[0] == "(":
                            valuelist = self.for_list(valuelist[1:-1])
                        elif type(valuelist) == list:
                            valuelist = valuelist[0]
                        return_list.append(valuelist)
                    # 执行方法运行后，value设置为空
                    valuelist = []
                    # 保存符合条件的字符为key
                    key = DataType().updateStrMake(data)
                else:
                    if data == "(":
                        tuplesum += 1
                        valuelist.append(data)
                    elif data == ")":
                        tuplesum -= 1
                        valuelist.append(data)
                    else:
                        if "^" in data:
                            pass
                        else:
                            valuelist.append(DataType().updateStrMake(data))
            return return_list
        else:
            return filelist

    # 处理后的值调用对应的方法
    def transfer(self, key, value):
        try:
            self.main(key, value)
        except:
            errorlog = traceback.print_exc()
            self.logs(f"执行失败：{errorlog}-------------------------------------")


class OpenFile():
    def testFileCase(self):
        import os
        # path定义要获取的文件名称的目录
        script_path = FileDate().osFilePath()
        paths = f"{script_path}/test/case"

        # os.listdir()方法获取文件夹名字，返回数组
        file_name_list = os.listdir(paths)
        return file_name_list


if __name__ == "__main__":
    pass
    caseutc = TimeMethod().intNewTimeUtc()
    case = AutoFile().openFile("driver_app_employee_login1.mqt", caseutc)
    print(case)
    # case = AutoFile().filetest("test.mqt")
    # for i in case:
    #     print(AutoFile().openFile(i))