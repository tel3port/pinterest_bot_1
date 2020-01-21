from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import globals as gls
import glob
from random import randint
import traceback
import schedule
import time
import requests
import os
import io
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import hashlib


class PinterestBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.random_search_term = gls.random_search_term()
        self.random_emotion = gls.random_emotion()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-sgm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        # self.driver = webdriver.Chrome("./chromedriver",)
        self. base_url = "https://www.pinterest.com"
        self.login()

    def login(self):
        print("logging me in....")
        print("session id at login: ", self.driver.session_id)

        try:

            self.driver.get(f"{self.base_url}/login/")
            WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.NAME, "id")))

            # fill up the credential fields
            self.driver.find_element_by_name('id').send_keys(self.username)
            self.driver.find_element_by_name('password').send_keys(self.password)

            self.driver.find_element_by_xpath('//*[contains(@type,"submit")]').click()

            print("login success...")
        except Exception as e:
            print("the login issue is: ", e)
            print(traceback.format_exc())
            pass

    def infinite_scroll(self):
        print("starting infinite scroll")
        time.sleep(10)
        try:
            print("session id at infinite scroll: ", self.driver.session_id)
            self.driver.get('https://www.pinterest.com/homefeed/')
            count = 0
            scroll_pause_time = 6

            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            time.sleep(3)

            random_num = randint(5, 8)
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
                print(f'number of scrolls', count)
                if count == random_num:
                    break

        except Exception as em:
            print('infinite_scroll Error occurred ' + str(em))
            print(traceback.format_exc())
            pass

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
            pass

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
            pass

        except Exception as e:
            print("read_links_from_csv the problem is: ", e)
            print(traceback.format_exc())
            pass

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
            pass

        except Exception as e:
            print("the read_descs from csv problem is: ", str(e))
            print(traceback.format_exc())
            pass

        finally:
            return list_of_descriptions

    @staticmethod
    def read_complements_from_csv(my_csv):
        complements_list = []
        try:
            with open(my_csv, gls.read) as rdr:
                reader = csv.reader(rdr, delimiter=",")
                for single_row in reader:
                    complements_list.append(single_row)

        except IOError as x:
            print("problem reading the read_descs_from_csv csv", x)
            print(traceback.format_exc())
            pass

        except Exception as e:
            print("the read_descs from csv problem is: ", str(e))
            print(traceback.format_exc())
            pass

        finally:
            return complements_list

    # -------------------- pinterest functionality section -----------------------------------------------------------------------
    # TODO create boards dynamically and check if they exist before creation
    def board_creator(self):
        pass

    def follow_user(self, user_link):
        print("follow user started")
        print("session id at follow user: ", self.driver.session_id)

        time.sleep(15)
        try:
            self.driver.get(user_link)
            time.sleep(15)

            button_xpath = "//button[contains(.,'Follow')]"

            element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            time.sleep(15)

            element.click()
            print(f"{user_link} followed!")

            time.sleep(7)

        except Exception as e:
            print("follow user issue, ", e)
            print(traceback.format_exc())
        finally:
            self.dm_single_user(user_link)

    def dm_single_user(self, user_link):
        print("session id at dm_single_user: ", self.driver.session_id)

        try:
            message_button_xpath = "//button[contains(.,'Message')]"
            dm_input_xpath = '//*[contains(@id,"message")]'
            send_btn_xpath = "//button[contains(.,'Send')]"

            element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, message_button_xpath)))
            time.sleep(15)
            element.click()
            self.driver.find_element_by_xpath(dm_input_xpath).send_keys(gls.generic_dm)
            time.sleep(5)
            self.driver.find_element_by_xpath(send_btn_xpath).click()

            print(f"{user_link} DM'd!")

        except Exception as e:
            print("DM user issue, ", e)
            print(traceback.format_exc())
            pass

    def pin_image(self, single_desc, single_link, single_image):
        print("pin image start")
        print("session id at pin_image: ", self.driver.session_id)

        time.sleep(15)
        random_search_term = gls.random_search_term()
        random_emotion = gls.random_emotion()

        try:
            self.driver.get(gls.pin_builder)
            title_xpath = '//*[contains(@placeholder,"Add your title")]'
            desc_xpath = '//*[contains(@id,"pin-draft-description")]'
            dest_link_xpath = '//*[contains(@id,"pin-draft-link")]'
            publish_btn_xpath = '//*[contains(@data-test-id,"board-dropdown-save-button")]'
            board_selector = f'//*[contains(@title,"{random_search_term}")]'

            self.driver.find_element_by_xpath(title_xpath).send_keys(f'I{random_emotion}{random_search_term}')
            time.sleep(5)
            self.driver.find_element_by_xpath(desc_xpath).send_keys(f'{random_search_term}! {single_desc}')
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
            pass

    def pin_link_extractor(self, list_complements):
        print("session id at pin_link_extractor: ", self.driver.session_id)

        links_set = set()
        try:
            time.sleep(7)
            self.driver.get('https://www.pinterest.com/following/')

            time.sleep(5)
            results = self.driver.find_elements_by_xpath('//a[@href]')

            print(f"number of pin links {len(results)}")

            for res in results:
                final_link = res.get_attribute('href')
                links_set.add(final_link)

            count = 0
            random_num = randint(3, 7)
            for single_link in list(links_set):
                if 'pinterest.com/pin/' in single_link:
                    self.image_commenter(single_link, list_complements)

                    time.sleep(randint(10, 15))

                count += 1
                print("number of comments", count)
                if count == random_num:
                    break

            links_set.clear()

        except Exception as we:
            print('image_commenter Error occurred ' + str(we))
            print(traceback.format_exc())
            pass

    def image_commenter(self, pin_link, list_complements):
        print("session id at image_commenter: ", self.driver.session_id)

        print('xxxxxx  pin_link xxxxxxxx')
        random_complement = list_complements[randint(0, len(list_complements) - 1)]
        print(random_complement)
        print(pin_link)

        comment_tab_xpath = '//*[contains(@data-test-id,"canonicalCommentsTab")]'
        comment_label = '//*[contains(@name,"communityItemTextBox")]'
        comment_textbox = '//*[contains(@data-test-id,"mentionsInput")]'
        submit_comment_btn_xpath = '//*[contains(@data-test-id,"activity-item-create-submit")]'

        try:
            self.driver.get(pin_link)

            tab = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, comment_tab_xpath)))
            time.sleep(5)
            tab.click()
            time.sleep(5)
            self.driver.find_element_by_xpath(comment_label).click()
            time.sleep(5)
            self.driver.find_element_by_xpath(comment_textbox).send_keys(random_complement)
            time.sleep(7)
            self.driver.find_element_by_xpath(submit_comment_btn_xpath).click()
            time.sleep(15)
            print("commenting done!")
        except Exception as we:
            print('image_commenter Error occurred ' + str(we))
            print(traceback.format_exc())

    # -------------------- image downloader section -----------------------------------------------------------------------

    @staticmethod
    def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)

            # build the google query

        # build the google query
        search_url = 'https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img'

        time.sleep(12)
        print(f'current session id fetch_image_urls: {wd.session_id}')

        # # open tab
        # current = wd.current_window_handle
        # wd.execute_script("window.open();")
        # new_tab = [tab for tab in wd.window_handles if tab != current][0]
        # wd.switch_to.window(new_tab)
        # You can use (Keys.CONTROL + 't') on other OSs
        # load the page
        time.sleep(12)
        wd.get(search_url.format(q=query))

        image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            try:
                scroll_to_end(wd)

                # get all image thumbnail results
                thumbnail_results = wd.find_elements_by_css_selector("img.rg_ic")
                number_results = len(thumbnail_results)

                print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

                for img in thumbnail_results[results_start:number_results]:
                    # try to click every thumbnail such that we can get the real image behind it
                    try:
                        img.click()
                        time.sleep(sleep_between_interactions)
                    except Exception as e:
                        print("the problem is, ", str(e))
                        continue

                    # extract image urls
                    actual_images = wd.find_elements_by_css_selector('img.irc_mi')
                    for actual_image in actual_images:
                        if actual_image.get_attribute('src'):
                            image_urls.add(actual_image.get_attribute('src'))

                    image_count = len(image_urls)

                    if len(image_urls) >= max_links_to_fetch:
                        print(f"Found: {len(image_urls)} image links, done!")
                        break
                else:
                    print("Found:", len(image_urls), "image links, looking for more ...")
                    time.sleep(1)
                    load_more_button = wd.find_element_by_css_selector(".ksb")
                    if load_more_button:
                        wd.execute_script("document.querySelector('.ksb').click();")

                # move the result startpoint further down
                results_start = len(thumbnail_results)

            except Exception as we:
                print('image_refresh_sequence Error occurred ' + str(we))
                print(traceback.format_exc())
                pass

            # close the tab
            # finally:
            #     wd.close()
            #
            #     wd.switch_to.window(current)

        return image_urls

    @staticmethod
    def persist_image(folder_path: str, url: str):
        try:
            image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")
            pass

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print(f"SUCCESS - saved {url} - as {file_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
            pass

    def search_and_download(self, search_term: str, driver_path: str, target_path='./dld_images', number_images=5):
        target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))
        target_folder = './dld_images'
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        print("session id at search_and_download: ", self.driver.session_id)

        # with webdriver.Chrome(executable_path=driver_path) as wd:
        res = self.fetch_image_urls(search_term, number_images, wd=self.driver, sleep_between_interactions=0.5)

        for elem in res:
            self.persist_image(target_folder, elem)

