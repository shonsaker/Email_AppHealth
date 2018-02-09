# Creates an email with the apphealth pdf
# and sends it to the users signed up for alerts
# by Harry Wells, modified by Steven Honsaker

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import traceback
import datetime
import ocelliDB


class SendMail:

    def __init__(self):
        self.db = ocelliDB.ocelliDb()
        self.script_name = __file__.split('/')[-1].split('.')[0]
        self.now = datetime.datetime.now()
        self.subject = "Daily AppHealth Report By ErpSuites"
        self.from_address = 'shonsaker@erpsuites.com'
        self.to_address = 'shonsaker@erpsuites.com'
        self.pdf_path = r"C:\Users\shonsaker\Documents\out.pdf"
        self.module = 'send_apphealth_mail.py'
        self.client_id = 0

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

        except Exception:
            traceback_message = traceback.format_exc()
            self.db.log_error(self.module, self.client_id, traceback_message)

    def run(self):

        server_connect = None
        try:
            server_connect = SMTP()
            server_connect.connect('smtp.serversuites.com')

            email = self.create_email()

            server_connect.sendmail(self.from_address, self.to_address, email.as_string())

        except Exception:
            traceback_message = traceback.format_exc()
            self.db.log_error(self.module, self.client_id, traceback_message)
        finally:
            if server_connect is not None:
                server_connect.quit()
