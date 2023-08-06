import smtplib
from email.message import EmailMessage


class Mailer:
    def __init__(self, *, host, port, user, password) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def send_msg(self, msg):
        s = smtplib.SMTP_SSL(self.host, self.port)
        s.login(self.user, self.password)
        s.send_message(msg)
        s.quit()

    def send(self, *, subject, from_, to, content):
        msg = EmailMessage()
        msg.set_content(content)

        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to

        # h/t: https://stackoverflow.com/a/54549934
        msg.add_header('List-Unsubscribe', '<http://somelink.com>')

        self.send_msg(msg)
