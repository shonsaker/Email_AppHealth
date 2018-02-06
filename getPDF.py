import img2pdf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import ocelliDB


class getPdf():

    def __init__(self):
        self.client_id = 24

    def get_client_list(self):
        try:
            # Add args depending on if the query is going to need any
            args = ""
            query = "select client_id from e1n_client where client_id = 24;"
            db = ocelliDB.ocelliDb()
            results = db.query(query, args)
            return results
        except Exception as e:
            print(e)

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
                height = browser.execute_script("return document.body.scrollHeight")
                height += 500

                # build the new options to get the correct page size
                chrome_options.add_argument("--window-size=1200x" + str(height))

                browser = webdriver.Chrome(r"C:\Users\shonsaker\Documents\shonsaker\chromedriver", options=chrome_options)
                browser.get(url)

                print("sleeping")
                sleep(45)
                print("awake")
                browser.save_screenshot(r"C:\Users\shonsaker\Documents\test.png")

        except Exception as e:
            print(e)

    def convertPdf(self):
        try:
            # convert the PNG to a PDF
            with open("C:\Users\shonsaker\Documents\out.pdf", "wb") as f:
                f.write(img2pdf.convert(r'C:\Users\shonsaker\Documents\test.png'))

        except Exception as e:
            print e

# if __name__ == '__main__':
#     get_apphealth()
#     convertPdf()
