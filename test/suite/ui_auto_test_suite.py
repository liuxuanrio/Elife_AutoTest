from openpyxl.reader.excel import load_workbook

from config.projectConfig import ProjectConfig
from utils.config import FileDate, TimeMethod, DataType
import traceback
from test.common.web_Driver_run import WebDriverRun


class AutoFile(WebDriverRun):

    def openFile(self, filename, caseutc):
        # 获取工作目录
        script_path = FileDate().osFilePath()

        picturePath = f"{script_path}/data/test_picture/{filename}"
        self.caseutc = caseutc
        self.path = picturePath

        if "jenkins_home" in picturePath:
            self.system_test = 1
        else:
            self.project_name = "driver_app_ui_testcase.xlsx"

        # 打开脚本文件 判断文件属于哪个项目
        if "driver_app" in filename:
            file = open(f'{script_path}/test/case/driver_app_case/{filename}', 'r', encoding='utf8')
        else:
            file = open(f'{script_path}/test/case/driver_app_case/{filename}', 'r', encoding='utf8')

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
                    self.transfer(key, valuelist)
                    print(key, valuelist)
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
        runlogData = self.runlog

        # 关闭开启的浏览器
        self.webquit(picturePath, caseutc)

        return runlogData, assertint

    # 处理list中嵌套方法
    def for_list(self, filelist):
        if "(" in filelist:
            tuplesum = 0
            valuelist = []
            key = ""
            return_list = []
            for i in range(len(filelist)):
                data = filelist[i]
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
                            self.logs(data)
                        else:
                            if data == "', '":
                                pass
                                valuelist.append(data)
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
    # 读取用例表格并转化成list
    def openXlsx(self, path, fileName):
        excelDir = fr'{path}/test/case/{fileName}'  # 打开xlsx文件
        workBook = load_workbook(excelDir)  # 保存原样--样式
        # 2- 操作对应的用例表
        workSheet = workBook.worksheets[0]
        dataList = []
        cnt = 1
        for cnts in workSheet.rows:
            if cnt > 2:
                caseProject = workSheet.cell(cnt, 1).value  # 用例项目
                caseModule = workSheet.cell(cnt, 2).value  # 用例模块
                caseTitle = workSheet.cell(cnt, 3).value  # 用例标题
                caseDescription = workSheet.cell(cnt, 4).value   # 用例描述
                casePoint = workSheet.cell(cnt, 5).value   # 测试点
                dataList.append([caseProject, caseModule, caseTitle, caseDescription, casePoint])
            cnt += 1
        return dataList  # 列表

    # 处理单独运行的脚本数据
    def updateFileList(self, projectName, fileList):
        dataList = []
        for name in fileList:
            dataList.append([projectName, projectName, name, projectName, projectName])
        return dataList

    # 获取执行脚本list
    def testFileCase(self):
        path = FileDate().osFilePath()  # 获取文件路径
        fileConfig = ProjectConfig().projectConfig()
        # 判断当前项目运行环境
        if "jenkins_home" in path:
            if "Elife_UI_AutoTest" in path:
                fileName = fileConfig["driver_app"]["caseName"]
                runType = fileConfig["driver_app"]["runType"]
            else:
                fileName = fileConfig["driver_app"]["caseName"]
                runType = fileConfig["driver_app"]["runType"]
        else:  # 本地调试可手动修改需要执行的文件
            fileName = fileConfig["driver_app"]["caseName"]
            runType = fileConfig["driver_app"]["runType"]

        if runType:
            if "," in runType:
                file_name_list = runType.split(",")
            else:
                file_name_list = [runType]
            file_name_list = self.updateFileList("driver_app", file_name_list)
        else:
            file_name_list = self.openXlsx(path, fileName)
        return file_name_list


if __name__ == "__main__":
    pass
    # caseutc = TimeMethod().intNewTimeUtc()
    # case = AutoFile().openFile("driver_app_update_password.mqt", caseutc)
    # print(case)
    case = print(OpenFile().testFileCase())