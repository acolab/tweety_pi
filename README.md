# tweety_pi
Adaptation fo the work of hzeller https://github.com/hzeller/rpi-rgb-led-matrix.git/ to live tweet on an RGB panel from Adafruit

##Build Library
To build the library with the Adafruit pinout wiring you need to edit the `./matrix/lib/Makefile` and uncomment `DEFINES+=-DRGB_CLASSIC_PINOUT` and `DEFINES+=-DONLY_SINGLE_CHAIN`

##Pyhton Library
To build/install the Python library type :
```
make build-python
sudo make install-python
```
in the `./matrix` folder
