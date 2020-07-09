from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


# 1
class MailsParser:
    # driver
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    # mongo
    mongo_client = MongoClient("mongodb://admin:12345@18.197.155.243/my_db")
    my_db = mongo_client.my_db
    mails = my_db.mails

    def get_mails_from_mailru(self):

        self.driver.get('https://mail.ru')

        elem = self.driver.find_element_by_id('mailbox:login')
        elem.send_keys('study.ai_172')

        elem.send_keys(Keys.RETURN)

        elem = WebDriverWait(self.driver, 3).until(
            ec.element_to_be_clickable((By.ID, 'mailbox:password'))
        )
        elem = self.driver.find_element_by_id('mailbox:password')
        elem.send_keys('NextPassword172')

        elem.send_keys(Keys.RETURN)

        mails = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'llc'))
        )

        mails = self.driver.find_elements_by_class_name('llc')

        # scroll to bottom
        last_mail = mails[0]
        for i in range(15):
            mails = WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'llc'))
            )
            mails = self.driver.find_elements_by_class_name('llc')

            # save to mongo
            for mail_item in mails:
                WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable((By.CLASS_NAME, 'llc'))
                )

                mail_data = {
                    'sender': mail_item.find_element_by_class_name('ll-crpt').text,
                    'departure_date': mail_item.find_element_by_class_name('llc__item_date').get_attribute('title'),
                    'subject': mail_item.find_element_by_class_name('ll-sj__normal').text,
                    'mail_link': mail_item.get_attribute('href')
                }

                self.mails.replace_one(mail_data, mail_data, upsert=True)

            # scroll down if don't last element
            if mails[-1] != last_mail:
                last_mail = mails[-1]
                actions = ActionChains(self.driver)
                actions.move_to_element(mails[-1])
                actions.perform()

        # save mail text
        for mail_elem in self.mails.find({}):
            mail_link = mail_elem['mail_link']
            self.driver.get(mail_link)
            text_body = WebDriverWait(self.driver, 3).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'letter-body__body'))
            )

            text_body = self.driver.find_element_by_class_name('letter-body__body').text
            mail_data['mail_text'] = text_body

            self.mails.replace_one(mail_data, mail_data, upsert=True)

            self.driver.back()

        self.driver.quit()


mails_parser = MailsParser()
mails_parser.mails.delete_many({})
mails_parser.get_mails_from_mailru()
count = 0
for mail in mails_parser.mails.find({}):
    print(mail)
    count += 1

print(count)