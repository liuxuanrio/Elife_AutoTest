import os
import pytest
import allure
from utils.config import FileDate, TimeMethod
from test.suite.ui_auto_test_suite import OpenFile, AutoFile

@allure.feature("sign_in")
class Test_sign_in:
    @pytest.mark.parametrize('caseProject,caseModule,caseTitle,caseDescription,casePoint', OpenFile().testCaseAll("sign_in"))
    def test_sign_in_action(self, caseProject, caseModule, caseTitle, caseDescription, casePoint):
        # 用例名称
        allure.dynamic.title(caseTitle)

        # 用例描述
        description = f"{caseDescription}\n测试点:\n{casePoint}"
        allure.dynamic.description(description)

        # 获取当前时间搓
        caseutc = TimeMethod().intNewTimeUtc()

        # 执行用例
        msg = AutoFile().openFile(caseTitle, caseutc)
        print(msg)

        # 保存执行日志
        with allure.step("执行日志"):
            allure.attach(msg[0])

        # 保存用例中的变量信息
        with allure.step("variable"):
            allure.attach(msg[2], 'Json数据', allure.attachment_type.JSON)

        with allure.step("截图"):
            # 获取当前用例生成的截图
            attachList = FileDate().osFilePathList(caseTitle + "_" + caseutc)
            for filename in attachList:
                print(filename)
                allure.attach.file(filename, attachment_type=allure.attachment_type.PNG)

        # 断言
        assert "FALSE" not in msg[1]



if __name__ == "__main__":
    # pytest.main(['test_merchants_all.py', '-s','-m=smoke'])#挑选带有smoke的进行运行
    pytest.main(['main.py', '-s', '--alluredir', './data/report/tmp'])
    os.system('allure generate  ./data/report/tmp -o ./data/report/report --clean')