#!/usr/bin/env python
# -*- coding: utf-8 -*-#
import twitter
import os
#import sys
#import subprocess
import pprint
import time
import itertools
from threading import Thread

from rgbmatrix import RGBMatrix
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def tweety_pi(keywords=["acolab"], myMatrix):
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
    image = create_image(latest['statuses'][0]['user']['screen_name'] + 
                       " : " + latest['statuses'][0]['text'])
    thread_display = display_image(image, myMatrix)
    thread_display.start()

    #Connect to the Stream Twitter API
    twitter_stream = twitter.TwitterStream(auth=auth, secure=True)
    print "Waiting for Tweet"
    #Iter over tweet stream containing hashtag
    for msg in twitter_stream.statuses.filter(track=",".join(keywords)):
        if 'text' in msg:
            image = create_image(msg['user']['screen_name'] + " : " + msg['text'])
            thread_display.load(image)
        print "Waiting for Tweet"
        

def create_image(text):
    """Create an image corresponding to text and pass it as argument to 
    led-matrix software."""
    font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf", 14)
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
    return im
     
class Display_Image(Thread):
    
    """ Thread displaying an image on the led matrix screen"""
    
    def __init__(self, image, myMatrix):
        Thread.__init__(self)
        self.load(image)
        self.myMatrix = myMatrix
        self.Terminated = False
        self.new_image = False

    def run(self):
        horizontal_position = 0
        scroll_jumps = 1
        scroll_ms = 30
        offscreen = myMatrix.CreateFrameCanvas()
        while not self.Terminated:
            for x, y in itertools.product(range(self.image_width), range(self.image_height)):
                if self.new_image:
                    x, y = (0, 0)
                    horizontal_position = 0
                    offscreen.Fill(0,0,0)
                r, g, b = self.pix[(horizontal_position + x) % self.image_width, y]
            offscreen.SetPixel(x, y, r, g, b)
            offscreen = myMatrix.SwapOnVSync(offscreen)
            horizontal_position += scroll_jumps
            if horizontal_position < 0:
                horizontal_position = self.image_width
            time.sleep(scroll_ms / 1000)
    
    def stop(self):
        self.Terminated = True
    
    def load(self, image):
        self.pix = image.load()
        self.image_width, self.image_height = image.size
        self.new_image = True

if __name__ == '__main__':
    #Initiate led matrix screen size
    rows = 16
    chains = 3
    parallel = 1
    myMatrix = RGBMatrix(rows, chains, parallel)
    tweety_pi(sys.argv[1:], myMatrix)
