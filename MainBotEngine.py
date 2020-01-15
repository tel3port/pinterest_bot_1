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
import traceback
import schedule


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
        print("logging me in....")

        self.driver.get(f"{self.base_url}/login/")
        WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.NAME, "id")))

        # fill up the credential fields
        self.driver.find_element_by_name('id').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)

        # click login button
        try:
            self.driver.find_element_by_xpath('//*[contains(@type,"submit")]').click()

            print("login success...")
        except Exception as e:
            print("the login issue is: ", e)
            print(traceback.format_exc())

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
                if count == 100:
                    break

        except Exception as em:
            print('infinite_scroll Error occurred ' + str(em))
            print(traceback.format_exc())

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
            print(traceback.format_exc())

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
            print(traceback.format_exc())

        except Exception as e:
            print("read_links_from_csv the problem is: ", e)
            print(traceback.format_exc())

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
            print(traceback.format_exc())

        except Exception as e:
            print("the read_descs from csv problem is: ", str(e))
            print(traceback.format_exc())

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
            print("follow user issue, ", e)
            print(traceback.format_exc())

    def pin_image(self, single_desc, single_link, single_image):
        print("pin image start")
        time.sleep(15)

        try:
            self.driver.get(gls.pin_builder)
            title_xpath = '//*[contains(@id,"pin-draft-title")]'
            desc_xpath = '//*[contains(@id,"pin-draft-description")]'
            dest_link_xpath = '//*[contains(@id,"pin-draft-link")]'
            publish_btn_xpath = '//*[contains(@data-test-id,"board-dropdown-save-button")]'
            board_selector = '//*[contains(@title,"Stuff to Buy")]'
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
            print("pin_image problem is at ", e)
            print(traceback.format_exc())


if __name__ == "__main__":

    pn_bot = PinterestBot("2ksaber@gmail.com", "E5XB!D2MerD!XGK")

    list_of_landers = ['https://cool-giveaways.weebly.com/',
                       'https://amzn.to/2Fw2wcz',
                       'https://amzn.to/36C970V',
                       'https://amzn.to/379FhAY'
                       ]
    list_of_descs = pn_bot.read_descs_from_csv(gls.descs_csv)
    links_to_follow = pn_bot.read_links_from_csv(gls.user_accounts_csv)
    image_list = glob.glob('media/*')


    def pin_image_sequence():
        random_image = image_list[randint(0, len(image_list) - 1)]
        random_lander = list_of_landers[randint(0, len(list_of_landers) - 1)]
        random_desc = list_of_descs[randint(0, len(list_of_descs) - 1)]
        pn_bot.pin_image(random_desc, random_lander, random_image)

    def follow_sequence():
        random_user = links_to_follow[randint(0, len(links_to_follow) - 1)]
        pn_bot.follow_user(random_user[0])


    def custom_scheduler():
        # scheduling the pin and follow  and infinite scroll times
        print("starting custom scheduler")

        schedule.every().day.at("11:15").do(pn_bot.infinite_scroll)
        schedule.every().day.at("08:30").do(pn_bot.infinite_scroll)

        schedule.every().day.at("12:01").do(pin_image_sequence)
        schedule.every().day.at("12:37").do(pin_image_sequence)
        schedule.every().day.at("13:05").do(pin_image_sequence)
        schedule.every().day.at("13:44").do(pin_image_sequence)
        schedule.every().day.at("14:07").do(pin_image_sequence)
        schedule.every().day.at("14:55").do(pin_image_sequence)
        schedule.every().day.at("15:03").do(pin_image_sequence)
        schedule.every().day.at("15:39").do(pin_image_sequence)
        schedule.every().day.at("16:16").do(pin_image_sequence)
        schedule.every().day.at("16:40").do(pin_image_sequence)
        schedule.every().day.at("17:10").do(pin_image_sequence)
        schedule.every().day.at("17:53").do(pin_image_sequence)
        schedule.every().day.at("18:25").do(pin_image_sequence)
        schedule.every().day.at("18:45").do(pin_image_sequence)
        schedule.every().day.at("19:02").do(pin_image_sequence)
        schedule.every().day.at("19:37").do(pin_image_sequence)
        schedule.every().day.at("20:22").do(pin_image_sequence)
        schedule.every().day.at("20:44").do(pin_image_sequence)
        schedule.every().day.at("21:11").do(pin_image_sequence)
        schedule.every().day.at("21:20").do(pin_image_sequence)
        schedule.every().day.at("22:15").do(pin_image_sequence)
        schedule.every().day.at("22:30").do(pin_image_sequence)
        schedule.every().day.at("22:44").do(pin_image_sequence)
        schedule.every().day.at("23:01").do(pin_image_sequence)
        schedule.every().day.at("23:40").do(pin_image_sequence)

        schedule.every().day.at("12:07").do(follow_sequence)
        schedule.every().day.at("12:35").do(follow_sequence)
        schedule.every().day.at("13:12").do(follow_sequence)
        schedule.every().day.at("13:45").do(follow_sequence)
        schedule.every().day.at("14:13").do(follow_sequence)
        schedule.every().day.at("14:57").do(follow_sequence)
        schedule.every().day.at("15:13").do(follow_sequence)
        schedule.every().day.at("15:42").do(follow_sequence)
        schedule.every().day.at("16:22").do(follow_sequence)
        schedule.every().day.at("16:44").do(follow_sequence)
        schedule.every().day.at("17:15").do(follow_sequence)
        schedule.every().day.at("17:57").do(follow_sequence)
        schedule.every().day.at("18:29").do(follow_sequence)
        schedule.every().day.at("18:49").do(follow_sequence)
        schedule.every().day.at("19:07").do(follow_sequence)
        schedule.every().day.at("19:44").do(follow_sequence)
        schedule.every().day.at("20:28").do(follow_sequence)
        schedule.every().day.at("20:47").do(follow_sequence)
        schedule.every().day.at("21:18").do(follow_sequence)
        schedule.every().day.at("21:25").do(follow_sequence)
        schedule.every().day.at("22:19").do(follow_sequence)
        schedule.every().day.at("22:39").do(follow_sequence)
        schedule.every().day.at("22:47").do(follow_sequence)
        schedule.every().day.at("23:09").do(follow_sequence)
        schedule.every().day.at("23:43").do(follow_sequence)

        while True:
            schedule.run_pending()
            time.sleep(1)


    custom_scheduler()
