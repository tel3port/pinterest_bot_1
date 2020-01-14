from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import globals as gls
import glob
import os
from random import randint


class PinterestBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-sgm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
        # self.driver = webdriver.Chrome("./chromedriver",)
        self. base_url = "https://www.pinterest.com"
        self.login()

    def login(self):

        self.driver.get(f"{self.base_url}/login/")
        WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.NAME, "id")))

        # fill up the credential fields
        self.driver.find_element_by_name('id').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)

        # click login button
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div/div[3]/form/div[5]/button').click()
        except Exception as e:
            print("the login issue is: ", e.with_traceback())

    def infinite_scroll(self):
        print("starting infinite scroll")
        time.sleep(10)
        try:
            self.driver.get('https://www.pinterest.com/homefeed/')
            count = 0
            scroll_pause_time = 30

            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            time.sleep(3)

            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(scroll_pause_time)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                time.sleep(3)

                if new_height == last_height:
                    break
                last_height = new_height

                count += 1
                if count == 5:
                    break

        except Exception as em:
            print('infinite_scroll Error occurred ' + str(em))

        finally:
            print(" infinite_scroll() done")

    @staticmethod
    def append_to_csv(saved_links_list, my_csv):
        try:
            this_csv = open(my_csv, gls.append)
            csv_writer = csv.writer(this_csv)
            for one_link in saved_links_list:
                csv_writer.writerow([str(one_link)])
                print("row (hopefully) written into csv")

        except Exception as em:
            print('append_to_csv Error occurred ' + str(em))

        finally:
            print(" append_to_csv() done")

            pass

    @staticmethod
    def read_links_from_csv(my_csv):
        list_of_links = []
        try:
            with open(my_csv, gls.read) as rdr:
                reader = csv.reader(rdr, delimiter=",")
                for single_row in reader:
                    list_of_links.append(single_row)

        except IOError as x:
            print("read_links_from_csv problem reading the user_accounts csv", x)
        except Exception as e:
            print("read_links_from_csv the problem is: ", e)

        finally:
            print("number of links: ", len(list_of_links))
            return list_of_links

    @staticmethod
    def read_descs_from_csv(my_csv):
        list_of_descriptions = []
        try:
            with open(my_csv, gls.read) as rdr:
                reader = csv.reader(rdr, delimiter=",")
                for single_row in reader:
                    list_of_descriptions.append(single_row)

        except IOError as x:
            print("problem reading the read_descs_from_csv csv", x)
        except Exception as e:
            print("the read_descs from csv problem is: ", str(e))

        finally:
            return list_of_descriptions

    def follow_user(self, user_link):
        print("follow user started")
        time.sleep(15)
        try:
            self.driver.get(user_link)
            time.sleep(15)

            button_xpath = "//button[contains(.,'Follow')]"

            element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            time.sleep(15)

            element.click()
            print(f"{user_link} followed!")
        except Exception as e:
            print("follow_user problem is at ", e.with_traceback())

    def pin_image(self, single_desc, single_link, single_image):
        print("pin image start")
        time.sleep(15)

        try:
            self.driver.get(gls.pin_builder)
            title_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div/div[1]/textarea'
            desc_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/textarea'
            dest_link_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/textarea'
            publish_btn_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/button[2]'
            board_selector = '//*[@id="__PWS_ROOT__"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div'
            self.driver.find_element_by_xpath(title_xpath).send_keys(f"Today's giveaway.ONLY {randint(3,23)} PRIZES remain!")
            time.sleep(5)
            self.driver.find_element_by_xpath(desc_xpath).send_keys(single_desc)
            time.sleep(4)
            self.driver.find_element_by_xpath(dest_link_xpath).send_keys(single_link)
            time.sleep(7)

            self.driver.find_element_by_id('media-upload-input').send_keys(f"{os.getcwd()}{'/'}{single_image}")

            self.driver.find_element_by_xpath(publish_btn_xpath).click()  # to reveal the menu
            board = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, board_selector)))

            actions = ActionChains(self.driver)
            actions.move_to_element(board).click().perform()
            time.sleep(3)
            self.driver.find_element_by_xpath(publish_btn_xpath).click()  # to publish the pin
            print("pin image done")

        except Exception as e:
            print("pin_image problem is at ", e.with_traceback())

    def kill_browser(self):
        self.driver.quit()


if __name__ == "__main__":

    while 1:

        pn_bot = PinterestBot("testerslimited@gmail.com", "E5XB!D2MerD!XGK")

        pn_bot.infinite_scroll()

        # pn_bot.extract_users_from_dialog(gls.follower_source)

        list_of_landers = ['https://cool-giveaways.weebly.com/',
                           'https://amzn.to/2Fw2wcz',
                           'https://amzn.to/36C970V',
                           'https://amzn.to/379FhAY'
                           ]
        list_of_descs = pn_bot.read_descs_from_csv(gls.descs_csv)
        links_to_follow = pn_bot.read_links_from_csv(gls.user_accounts_csv)
        image_list = glob.glob('media/*')

        for i in range(100):
            random_lander = list_of_landers[randint(0, len(list_of_landers) - 1)]
            random_desc = list_of_descs[randint(0, len(list_of_descs) - 1)]
            random_image = image_list[randint(0, len(image_list) - 1)]

            time.sleep(7)
            pn_bot.pin_image(random_desc, random_lander, random_image)
            time.sleep(randint(3, 30))

            random_user = links_to_follow[randint(0, len(links_to_follow) - 1)]
            pn_bot.follow_user(random_user[0])
            time.sleep(randint(3, 30))

            pn_bot.infinite_scroll()
            time.sleep(randint(3, 30))

            another_random_user = links_to_follow[randint(0, len(links_to_follow) - 1)]
            pn_bot.follow_user(another_random_user[0])
            time.sleep(randint(3, 30))

            yet_another_random_user = links_to_follow[randint(0, len(links_to_follow) - 1)]
            pn_bot.follow_user(yet_another_random_user[0])
            time.sleep(randint(3, 30))





        pn_bot.infinite_scroll()
        pn_bot.kill_browser()
        time.sleep(randint(5, 50))
