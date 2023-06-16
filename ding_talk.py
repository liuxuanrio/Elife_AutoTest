import os
import jenkins #安装pip install python-jenkins
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests


# jenkins登录地址
jenkins_url = "http://18.222.127.214:8989/job/"
# 获取jenkins对象
server = jenkins.Jenkins(jenkins_url) #Jenkins登录名 ，密码
# job名称
job_name = "Elife_UI_AutoTest" #Jenkins运行任务名称
# job的url地址
job_url = jenkins_url + job_name
# 获取最后一次构建
job_last_build_url = server.get_info(job_name)['lastBuild']['url']
# 报告地址
report_url = job_last_build_url + 'allure' #'allure'为我的Jenkins全局工具配置中allure别名

'''
钉钉推送方法：
读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
使用钉钉机器人的接口，拼接后推送text
'''

def DingTalkSend():
    d = {}
    # 获取项目绝对路径
    path = os.path.abspath(os.path.dirname((__file__)))
    # 打开prometheusData 获取需要发送的信息
    f = open(path + r'/allure-report/export/prometheusData.txt', 'r')
    for lines in f:
        for c in lines:
            launch_name = lines.strip('\n').split(' ')[0]
            num = lines.strip('\n').split(' ')[1]
            d.update({launch_name: num})
    f.close()
    retries_run = d.get('launch_retries_run')  # 运行总数
    print('运行总数:{}'.format(retries_run))
    status_passed = d.get('launch_status_passed')  # 通过数量
    print('通过数量：{}'.format(status_passed))
    status_failed = d.get('launch_status_failed')  # 不通过数量
    print('通过数量：{}'.format(status_failed))

    # 钉钉推送
    headers = {'Content-Type': 'application/json', "Charset": "UTF-8"}
    # 这里替换为复制的完整 webhook 地址
    prefix = 'https://oapi.dingtalk.com/robot/send?access_token=4cac6867a85bfe684ac3c1d361dafad1e2d723095fe267eac84c532575206009'
    # 时间戳
    timestamp = str(round(time.time() * 1000))
    # 这里替换为自己复制过来的加签秘钥
    secret = 'SEC1f4db9bb49584c977e4ec4dfe3c6ba100c5c79200ee49dddcc658d782eca3e6a'
    # 编码转换
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    # 使用HmacSHA256算法计算签名，然后进行Base64 encode
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    #把签名参数再进行urlEncode，得到最终的签名
    # 将一些特殊的字符串转换为固定的一些符号字母数字组合，比如/转为%2（随便编的，大概这个意思）
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    #拼接url
    url = f'{prefix}&timestamp={timestamp}&sign={sign}'
    #钉钉消息格式，其中 content 就是我们要发送的具体内容
    con = {"msgtype": "text",
           "text": {
               "content": "driver app UI自动化脚本执行完成。"
                          "\n测试概述:"
                          "\n运行总数:" + retries_run +
                          "\n通过数量:" + status_passed +
                          "\n失败数量:" + status_failed +
                          "\n构建地址：\n" + job_url +
                          "\n报告地址：\n" + report_url
           }
           }


    jd = json.dumps(con)
    requests.request('POST', url, data=jd, headers=headers)


if __name__ == '__main__':
    DingTalkSend()