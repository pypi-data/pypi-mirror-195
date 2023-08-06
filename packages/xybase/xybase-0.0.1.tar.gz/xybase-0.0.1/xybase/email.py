from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from typing import Union


class EmailServer:
    smtp: SMTP_SSL

    def __init__(self, host: str, port: int, user: str, password: str):
        self.smtp = SMTP_SSL(host, port)
        self.smtp.login(user, password)

    def quit(self):
        self.smtp.quit()


class Email:
    msg: MIMEMultipart
    smtp: SMTP_SSL

    def __init__(self, server: Union[EmailServer, SMTP_SSL]):
        self.msg = MIMEMultipart()
        self.smtp = server if isinstance(server, SMTP_SSL) else server.smtp

    def from_(self, from_: str):
        """ 标题 """
        self.msg['from'] = from_
        return self

    def subject(self, subject: str):
        """ 副标题 """
        self.msg['subject'] = subject
        return self

    def to(self, to: Union[str, list[str]]):
        """ 收件人列表 """
        self.msg['to'] = to if isinstance(to, str) else ','.join(to)
        return self

    def text(self, text: str, charset='utf-8'):
        """ 文本 """
        self.msg.attach(MIMEText(text, _charset=charset))
        return self

    def html(self, html: str, charset='utf-8'):
        """ HTML """
        self.msg.attach(MIMEText(html, 'html', charset))
        return self

    def attach(self, source: Union[str, bytes], filename: str = None):
        """ 附件 """
        att = MIMEApplication(open(source, 'rb').read() if isinstance(source, str) else source)
        if not filename and isinstance(source, str):
            paths = source.split('/')
            filename = paths[len(paths) - 1]
        att.add_header('Content-Disposition', 'attachment', filename=filename)
        self.msg.attach(att)
        return self

    def send(self, to_addrs: Union[str, list[str]]):
        """ 发送邮件，to_addrs:收件人地址列表, from_addr:与服务器登录用户邮箱地址一致 """
        self.smtp.sendmail(from_addr=self.smtp.user, to_addrs=to_addrs, msg=self.msg.as_string())
