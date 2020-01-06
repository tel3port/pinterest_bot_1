from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import globals as gls
import logging
import glob
import sys
import os

image_list = glob.glob('/media/*')


class PinterestBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome("./chromedriver")
        self. base_url = "https://www.pinterest.com"
        self.login()

    def login(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver.get(f"{self.base_url}/login/")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "id")))

        # fill up the credential fields
        self.driver.find_element_by_name('id').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)

        # click login button
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div/div[3]/form/div[5]/button').click()

    def nav_user(self, user):
        self.driver.get(f'{self.base_url}/{user}/')

    def infinite_scroll(self):
        scroll_pause_time = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    @staticmethod
    def append_to_csv(saved_links_list, my_csv):
        gls.log_file_writer()
        try:
            this_csv = open(my_csv, gls.append)
            csv_writer = csv.writer(this_csv)
            for single_link in saved_links_list:
                csv_writer.writerow([str(single_link)])
                print("row (hopefully) written into csv")

        except Exception as em:
            logging.error('Error occurred ' + str(em))
            print('Error occurred ' + str(em))

        finally:
            print(" write_to_csv() done")

            pass

    @staticmethod
    def read_from_csv(my_csv):
        list_of_links = []
        try:
            with open(my_csv, gls.read) as rdr:
                reader = csv.reader(rdr, delimiter=",")
                for single_row in reader:
                    list_of_links.append(single_row)

        except IOError as x:
            print("problem reading the user_accounts csv")
            logging.error('Error occurred ' + str(x))
        except Exception as e:
            print("the problem is: ", e)
            logging.error('Error occurred ' + str(e))

        finally:
            print(list_of_links)
            pass

    def follow_user(self, user):
        self.nav_user(user)
        time.sleep(5)

        button_xpath = "//button[contains(.,'Follow')]"

        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        element.click()
        print(f"{user} followed!")

    def extract_users_from_dialog(self):
        links_set = set()
        self.driver.get("https://www.pinterest.com/technews24h/_community/")
        btn_xpath = '//*[@id="__PWS_ROOT__"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div[2]/button'

        el = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
        el.click()

        time.sleep(200)
        results = self.driver.find_elements_by_xpath('//a[@href]')

        print(f"size of results {len(results)}")

        for res in results:
            final_link = res.get_attribute('href')
            print(final_link)
            links_set.add(final_link)

        self.append_to_csv(list(links_set), gls.user_accounts_csv)

    def pin_image(self):
        self.driver.get(gls.pin_builder)
        title_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div/div[1]/textarea'
        desc_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/textarea'
        dest_link_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/textarea'
        publish_btn_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/button[2]'
        board_selector = '//*[@id="__PWS_ROOT__"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div'
        self.driver.find_element_by_xpath(title_xpath).send_keys("2020 be like...")
        time.sleep(5)
        self.driver.find_element_by_xpath(desc_xpath).send_keys("winning at life")
        time.sleep(4)
        self.driver.find_element_by_xpath(dest_link_xpath).send_keys('https://cool-giveaways.weebly.com/')
        time.sleep(7)

        self.driver.find_element_by_id('media-upload-input').send_keys(os.getcwd()+image_list[0])

        self.driver.find_element_by_xpath(publish_btn_xpath).click() # to reveal the menu
        board = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, board_selector)))

        actions = ActionChains(self.driver)
        actions.move_to_element(board).click().perform()
        time.sleep(3)
        self.driver.find_element_by_xpath(publish_btn_xpath).click()  # to publish the pin

    def follow_and_comment(self):
        self.driver.get('https://www.pinterest.com/homefeed/')
        parsed_results_list = []

        home_screen_results = self.driver.find_elements_by_xpath('//a[@href]')

        print(f"size of results {len(home_screen_results)}")

        for res in home_screen_results:
            try:
                final_link = res.get_attribute('href')
                print(final_link)
                button_xpath = '//*[@id="__PWS_ROOT__"]/div[1]/div[3]/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/button/div'

                element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                element.click()
                print(f"{element} followed!")

            except Exception as e:
                print("the issue is: ", e)


if __name__ == "__main__":
    pn_bot = PinterestBot("testerslimited@gmail.com", "E5XB!D2MerD!XGK")
    time.sleep(5)
    pn_bot.extract_users_from_dialog()
    pn_bot.read_from_csv(gls.user_accounts_csv)
    pn_bot.pin_image()










