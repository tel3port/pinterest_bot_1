import time
from random import randint
import logging

user_accounts_csv = "user_accounts.csv"
descs_csv = "descs.csv"
complements_csv = "complements.csv"
phrases_csv = "phrases.csv"
generic_dm = "I would like to collaborate with you on a new project. Here is an example of what i do"

write = 'w'
read = "r"
append = 'a'
pin_builder = 'https://www.pinterest.com/pin-builder/'
follower_source = 'https://www.pinterest.com/technews24h/_community/'
board_creator = 'https://www.pinterest.com/marlinx2020/boards/'


def random_search_term():
    list_of_search_terms = ["ice cream phone wallpaper", "chocolate cake phone wallpaper", "vanilla cake phone wallpaper",
                            "frozen yoghurt phone wallpaper", "cookies phone wallpaper", "custard phone wallpaper",
                            "pudding phone wallpaper", 'custard phone wallpaper', "coffee phone wallpaper",
                            "rock candy phone wallpaper"]

    return list_of_search_terms[randint(0, len(list_of_search_terms) - 1)]


def random_lander():
    list_of_landers = ['https://cool-giveaways.weebly.com/',
                       'https://win-150-dollars-now.weebly.com/',
                       'https://freebie-heaven.weebly.com/',
                       'https://win-google-pixel-now.weebly.com/',
                       'https://win-nintendo-switch-now.weebly.com/',
                       'https://win-a-fortune-today.weebly.com/',
                       'https://amzn.to/379FhAY'
                       ]
    return list_of_landers[randint(0, len(list_of_landers) - 1)]

def random_emotion():
    list_of_emotions = [' HATE ', ' adore ', ' devote to ', ' love ', " like ", ' dislike ', " enjoy ", " am angry at ", " feel sad for ", " am surprised by ", ' trust ', " anticipate ", ' crave ', " am interested in ", " satisfy "]

    return list_of_emotions[randint(0, len(list_of_emotions) - 1)]


def sleep_time():
    t = randint(7, 65)
    print(f"thread sleeping for {t} seconds...")

    time.sleep(t)

    return t


# def log_file_writer():
#     return logging.basicConfig(filename='errors.log',
#                                format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#                                datefmt='%Y-%m-%d:%H:%M:%S',
#                                level=logging.DEBUG)

