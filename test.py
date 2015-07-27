#!/usr/bin/env python
from rgbmatrix import RGBMatrix
import time
import itertools

rows = 16
chains = 3
parallel = 1
myMatrix = RGBMatrix(rows, chains, parallel)
myMatrix.pwmBits = 1
myMatrix.luminanceCorrect = False
offscreen = myMatrix.CreateFrameCanvas()
for i in xrange(3):
    for x,y in itertools.product(range(offscreen.width), range(offscreen.height)):
        offscreen.SetPixel(x,y,255, 0, 0)
        start = time.time()
    offscreen = myMatrix.SwapOnVSync(offscreen)
    stop = time.time()
    print stop-start
    time.sleep(1)
    myMatrix.Clear()
    time.sleep(1)
