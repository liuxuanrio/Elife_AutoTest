import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

import pytest
import allure
from utils.config import FileDate, TimeMethod
from test.suite.ui_auto_test_suite import OpenFile, AutoFile


class Test_merchants_go:
    @pytest.mark.parametrize('casename', OpenFile().testFileCase())  # 获取test/case中的用例文件
    @allure.story("elife_ui_test")
    @allure.title("driver_app")
    @allure.testcase("")
    def test_merchant_action(self, casename):
        # 用例名称
        allure.dynamic.testcase(casename)

        # 获取当前时间搓
        caseutc = TimeMethod().intNewTimeUtc()

        # 执行用例
        msg = AutoFile().openFile(casename, caseutc)
        print(msg)

        # 保存执行日志
        with allure.step("执行日志"):
            allure.attach(msg[0])

        with allure.step("截图"):
            # 获取当前用例生成的截图
            attachList = FileDate().osFilePathList(casename + "_" + caseutc)
            for filename in attachList:
                print(filename)
                allure.attach.file(filename, attachment_type=allure.attachment_type.PNG)

        # 断言
        assert "FALSE" not in msg[1]


if __name__ == "__main__":
    # pytest.main(['test_merchants_all.py', '-s','-m=smoke'])#挑选带有smoke的进行运行
    pytest.main(['test_merchants_go.py', '-s', '--alluredir', './data/report/tmp'])
    os.system('allure generate  ./data/report/tmp -o ./data/report/report --clean')
