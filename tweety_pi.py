#!/usr/bin/env python
# -*- coding: utf-8 -*-#
import twitter
import os
import sys
import subprocess
import pprint
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def tweety_pi(keywords=["ACoLab"], delay = 15):
    """Follow list of keywords on Twitter and display it on led display"""
    pp = pprint.PrettyPrinter(indent=4)

    display_led("Tweety Pi")
    os.system("matrix/led-matrix -d -r16 -c3 -p11 -D1 -m{delay} tweet.ppm".format(delay=delay))

    #Twitter key needed to connect to Twitter API
    consumer_key="WiZrpKzslTQt3Y0vyIz1qhTeU"
    consumer_secret="Smzs6IoO684EjpRlOGHvTj9JbXjdPec1rIBlA6wdYjUS0hJNh2"
    access_token_key="2243641387-8TtZVCnI9dk5T2suMiQTaXREDy3iYdwNLiCDzFx"
    access_token_secret="yPVbvgRf757IQA6DSetajTXL05NTHkFDImYJBiuSbYUD9"

    #Twitter Authentification
    auth = twitter.OAuth(access_token_key,
                         access_token_secret,
                         consumer_key,
                         consumer_secret)

    #Get the lastest tweet containing keywords
    latest = twitter.Twitter(auth=auth).search.tweets(q=" OR ".join(keywords))
    #Display the latest tweet text
    if latest['statuses']:
        display_led(latest['statuses'][0]['user']['screen_name'] + \
                           " : " + latest['statuses'][0]['text'])
    else:
        display_led("No recent Tweet")
     
    #Connect to the Stream Twitter API
    twitter_stream = twitter.TwitterStream(auth=auth, secure=True)
    print "Waiting for Tweet"
    #Iter over tweet stream containing hashtag
    while True:
        try:
            for msg in twitter_stream.statuses.filter(track=",".join(keywords)):
                if 'text' in msg:
                    display_led(msg['user']['screen_name'] + " : " + msg['text'])
                print "Waiting for Tweet"
            diplay_led("Network connection lost")
        except Exception as e: 
            print e
            continue

def display_led(text):
    """Create an image corresponding to text and pass it as argument to 
    led-matrix software."""
    font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf", 14)
    print "Tweet arrived : ", text
    width = 0
    for letter in text:
        width += font.getsize(letter)[0]

    #Load logo that will be paste at the begining of the picture
    logo = Image.open("/home/pi/display16x32/logo_16x21.ppm")
    logo_width, ignore = logo.size
 
    im = Image.new("RGB", (width + (logo_width + 5) * 2, 16), "black")
    draw = ImageDraw.Draw(im)

    #Paste the logo at the begining of the picture
    im.paste(logo,(0, 0))

    #Start text 5 pixel left to the Logo
    x = logo_width + 5
    section = len(text) / 5
    step = 255 / section
    i = 0

    for letter in text:
        #Create color shading from Blue to Green to Red to Magenta
        if i < section:
            R = 0
            G = step * i
            B = 255
        elif section <= i < 2*section:
            R = 0
            G = 255
            B = 255 - step * (i - section)
        elif 2*section <= i <= 3*section:
            R = step * (i - 2*section)
            G = 255
            B = 0
        elif 3*section <= i <= 4*section:
            R = 255
            G = 255 - step * (i - 3*section)
            B = 0
        elif 4*section <= i <= 5*section:
            R = 255
            G = 0
            B = step * (i - 4*section)

        draw.text((x, 0), letter, fill=(R, G, B), font=font)
        x = x + font.getsize(letter)[0]
        i += 1

    #Paste the logo at the end of the picture
    im.paste(logo,(x + 5, 0))
    
    im.save("tweet.ppm")

if __name__ == '__main__':
    with open('config.json') as data_file:    
        config = json.load(data_file)
    tweety_pi(config["keywords"], config['delay']) 