# -------------------- image optimiser section -----------------------------------------------------------------------

    @staticmethod
    def read_phrases_from_csv(my_csv):
        list_of_phrases = []
        try:
            with open(my_csv, gls.read) as rdr:
                reader = csv.reader(rdr, delimiter=",")
                for single_row in reader:
                    list_of_phrases.append(single_row)

        except IOError as x:
            print("problem reading the read_descs_from_csv csv", x)
            print(traceback.format_exc())
            pass

        except Exception as e:
            print("the read_descs from csv problem is: ", str(e))
            print(traceback.format_exc())
            pass

        finally:
            return list_of_phrases

    def image_optimiser(self, my_csv):
        print("session id at image_optimiser: ", self.driver.session_id)

        try:
            self.read_phrases_from_csv(my_csv)

            raw_image_list = glob.glob('dld_images/*')
            # processed_image_list = glob.glob('media/*')
            final_phrase_list = self.read_phrases_from_csv(gls.phrases_csv)

            print(f'number of phrases: {len(final_phrase_list)}')
            print(f'number of images: {len(raw_image_list)}')

            count = 0
            for single_image in raw_image_list:
                print(f'processing {single_image}...')
                random_desc = final_phrase_list[randint(0, len(final_phrase_list) - 1)]
                image = Image.open(single_image)
                new_image = image.resize((600, 900))
                draw = ImageDraw.Draw(new_image)
                font = ImageFont.truetype("./fonts/eternity.ttf", 65)
                draw.rectangle([0, 0, 600, 151], width=5, fill=(randint(0, 255), randint(0, 255), randint(0, 255)), )
                draw.text((70, 5), random_desc[0], fill=(randint(0, 255), randint(0, 255), randint(0, 255)), font=font)
                new_image.save(f'./media/{"final_img_"}{count}.jpg')
                count += 1

            print(" image optimisation done")

        except Exception as we:
            print('image_optimiser Error occurred ' + str(we))
            print(traceback.format_exc())
            pass

    # -------------------- image refresher section -----------------------------------------------------------------------

    @staticmethod
    def image_deleter():
        try:
            for i in glob.glob("./dld_images/*.jpg"):
                os.remove(i)

        except Exception as we:
            print('image_deleter Error occurred ' + str(we))
            print(traceback.format_exc())
            pass

    # -------------------- bot's entry point -----------------------------------------------------------------------


