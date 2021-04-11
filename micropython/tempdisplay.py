from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf,sys, utime
import imgfile
import am2320
from temperaturebuffer import TemperatureBuffer

width  = 128 # SSD1306 horizontal resolution
height = 32   # SSD1306 vertical resolution

i2c_dev = I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)  # start I2C on I2C1 (GPIO 26/27)
i2c_addr = [hex(ii) for ii in i2c_dev.scan()] # get I2C address in hex format

sensor = am2320.AM2320(i2c_dev)

oled = SSD1306_I2C(width, height, i2c_dev) # oled controller

tempbuffer = TemperatureBuffer (width)

text_x = 0 # start point for text in x-dir
text_y = 0 # start point for text in y-dir
text_y_space = 13 # space between text in y-dir

max_temp = 30
min_temp = 0

graph_start_y = 22

# This value used by temp_to_yoffset - put outside of function so only need to calculate once
# Scale is temperature range divided by number pixels
scale =  (height -1 - graph_start_y) / (max_temp - min_temp)

while (1):
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    print("Temp: {}C RH {}%".format(temperature, humidity))
    # Check that the value is in a valid range (skip errornous readings)
    if (temperature > max_temp or humidity > 100) :
        print (" skipping erroroneous value")
        continue
    tempbuffer.addValue(temperature)

    oled.fill(0) # clear the OLED
    
    # Create text display
    text_1 = "Temp: {:.1f}C".format(sensor.temperature())
    text_2 = "RH: {:.1f}%".format(sensor.humidity())
    oled.text(text_1,text_x,text_y) # Show temperature
    oled.text(text_2,text_x,text_y+text_y_space) # Show Humidity

    # Create line graph across bottom of screen
    # Most recent value at right of screen (could reverse if preferred)
    x_pos = 0
    values = tempbuffer.getValues()
    for temp_value in values:
        # Convert temperature value into y position (high value = graph_start_y, low value = height of screen)
        y_pos = graph_start_y + int((max_temp - temp_value) * scale)
        # Draw a pixel for each value
        oled.pixel(x_pos, y_pos, 1)
        x_pos += 1

    oled.show() # output to OLED display
    
    utime.sleep(30)
