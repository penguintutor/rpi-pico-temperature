import tempdisplay
from machine import Pin
import utime

# Add short delay when starting from boot to allow
# I2C devices to settle
utime.sleep(1)
tempdisplay.main()