if __name__ == "__main__":

    pn_bot = PinterestBot("2ksaber@gmail.com", "E5XB!D2MerD!XGK")
    print(f'search term in play: {pn_bot.random_search_term}')
    list_of_landers = ['https://cool-giveaways.weebly.com/',
                       'https://win-150-dollars-now.weebly.com/',
                       'https://freebie-heaven.weebly.com/',
                       'https://win-google-pixel-now.weebly.com/',
                       'https://win-nintendo-switch-now.weebly.com/',
                       'https://win-a-fortune-today.weebly.com/',
                       'https://amzn.to/379FhAY'
                       ]
    list_of_descs = pn_bot.read_descs_from_csv(gls.descs_csv)
    links_to_follow = pn_bot.read_links_from_csv(gls.user_accounts_csv)

    # refreshes images 3 times a week
    def image_refresh_sequence():
        time.sleep(5)
        try:
            pn_bot.search_and_download(pn_bot.random_search_term, './chromedriver', './dld_images', 35)
            time.sleep(10)
            pn_bot.image_optimiser(gls.phrases_csv)
            pn_bot.image_deleter()

        except Exception as we:
            print('image_refresh_sequence Error occurred ' + str(we))
            print(traceback.format_exc())
            pass

    # pins to account
    def pin_image_sequence():
        image_list = glob.glob('media/*')
        random_image = image_list[randint(0, len(image_list) - 1)]
        random_lander = list_of_landers[randint(0, len(list_of_landers) - 1)]
        random_desc = list_of_descs[randint(0, len(list_of_descs) - 1)]
        pn_bot.pin_image(random_desc, random_lander, random_image)

    # follows  and dms users from the csv
    def follow_sequence():
        random_user = links_to_follow[randint(0, len(links_to_follow) - 1)]
        pn_bot.follow_user(random_user[0])

    # comments on pins of people being followed
    def comment_sequence():
        list_of_complements = pn_bot.read_complements_from_csv(gls.complements_csv)
        print(f'complement list size: {len(list_of_complements)}')
        pn_bot.pin_link_extractor(list_of_complements)

    # schedules when the above actions should be done
    def custom_pinterest_bot_1_scheduler():
        # scheduling the pin and follow  and infinite scroll times
        print("starting custom scheduler")

        # schedule.every().monday.at("03:03").do(image_refresh_sequence)
        # schedule.every().wednesday.at("03:21").do(image_refresh_sequence)
        schedule.every().day.at("03:57").do(image_refresh_sequence)

        schedule.every().day.at("08:10").do(pn_bot.infinite_scroll)
        schedule.every().day.at("09:00").do(comment_sequence)
        schedule.every().day.at("09:45").do(pn_bot.infinite_scroll)
        schedule.every().day.at("10:23").do(comment_sequence)

        schedule.every().day.at("12:01").do(pin_image_sequence)
        schedule.every().day.at("12:31").do(pin_image_sequence)
        schedule.every().day.at("13:01").do(pin_image_sequence)
        schedule.every().day.at("13:31").do(pin_image_sequence)
        schedule.every().day.at("14:01").do(pin_image_sequence)
        schedule.every().day.at("14:31").do(pin_image_sequence)
        schedule.every().day.at("15:01").do(pin_image_sequence)
        schedule.every().day.at("15:31").do(pin_image_sequence)
        schedule.every().day.at("16:01").do(pin_image_sequence)
        schedule.every().day.at("16:31").do(pin_image_sequence)
        schedule.every().day.at("17:01").do(pin_image_sequence)
        schedule.every().day.at("17:31").do(pin_image_sequence)
        schedule.every().day.at("18:01").do(pin_image_sequence)
        schedule.every().day.at("18:31").do(pin_image_sequence)
        schedule.every().day.at("19:01").do(pin_image_sequence)
        schedule.every().day.at("19:31").do(pin_image_sequence)
        schedule.every().day.at("20:01").do(pin_image_sequence)
        schedule.every().day.at("20:31").do(pin_image_sequence)
        schedule.every().day.at("21:01").do(pin_image_sequence)
        schedule.every().day.at("21:31").do(pin_image_sequence)
        schedule.every().day.at("22:01").do(pin_image_sequence)
        schedule.every().day.at("22:31").do(pin_image_sequence)
        schedule.every().day.at("22:01").do(pin_image_sequence)
        schedule.every().day.at("23:31").do(pin_image_sequence)
        schedule.every().day.at("23:01").do(pin_image_sequence)

        schedule.every().day.at("12:23").do(follow_sequence)
        schedule.every().day.at("12:44").do(follow_sequence)
        schedule.every().day.at("13:23").do(follow_sequence)
        schedule.every().day.at("13:44").do(follow_sequence)
        schedule.every().day.at("14:23").do(follow_sequence)
        schedule.every().day.at("14:44").do(follow_sequence)
        schedule.every().day.at("15:23").do(follow_sequence)
        schedule.every().day.at("15:44").do(follow_sequence)
        schedule.every().day.at("16:23").do(follow_sequence)
        schedule.every().day.at("16:44").do(follow_sequence)
        schedule.every().day.at("17:23").do(follow_sequence)
        schedule.every().day.at("17:44").do(follow_sequence)
        schedule.every().day.at("18:23").do(follow_sequence)
        schedule.every().day.at("18:44").do(follow_sequence)
        schedule.every().day.at("19:23").do(follow_sequence)
        schedule.every().day.at("19:44").do(follow_sequence)
        schedule.every().day.at("20:23").do(follow_sequence)
        schedule.every().day.at("20:44").do(follow_sequence)
        schedule.every().day.at("21:23").do(follow_sequence)
        schedule.every().day.at("21:44").do(follow_sequence)
        schedule.every().day.at("22:23").do(follow_sequence)
        schedule.every().day.at("22:44").do(follow_sequence)
        schedule.every().day.at("22:23").do(follow_sequence)
        schedule.every().day.at("23:44").do(follow_sequence)
        schedule.every().day.at("23:23").do(follow_sequence)

        while 1:
            schedule.run_pending()
            time.sleep(1)

    #  FOR LOCAL TESTING ONLY
    # def run_locally():
    #     for _ in range(5):
    #         # pn_bot.infinite_scroll()
    #         # comment_sequence()
    #         # image_refresh_sequence()
    #         pin_image_sequence()
    #         # follow_sequence()
    #
    # run_locally()
    # print("test done")

    custom_pinterest_bot_1_scheduler()
