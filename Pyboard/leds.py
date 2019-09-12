import time, machine
import chars

palette = {
  "r" : [255,0,0],
  "v" : [0,255,0],
  "b" : [0,0,255],
  "p" : [255,0,255],
  "w" : [255,255,255],
  "g" : [101,101,101],
  "c" : [0,128,255],
  "m" : [255,128,0],
  "d" : [0,255,128],
  "e" : [255,0,128],
  "f" : [128,0,255],
}

LED_BROADCAST = 1       # broadcast I2C address
LED_ADDR = 60           # default individual LED36 address

i2c = machine.I2C('Y')

def init(addr=1):
  i2c.writeto(addr, b'\x01')
  time.sleep_ms(16)

def cyc(addr, dt=250):
    """ Set all LEDs to black, red, green, yellow, blue, magenta, cayn and white for dt ms
        ramp up brightnes from 0 % to 100 %
    """
    while True:
        try:
            fill_rgb(addr, 100, 100, 100)
            break
        except:
            time.sleep_ms(100)
    for i in range(8):
        fill_rgb(addr, (i & 1) * 255, ((i >> 1) & 1) * 255, ((i >> 2) & 1) * 255)
        time.sleep_ms(dt)
    for i in range(100):
        brightness(addr, i)
        time.sleep_ms(20)

def brightness(addr, b=100):
    """ Set brigntness """
    ba = bytearray(b'\x02\x16 ')
    ba[-1] = b & 0xff
    i2c.writeto(addr, ba)

def bloop(addr, dt=100, maxv=100, inc=1):
    """ Cycle through brigntness ramp """
    b = 0
    while True:
        print(b)
        brightness(addr, b)
        b += inc
        b %= maxv
        time.sleep_ms(dt)

def pump(addr, dt=10, maxv=100):
    """ Cycle through brightness modulation """
    import math
    sinar = []
    for i in range(90):
        sinar.append(int((math.sin(i * 4 / 180 * math.pi) + 1) * maxv / 2))
    i = 0
    while True:
        brightness(addr, sinar[i])
        i += 1
        i %= len(sinar)
        time.sleep_ms(dt)

def fill_rgb(addr, r, g, b):
    """ Fill LED array using set pixel command """
    i2c.writeto(addr, b'\x02X\x00\x00')
    buf = bytearray(b'\x02A   ')
    buf[2] = r
    buf[3] = g
    buf[4] = b
    for i in range(36):
        i2c.writeto(addr, buf)

def illu(addr, r, g, b):
    """ Fill LED array using set illumination command """
    buf = bytearray(b'\x02i   ')
    buf[2] = r
    buf[3] = g
    buf[4] = b
    i2c.writeto(addr, buf)

def fill_frame(addr, r, g, b):
    """ Fill LED array using fill frame command """
    i2c.writeto(addr, b'\x02ml')
    buf = bytearray(b'   ')
    buf[0] = r
    buf[1] = g
    buf[2] = b
    for i in range(36):
        i2c.writeto(addr, buf)

def set_dot(addr, x, y, r, g, b, orientation=1):
    if orientation == -1:
        x = 5-x 
        y = 5-y 

    """ Set single LED color at position """
    buf = bytearray(b'\x02X  ')
    buf[2] = x
    buf[3] = y
    i2c.writeto(addr, buf)

    buf = bytearray(b'\x02A   ')
    buf[2] = r
    buf[3] = g
    buf[4] = b
    i2c.writeto(addr, buf)

def fill_raw(addr, r, g, b):
    """ Fill LED array with raw values using fill frame command """
    i2c.writeto(addr, b'\x02nl')
    buf = bytearray(b'   ')
    buf[0] = r
    buf[1] = g
    buf[2] = b
    for i in range(36):
        i2c.writeto(addr, buf)

def led_pins(addr, v):
    """ Permute LED colors (use with care) """
    buf = bytearray(b'\x02\x1c\x00')
    buf[-1] = v & 3
    i2c.writeto(addr, buf)

def random_dots(addr, dt=10):
    """ Set random colors at random positions """
    import pyb
    while True:
        rn = pyb.rng()
        r = rn & 0xff
        g = (rn >> 8) & 0xff
        b = (rn >> 16) & 0xff
        x = (rn >> 24) % 36
        y = x // 6
        x %= 6
        set_dot(addr, x, y, r, g, b)
        time.sleep_ms(dt)

def draw_char(addr, char):
    pixels = chars.get_char(char)
    for row, val in enumerate(pixels):
        for col, pixel in enumerate(val):
            if pixel == 0:
                set_dot(addr, row, col, 0, 0, 0)
            else:
                set_dot(addr, row, col, 255, 0, 255)

def display(addr, buffer, orientation, w, h, r=255, g=255, b=255, x=0, y=0):
    for row, val in enumerate(buffer):
        if row>=h:
            break
        for col, pixel in enumerate(val):
            if col>=w:
                break
            if pixel == 0:
                set_dot(addr, row+y, col+x, 0, 0, 0, orientation)
            elif pixel in palette:
                set_dot(addr, row+y, col+x, palette[pixel][0], palette[pixel][1], palette[pixel][2], orientation)
            else:
                set_dot(addr, row+y, col+x, r, g, b, orientation)

def loader(addr, value, orientation, color='w'):
    for i in range(6):
        if i>value:
            set_dot(addr, 5, i, 0, 0, 0, orientation)
        else:
            set_dot(addr, 5, i, int(palette[color][0]/4), int(palette[color][1]/4), int(palette[color][2]/4), orientation)

