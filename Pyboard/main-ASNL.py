import urequests
import time, machine
import leds
import chars
from pyb import Switch

sleep       = 100   # resolution of 100ms, must be a pdc of all values below
scroll      = 100   # every 100ms
loader      = 100000 # every 100s so every refresh 6x100s=10mn
orientation = -1    # 1 for USB cable on bottom, -1 for USB cable on top

color = 'w'
timer = 0
load  = 0
sw    = Switch()
text  = []

leds.init()
leds.fill_raw(leds.LED_ADDR,0,0,0);
leds.display(leds.LED_ADDR,chars.get_text_buffer('؞'),orientation,chars.PIXEL_SIZE,chars.PIXEL_SIZE)

while True:
    if sw.value() == True:
        print('[Restart]')
        leds.fill_raw(leds.LED_ADDR,0,0,0);
        load  = 0
        timer = 0

    if timer%loader==0:
        if load==0:
            response = None
            try:
                response = urequests.get('http://149.202.45.91/pyboard-apps/ASNL.php')
                parsed = response.json()
                print('[Load] Server:',parsed)
                if "rank" in parsed:
                    if parsed['win']:
                        color = 'v'
                    elif parsed['lose']:
                        color = 'r'
                    else:
                        color = 'w'
                    display = 'p>w ' + parsed['rank'].upper() + ' p>' + color + ' ' + parsed['result'].upper() + ' p>g ' + parsed['team'].upper() + ' '
                    text = chars.get_text_buffer(display)
                    print('[Load] Display:', display)
                else:
                    print('[Load] Bad response:', response.status_code, response.reason)
            except Exception as e:
                if response:
                    # server error
                    text = chars.get_text_buffer('r?g' + str(response.status_code) + 'w¿')
                    timer = 1000000-5*6*scroll # Retry in 5 scrolled chars
                else:
                    # no wifi
                    text = chars.get_text_buffer('f؞m؞c؞d؞')
                    timer = 1000000-4*6*scroll # Retry in 2 scrolled chars

                print('[Load] Error:', str(e))
                load = -1 # Retry on next tick

        leds.loader(leds.LED_ADDR, load, orientation, color)
        load = (load+1)%6

    if timer % scroll == 0:
        try:
            if text:
                leds.display(leds.LED_ADDR,text,orientation,6,chars.PIXEL_SIZE)
                chars.scroll_left(text)
        except Exception as e:
            print('[Scroll]', str(e))
    
    time.sleep_ms(sleep)
    timer = 0 if (timer>=1000000) else timer + sleep
