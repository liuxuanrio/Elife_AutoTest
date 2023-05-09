import imaplib
import email
import tempfile
import time

def openEmail(body, type):
    fp = tempfile.TemporaryFile()  # 创建临时文件
    fp.write(body.encode('utf-8'))
    fp.seek(0)
    data = str(fp.readline())[2: -5]
    if data.isdigit():  # 判断字符串中是否存在字母，长度大于15
        pass
    else:
        fp.readline()
        data = str(fp.readline())[2: -5]
    if data.isdigit():  # 判断字符串中是否存在字母，长度大于15
        pass
    else:
        data = "False"
    return data

def selectGmail(type):
    try:
        time.sleep(2)
        import socket
        import socks
        # 设置代理
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7890)
        socket.socket = socks.socksocket

        imap = imaplib.IMAP4_SSL("imap.gmail.com")  # establish connection

        imap.login("dev2elifetransfer@gmail.com", "auskojgqeppsmzqq")  # login

        status, messages = imap.select("INBOX")  # select inbox

        numOfMessages = int(messages[0])  # get number of messages

        data = "False"
        for i in range(numOfMessages, numOfMessages - 5, -1):
            res, msg = imap.fetch(str(i), "(RFC822)")  # fetches the email using it's ID

            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    # subject, From = obtain_header(msg)

                    # if msg.is_multipart():
                    # # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            data = openEmail(body, type)
                            if data == "False":
                                pass
                            else:
                                break
                if data not in "False":
                    break
            if data not in "False":
                break

        imap.close()
        print(data)
        return data

    except:
        return "False"

if __name__ == "__main__":
    # type： 1 gmailCode 2 userCode
    # 来源：1、gmailCode driver app根据手机号获取验证码，all ride获取验证码
    #      2、待扩展
    # type = sys.argv[1]
    print(selectGmail(type))
