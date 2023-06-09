class ProjectConfig:
    # 配置执行项目，执行方式
    def projectConfig(self):
        """
        runType  为空时执行xlsx中所有用例  有文件名时执行当前文件名中的脚本多个用,号隔开
        testData  测试数据 csv文件 text文件 路径
        testCase  mqt文件路径
        :return:
        """
        config = {
            "driver_app": {"caseName": "driver_app_ui_testcase.xlsx", "runType": "driver_app_account_add.mqt",
                           "testData": "/data/test_case_file/driver_app/", "testCase": "/test/case/driver_app_case/",
                           "jobName": "Elife_UI_AutoTest", "title": "driver app UI自动化脚本执行完成:"},
            "flt_mgmt": {"caseName": "flt_mgmt_ui_testcase.xlsx", "runType": "flt_mgmt_employee_login.mqt",
                           "testData": "/data/test_case_file/flt_mgmt/", "testCase": "/test/case/flt_mgmt_case/",
                           "jobName": "Flt_mgmt_UI_AutoTest", "title": "flt_mgmt UI自动化脚本执行完成:"}
        }
        return config