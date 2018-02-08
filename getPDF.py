import img2pdf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import traceback
import os
import log_errors
import ocelliDB
import sendMail


class getPdf():

    def __init__(self):
        self.send_mail = sendMail.SendMail()
        self.log = log_errors.error_handling()
        self.client_id = 24
        self.module = "SendPDF"

    def get_client_list(self):
        try:
            # Get a list of customers who have a user that has enabled the alert
            args = ""
            query = "select DISTINCT client_id from e1n_client_users where client_user_summary_email='Y' and client_id = 24 order by client_id;"
            db = ocelliDB.ocelliDb()
            results = db.query(query, args)
            return results
        except Exception:
            traceback_message = traceback.format_exc()
            self.log.log_error(self.module, self.client_id, traceback_message)

    def get_user_list(self):
        try:
            # Get the list of users to send mail to
            query = """select t1.user_key, t2.user_email_address
                        from
                          (select *
                          from e1n_client_users
                          where
                          client_id = %s and client_user_summary_email = 'Y') as t1
                        join
                          (select user_email_address, user_key
                            from e1n_users) as t2
                          on t1.user_key = t2.user_key;"""

            db = ocelliDB.ocelliDb()
            results = db.query(query, self.client_id)
            return results

        except Exception:
            traceback_message = traceback.format_exc()
            self.log.log_error(self.module, self.client_id, traceback_message)

    def get_apphealth(self):
        try:
            # Reach out to the Db and get all the registered clients
            client_list = self.get_client_list()
            for client in client_list:
                self.client_id = client["client_id"]

                # Add a client_id to the Url to specify the client we wish to run for
                url = "https://clarity.erpsuites.com/stage/apphealth_sh_test.php?client_id=" + str(self.client_id)

                chrome_options = Options()
                chrome_options.add_argument("--headless")

                # Hit the page once to get the total length of the page
                browser = webdriver.Chrome(r"C:\Users\shonsaker\Documents\shonsaker\chromedriver", options=chrome_options)
                browser.get(url)
                # Expand the Arch table
                class_name = "details-control"
                self.click_item(browser, class_name)

                height = browser.execute_script("return document.body.scrollHeight")

                # build the new options to get the correct page size
                chrome_options.add_argument("--window-size=1200x" + str(height))
                chrome_options.add_argument("--hide-scrollbars")

                browser = webdriver.Chrome(r"C:\Users\shonsaker\Documents\shonsaker\chromedriver", options=chrome_options)
                browser.get(url)

                print("sleeping")
                sleep(45)
                print("awake")

                # Expand the Arch table
                class_name = "details-control"
                self.click_item(browser, class_name)

                self.png_path = r"C:\Users\shonsaker\Documents\test.png"
                browser.save_screenshot(self.png_path)
                browser.quit()
                self.convert_pdf()
                self.send_mail.client_id = self.client_id
                self.send_mail.run()

                # Send emails to every user who has requested it in this customer
                # users = self.get_user_list()
                # for user in users:
                #     print user["user_email_address"]
                #     self.send_mail.client_id = self.client_id
                #     self.send_mail.to_address = user["user_email_address"]
                #     self.send_mail.create_email()

                # Remove png and pdf files after the client is finished
                os.remove(self.png_path)
                os.remove(self.pdf_path)


        except Exception as e:
            traceback_message = traceback.format_exc()
            self.log.log_error(self.module, self.client_id, traceback_message)

    def convert_pdf(self):
        try:
            # convert the PNG to a PDF
            self.pdf_path = "C:\Users\shonsaker\Documents\out.pdf"
            with open(self.pdf_path, "wb") as f:
                f.write(img2pdf.convert(self.png_path))

        except Exception as e:
            traceback_message = traceback.format_exc()
            self.log.log_error(self.module, self.client_id, traceback_message)

    def click_item(self, browser, class_name):
        try:
            expand_tabs = browser.find_elements_by_class_name(class_name)
            for item in expand_tabs:
                item.click()
            sleep(5)
        except Exception:
            traceback_message = traceback.format_exc()
            self.log.log_error(self.module, self.client_id, traceback_message)
