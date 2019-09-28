# hex (string) to rgb (tuple3)
def hex2rgb(hex):
    hex_cleaned = hex.lstrip('#')
    return tuple(int(hex_cleaned[i:i+2], 16) for i in (0, 2 ,4))

# rgb (tuple3) to hex (string)
def rgb2hex(rgb):
    return '#' + ''.join([str('0' + hex(hh)[2:])[-2:] for hh in rgb])

# weighted mix of two colors in RGB space (takes and returns hex values)
def mix(hex1, hex2, wt1=0.5):
    rgb1 = hex2rgb(hex1)
    rgb2 = hex2rgb(hex2)
    return rgb2hex(tuple([int(wt1 * tup[0] + (1.0 - wt1) * tup[1]) for tup in zip(rgb1, rgb2)]))

