#!/usr/bin/env python
# -*- coding: utf-8 -*-#
import twitter
import os
import sys
import subprocess
import pprint

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def tweety_pi(keywords=["Cabu"]):
    """Follow list of keywords on Twitter and display it on led display"""
    pp = pprint.PrettyPrinter(indent=4)
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
    latest = twitter.Twitter(auth=auth).search.tweets(q=" ".join(keywords), 
                                                      result_type="recent", 
                                                      count=1)
    
    #Display the latest tweet text
    display_led(latest['statuses'][0]['user']['screen_name'] + 
                       " : " + latest['statuses'][0]['text'])

    #Connect to the Stream Twitter API
    twitter_stream = twitter.TwitterStream(auth=auth, secure=True)
    print "Waiting for Tweet"
    #Iter over tweet stream containing hashtag
    for msg in twitter_stream.statuses.filter(track=",".join(keywords)):
        if 'text' in msg:
            display_led(msg['user']['screen_name'] + " : " + msg['text'])
        print "Waiting for Tweet"

def display_led(text):
    """Create an image corresponding to text and pass it as argument to 
    led-matrix software."""
    font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf", 14)
#    #Find the PID of the process, if it exist, and return it
#    PID = subprocess.check_output("pidof led-matrix", shell=True).split(" ")[0]
#    if PID:
#        print "Kill process : ", PID
#        os.system("kill " + PID)
    print "Tweet arrived : ", text
    width, ignore = font.getsize(text)

    #Load logo that will be paste at the begining of the picture
    logo = Image.open("logo_16x21.ppm")
    logo_width, ignore = logo.size
 
    im = Image.new("RGB", (width + logo_width + 90, 16), "black")
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
     
#    os.system("./rpi-rgb-led-matrix/led-matrix -d -r16 -c3 -p11 -D1 tweet.ppm")

if __name__ == '__main__':
    tweety_pi(sys.argv[1:])
