# Creates an email with the apphealth pdf
# and sends it to the approiate people
# by Harry Wells, modified by Steven Honsaker

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import traceback
import datetime
import os
import sys


class SendMail:

    def __init__(self):

        self.script_name = __file__.split('/')[-1].split('.')[0]
        self.now = datetime.datetime.now()
        self.subject = "Daily AppHealth Report By ErpSuites"
        self.from_address = 'shonsaker@erpsuites.com'
        self.to_address = 'shonsaker@erpsuites.com'
        self.pdf_path = "C:\Users\shonsaker\Documents\out.pdf"
        self.module = 'send_apphealth_mail.py'

    def create_email(self):

        try:
            email_structure = MIMEMultipart()
            email_structure['Subject'] = self.subject
            email_structure['From'] = self.from_address
            email_structure['To'] = self.to_address

            filename = self.pdf_path
            fp = open(filename, 'rb')
            att = MIMEApplication(fp.read(), _subtype="pdf")
            fp.close()
            att.add_header('Content-Disposition', 'attachment', filename=filename)
            email_structure.attach(att)

            return email_structure

        except Exception as e:
            print(e)
            self.log_error.log_error(self.module, sys._getframe().f_code.co_name, traceback.format_exc())

    def run(self):

        server_connect = None
        try:
            server_connect = SMTP()
            server_connect.connect('smtp.serversuites.com')

            email = self.create_email()

            server_connect.sendmail(self.from_address, self.to_address, email.as_string())

        except Exception:
            self.log_error.log_error(self.module, sys._getframe().f_code.co_name, traceback.format_exc())
        finally:
            if server_connect is not None:
                server_connect.quit()
            if os.path.isfile(self.pdf_path):
                # os.remove(self.pdf_path)
                t = 0

# if __name__ == "__main__":
#     send_mail = SendMail()
#     send_mail.run()