#!/usr/bin/env python
from rgbmatrix import RGBMatrix
import time
import itertools
import random

rows = 16
chains = 3
parallel = 1
myMatrix = RGBMatrix(rows, chains, parallel)
myMatrix.pwmBits = 1
myMatrix.luminanceCorrect = False
offscreen = myMatrix.CreateFrameCanvas()
for i in xrange(10):
    image = [(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)) for i in xrange(myMatrix.width*myMatrix.height)]
    screen_width = offscreen.width
    screen_height = offscreen.height
    setpixel = offscreen.SetPixel
    start = time.time()
    #[r,g,b = image[x + y*screen_width] ; setpixel(x,y,r,g,b) for x,y in itertools.product(range(screen_width), range(screen_height))]
    for x,y in itertools.product(range(screen_width), range(screen_height)):
        r, g, b = image[x + y*screen_width]
        setpixel(x,y,r, g, b)
    print 1/(time.time()-start)
    offscreen = myMatrix.SwapOnVSync(offscreen)
