#!/usr/bin/env python
# -*- coding: utf-8 -*-#
import twitter
import os
import sys
import time
import itertools
from threading import Thread
import json

from rgbmatrix import RGBMatrix
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def tweety_pi(myMatrix, keywords, speed=1):
    """Follow list of keywords on Twitter and display it on led display"""
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
    latest = twitter.Twitter(auth=auth).search.tweets(q=" OR ".join(keywords), 
                                                      result_type="recent", 
                                                      count=1)
    #Display the latest tweet text
    if len(latest['statuses']):
        image = create_image(latest['statuses'][0]['user']['screen_name'] + " : " + latest['statuses'][0]['text'])
        #image = create_image("test")
        thread_display = Display_Image(image, myMatrix, speed)
        thread_display.start()
        thread_display.join()

def create_image(text):
    """Create an image corresponding to text and pass it as argument to 
    led-matrix software."""
    font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf", 14)
    print "Tweet arrived : ", text
    text_width, ignore = font.getsize(text)

    #Load logo that will be paste at the begining of the picture
    logo = Image.open("logo_16x21.ppm")
    logo_width, ignore = logo.size
 
    im = Image.new("RGB", (99 + logo_width + text_width + logo_width + 30, 16), "black")
    draw = ImageDraw.Draw(im)

    x = 99
    #Paste the logo at the begining of the picture
    im.paste(logo,(x, 0))

    #Start text 5 pixel left to the Logo
    x = x + logo_width + 5
    section = (len(text) / 5) + 1
    #section = (text_width / 5) + 1
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
    
    def __init__(self, image, myMatrix, s):
        Thread.__init__(self)
        self.load(image)
        self.myMatrix = myMatrix
        self.Terminated = False
        self.new_image = False
        self.speed = s

    def run(self):
        horizontal_position = 0
	# Set speed :
        scroll_jumps = self.speed * 2
        scroll_ms = 1 
        offscreen = self.myMatrix.CreateFrameCanvas()
        im_width = self.image_width
        im_height = self.image_height
        screen_width = self.myMatrix.width
        screen_height = self.myMatrix.height
        pixl = self.pix
        while not self.Terminated:
            for x, y in itertools.product(range(screen_width), range(screen_height)):
                r, g, b = pixl[(horizontal_position + x) % im_width + y * im_width]
                offscreen.SetPixel(x, y, r, g, b)
            offscreen = self.myMatrix.SwapOnVSync(offscreen)
            horizontal_position += scroll_jumps
            if horizontal_position > im_width:
		self.stop()
            if horizontal_position < 0:
                horizontal_position = im_width
    
    def stop(self):
        self.Terminated = 1
    
    def load(self, image):
        self.pix = list(image.getdata())
        self.image_width, self.image_height = image.size
        self.new_image = True

if __name__ == '__main__':
    #Initiate led matrix screen size
    rows = 16
    chains = 3
    parallel = 1
    myMatrix = RGBMatrix(rows, chains, parallel)
    myMatrix.pwmBits = 11
    with open('config.json') as data_file:    
        config = json.load(data_file)
    while 1:
        tweety_pi(myMatrix, config["keywords"], config['speed']) 
