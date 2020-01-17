import time
from random import randint
import logging

user_accounts_csv = "user_accounts.csv"
descs_csv = "descs.csv"
complements_csv = "complements.csv"
phrases_csv = "phrases.csv"
generic_dm = "New to pinterest. Want a follow for a follow? I really want an awesome pinterest following like yours!"

write = 'w'
read = "r"
append = 'a'
pin_builder = 'https://www.pinterest.com/pin-builder/'
follower_source = 'https://www.pinterest.com/technews24h/_community/'


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

