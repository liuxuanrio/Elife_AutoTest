class ProjectConfig:
    # 配置执行项目，执行方式
    def projectConfig(self):
        """
        runType  为空时执行xlsx中所有用例  有文件名时执行当前文件名中的脚本多个用,号隔开
        :return:
        """
        config = {
            "driver_app": {"caseName": "driver_app_ui_testcase.xlsx", "runType": "chrom_config.mqt",
                           "testData": "/data/test_case_file/driver_app/", "testCase": "/test/case/driver_app_case/"}
        }
        return config