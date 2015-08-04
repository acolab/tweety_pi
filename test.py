#!/usr/bin/env python
"""
Mock-up to optimize image parsing in similar situation than actual one
"""

#Import module to handle led matrix display
from rgbmatrix import RGBMatrix

import time
import itertools
import random

#Init matrix display
rows = 16
chains = 3
parallel = 1
myMatrix = RGBMatrix(rows, chains, parallel)
myMatrix.pwmBits = 1
myMatrix.luminanceCorrect = False

#Create a buffer of the matrix display to hold new image before displaying
offscreen = myMatrix.CreateFrameCanvas()

#Speed test loop
for i in xrange(10):
    
    #Init random image
    image = [(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)) for i in xrange(myMatrix.width*myMatrix.height)]
    
    start = time.time()
    screen_width = offscreen.width
    screen_height = offscreen.height
    setpixel = offscreen.SetPixel
    #[r,g,b = image[x + y*screen_width] ; setpixel(x,y,r,g,b) for x,y in itertools.product(range(screen_width), range(screen_height))]
    
    #Iterate over the image to get RGB value for a given x,y position - loop to optimize
    for x,y in itertools.product(range(screen_width), range(screen_height)):
        r, g, b = image[x + y*screen_width]
        setpixel(x,y,r, g, b)
    
    #Send buffer to display on the next VSync
    offscreen = myMatrix.SwapOnVSync(offscreen)
    
    #Display actual refresh rate of the display
    print ("Refresh rate : %d Hz" % 1/(time.time()-start))
