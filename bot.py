from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from time import sleep
from table_frame import TableFrame
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.common.keys import Keys


class MyBot:
    def __init__(self, login_id, password) -> None:
        self.login_id = login_id
        self.password = password
        self.mail_address = ""
        self.sender_pass = ""
        self.session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
        self.session.starttls()  # enable security
        self.session.login(
            self.mail_address, self.sender_pass
        )  # login with mail_id and password

    def open_site(self):
        self.driver = webdriver.Chrome()

        # Login
        self.driver.get(
            "https://www.intervalworld.com/web/my/auth/loginPage?OWASP_CSRFTOKEN=8QNG-1UWR-RC4M-UUWB-U9GG-Z8DO-KRK4-0J4Z&OWASP_CSRFTOKEN=8QNG-1UWR-RC4M-UUWB-U9GG-Z8DO-KRK4-0J4Z&OWASP_CSRFTOKEN=8QNG-1UWR-RC4M-UUWB-U9GG-Z8DO-KRK4-0J4Z"
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="textfield"]"""))
        )
        self.driver.find_element_by_xpath(
            "/html/body/div[10]/div/form/table/tbody/tr[1]/td[2]/input"
        ).send_keys(self.login_id)
        self.driver.find_element_by_xpath(
            "/html/body/div[10]/div/form/table/tbody/tr[2]/td[2]/input"
        ).send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="buttonlogin"]').click()

    def search(self):
        self.driver.get("https://www.intervalworld.com/web/cs?a=0")

        city = "Maui"
        today = datetime.today()
        after_14 = (today + timedelta(days=14)).strftime("%mm/%dd/%Y")
        after_59 = (today + timedelta(days=59)).strftime("%mm/%dd/%Y")

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="toDate"]'))
        )

        city_field = self.driver.find_element_by_xpath('//*[@id="searchCriteria"]')
        earliest_date_field = self.driver.find_element_by_xpath('//*[@id="fromDate"]')
        last_date_field = self.driver.find_element_by_xpath('//*[@id="toDate"]')
        continue_button = self.driver.find_element_by_xpath(
            '//*[@id="exchange_form_continue_btn"]'
        )

        city_field.clear()
        last_date_field.clear()
        last_date_field.send_keys(after_59)
        earliest_date_field.send_keys(Keys.CONTROL, "a")
        earliest_date_field.send_keys(Keys.DELETE)
        earliest_date_field.send_keys(after_14)
        city_field.send_keys(city)
        continue_button.click()
        self.driver.find_element_by_xpath('//*[@id="submitButton"]/input').click()

        # Select Number of Bedrooms
        select = Select(
            self.driver.find_element_by_xpath(
                '//*[@id="column2content"]/div/div[2]/form/table/tbody/tr[1]/td[4]/select'
            )
        )
        select.select_by_value("2")
        sleep(1)
        self.driver.find_element_by_xpath(
            '//*[@id="column2content"]/div/div[2]/form/table/tbody/tr[2]/td/input[1]'
        ).click()

    def send_mail(self, mail_content):
        message = MIMEMultipart()
        message["From"] = self.mail_address
        message["To"] = self.mail_address
        message["Subject"] = "Resort Notification"
        message.attach(MIMEText(mail_content, "plain"))
        text = message.as_string()
        self.session.sendmail(self.mail_address, self.mail_address, text)

    def extract_results(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="deposit_a_week"]/a'))
        )
        source = self.driver.page_source
        text = "Sorry, we did not find any matches for your travel dates"
        no_result = text in source
        if no_result:
            print(text)
        else:
            does_exist = False
            matches = [
                x.start()
                for x in re.finditer(r'(.*?)<div class="table_frame">(.*?)', source)
            ]
            for i, start in enumerate(matches):
                if i != len(matches) - 1:
                    end = matches[i + 1]
                else:
                    end = len(source)
                check = TableFrame(source[start:end]).check()
                if check:
                    self.send_mail(check)
                    does_exist = True
            if not does_exist:
                print("No matches found")

    def run(self):
        self.open_site()
        self.search()
        self.extract_results()
        self.session.quit()


bot = MyBot("Zorieric", "vacati0nfun").run()
