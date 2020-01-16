import glob
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import traceback
import csv
import globals as gls
from random import randint

raw_image_list = glob.glob('dld_images/*')
processed_image_list = glob.glob('media/*')
list_of_phrases = []


def read_phrases_from_csv(my_csv):

    try:
        with open(my_csv, gls.read) as rdr:
            reader = csv.reader(rdr, delimiter=",")
            for single_row in reader:
                list_of_phrases.append(single_row)

    except IOError as x:
        print("problem reading the read_descs_from_csv csv", x)
        print(traceback.format_exc())

    except Exception as e:
        print("the read_descs from csv problem is: ", str(e))
        print(traceback.format_exc())

    finally:
        return list_of_phrases


read_phrases_from_csv("phrases.csv")

print(f'number of phrases: {len(list_of_phrases)}')
print(f'number of images: {len(raw_image_list)}')

count = 0
for single_image in raw_image_list:
    print(f'processing {single_image}...')
    random_desc = list_of_phrases[randint(0, len(list_of_phrases) - 1)]
    image = Image.open(single_image)
    newImage = image.resize((600, 900))
    draw = ImageDraw.Draw(newImage)
    font = ImageFont.truetype("./fonts/greatribes.ttf", 65)
    draw.rectangle([0, 0, 600, 100], width=5, fill="#4F4F4F")
    draw.text((70, 5), random_desc[0], fill=(240, 248, 255), font=font)
    newImage.save(f'./processed_media/food/{"pin_image_"}{count}.jpg')
    count += 1

    if count == 3:
        break


print("done")
