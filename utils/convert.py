#!/usr/bin/env python

"""
Solarized color handler

Bascially used to convert base colors
Could be also handy for other purpose

by Wang Lu
2011.04.21
"""

import sys

COLORSTRING="""
    base03    #002b36  8/4 brblack  234 #1c1c1c 15 -12 -12   0  43  54 193 100  21
    base02    #073642  0/4 black    235 #262626 20 -12 -12   7  54  66 192  90  26
    base01    #586e75 10/7 brgreen  240 #4e4e4e 45 -07 -07  88 110 117 194  25  46
    base00    #657b83 11/7 bryellow 241 #585858 50 -07 -07 101 123 131 195  23  51
    base0     #839496 12/6 brblue   244 #808080 60 -06 -03 131 148 150 186  13  59
    base1     #93a1a1 14/4 brcyan   245 #8a8a8a 65 -05 -02 147 161 161 180   9  63
    base2     #eee8d5  7/7 white    254 #d7d7af 92 -00  10 238 232 213  44  11  93
    base3     #fdf6e3 15/7 brwhite  230 #ffffd7 97  00  10 253 246 227  44  10  99
    yellow    #b58900  3/3 yellow   136 #af8700 60  10  65 181 137   0  45 100  71
    orange    #cb4b16  9/3 brred    166 #d75f00 50  50  55 203  75  22  18  89  80
    red       #dc322f  1/1 red      160 #d70000 50  65  45 220  50  47   1  79  86
    magenta   #d33682  5/5 magenta  125 #af005f 50  65 -05 211  54 130 331  74  83
    violet    #6c71c4 13/5 brmagenta 61 #5f5faf 50  15 -45 108 113 196 237  45  77
    blue      #268bd2  4/4 blue      33 #0087ff 55 -10 -45  38 139 210 205  82  82
    cyan      #2aa198  6/6 cyan      37 #00afaf 60 -35 -05  42 161 152 175  74  63
    green     #859900  2/2 green     64 #5f8700 60 -20  65 133 153   0  68 100  60
"""

COLORSTRING_LINES = []

COLORMAP={}

class ColorObj():
    def __init__ (self, colorstr):
        l = colorstr.split()
        self.name = l[0]
        self.hexstr = l[1]
        (self.value16, self.value8) = map(int, l[2].split('/'))
        self.termname = l[3]
        self.value256 = l[4]
        self.hex256 = l[5]
        self.labvalue = map(int, (l[6],l[7],l[8]))
        self.rgbvalue = map(int, (l[9],l[10],l[11]))
        self.hsbvalue = map(int, (l[12],l[13],l[14]))
        self.term256value = (int(self.hex256[1:3],16), int(self.hex256[3:5],16), int(self.hex256[5:7],16))
        # verify
        assert self.hexstr == '#%02x%02x%02x' % tuple(self.rgbvalue)

def parse_colorstring():
    lines = COLORSTRING.split('\n')
    for l in lines:
        l = l.strip()
        if l == '':
            continue
        COLORSTRING_LINES.append(l)
        c = ColorObj(l)
        COLORMAP[c.name] = c


def format_8rgb_hex(v):
    return '%02x%02x%02x' % tuple(v)

def format_8rgb_Hex(v):
    return '%02X%02X%02X' % tuple(v)

def format_16rgb_hex(v):
    return '%02x%02x%02x%02x%02x%02x' % (v[0],v[0],v[1],v[1],v[2],v[2])

def format_16rgb_Hex(v):
    return '%02X%02X%02X%02X%02X%02X' % (v[0],v[0],v[1],v[1],v[2],v[2])


FORMATTER_LIST = [format_8rgb_hex, format_8rgb_Hex, format_16rgb_hex, format_16rgb_Hex]

def convert_basecolors_to_term256(fn):
    for l in open(fn).readlines():
        if l[-1] == '\n':
            l = l[:-1] # remove the trailing newline

        # avoid converting the color def
        is_color_def = False
        for colorline in COLORSTRING_LINES:
            if l.find(colorline) != -1:
                is_color_def = True
                break
        if is_color_def:
            print l
            continue

        for cn in COLORMAP.keys():
            if cn.startswith('base'):
                cobj = COLORMAP[cn]
                for f in FORMATTER_LIST:
                    l = l.replace(f(cobj.rgbvalue), f(cobj.term256value))
        print l

if __name__ == '__main__':
    parse_colorstring()
    convert_basecolors_to_term256(sys.argv[1])



