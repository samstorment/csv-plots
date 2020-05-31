# some functions for manipulating colors in hex/rgb/rgba form

# a method generally used for inverting the text color of something based on its background color so the text contrasts well enough with the background
# params = hex color string in range #000000 to #ffffff, bool to indicate if you want to simply output black or white based on the given hex string color
def invert(hexStr, bw):

    # if a hex string is of length 1, add a 0 to the front of it
    # param = the hexstring for a hex rgb value (just 2 characters, or 1 if the leading 0 was automatically removed)
    def hexify(rgb):
        if len(rgb) == 1:
            return '0' + rgb
        else:
            return rgb

    # check if the first character has a # and remove it
    if (hexStr[0] == '#'):
        hexStr = hexStr[slice(1, len(hexStr))]

    # Convert the hex string to corresponding RGB ints
    r = int(hexStr[slice(0,2)], 16) # red is first 2 hex characters
    g = int(hexStr[slice(2,4)], 16) # green is next 2
    b = int(hexStr[slice(4,6)], 16) # blue is last 2

    # if you want to just get a black or white color
    if (bw):
        if ((r * 0.299 + g * 0.587 + b * 0.114) > 135): # > 186 was initial val
            return '#000000'
        else:
            return '#ffffff'

    # subtract the current rgb values from the max values to get inverted colors
    r = 255 - r
    g = 255 - g
    b = 255 - b

    # convert the decimal rgb values to hex strings. the hex conversion adds the characters '0x' to the front of the hex string
    # we remove those 2 extra characters with the slice, then hexify that value if the value needs a leading 0
    r = hex(r)
    r = hexify(r[slice(2, len(r))])
    g = hex(g)
    g = hexify(g[slice(2, len(g))])
    b = hex(b)
    b = hexify(b[slice(2, len(b))])

    # return the inverted color in hex string color format
    rgb = '#'+r+g+b
    return(rgb)

# converts a hex color string to the rgba format used by matplotlib
def toRGBA(hexStr):

    if (hexStr[0] == '#'):
        hexStr = hexStr[slice(1, len(hexStr))]

    # Convert the hex string to corresponding RGB ints
    r = int(hexStr[slice(0,2)], 16) # red is first 2 hex characters
    g = int(hexStr[slice(2,4)], 16) # green is next 2
    b = int(hexStr[slice(4,6)], 16) # blue is last 2

    # rather than a scale from 0 to 255, this rgba scale goes from 0 to one so we simply divide the current rgba vaues by the max value of 255
    return (r/255, g/255, b/255, 1)
