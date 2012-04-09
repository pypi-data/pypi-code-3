#
# THIS IS WORK IN PROGRESS
#
# The Python Imaging Library
# $Id$
#
# portable compiled font file parser
#
# history:
# 1997-08-19 fl   created
# 2003-09-13 fl   fixed loading of unicode fonts
#
# Copyright (c) 1997-2003 by Secret Labs AB.
# Copyright (c) 1997-2003 by Fredrik Lundh.
#
# See the README file for information on usage and redistribution.
#

import Image
import FontFile

import string

# --------------------------------------------------------------------
# declarations

PCF_MAGIC = 0x70636601 # "\x01fcp"

PCF_PROPERTIES = (1<<0)
PCF_ACCELERATORS = (1<<1)
PCF_METRICS = (1<<2)
PCF_BITMAPS = (1<<3)
PCF_INK_METRICS = (1<<4)
PCF_BDF_ENCODINGS = (1<<5)
PCF_SWIDTHS = (1<<6)
PCF_GLYPH_NAMES = (1<<7)
PCF_BDF_ACCELERATORS = (1<<8)

BYTES_PER_ROW = [
    lambda bits: ((bits+7)  >> 3),
    lambda bits: ((bits+15) >> 3) & ~1,
    lambda bits: ((bits+31) >> 3) & ~3,
    lambda bits: ((bits+63) >> 3) & ~7,
]


def l16(c):
    return ord(c[0]) + (ord(c[1])<<8)
def l32(c):
    return ord(c[0]) + (ord(c[1])<<8) + (ord(c[2])<<16) + (ord(c[3])<<24)

def b16(c):
    return ord(c[1]) + (ord(c[0])<<8)
def b32(c):
    return ord(c[3]) + (ord(c[2])<<8) + (ord(c[1])<<16) + (ord(c[0])<<24)

def sz(s, o):
    return s[o:string.index(s, "\0", o)]

##
# Font file plugin for the X11 PCF format.

class PcfFontFile(FontFile.FontFile):

    name = "name"

    def __init__(self, fp):

        magic = l32(fp.read(4))
        if magic != PCF_MAGIC:
            raise SyntaxError, "not a PCF file"

        FontFile.FontFile.__init__(self)

        count = l32(fp.read(4))
        self.toc = {}
        for i in range(count):
            type = l32(fp.read(4))
            self.toc[type] = l32(fp.read(4)), l32(fp.read(4)), l32(fp.read(4))

        self.fp = fp

        self.info = self._load_properties()

        metrics = self._load_metrics()
        bitmaps = self._load_bitmaps(metrics)
        encoding = self._load_encoding()

        #
        # create glyph structure

        for ch in range(256):
            ix = encoding[ch]
            if ix is not None:
                x, y, l, r, w, a, d, f = metrics[ix]
                glyph = (w, 0), (l, d-y, x+l, d), (0, 0, x, y), bitmaps[ix]
                self.glyph[ch] = glyph

    def _getformat(self, tag):

        format, size, offset = self.toc[tag]

        fp = self.fp
        fp.seek(offset)

        format = l32(fp.read(4))

        if format & 4:
            i16, i32 = b16, b32
        else:
            i16, i32 = l16, l32

        return fp, format, i16, i32

    def _load_properties(self):

        #
        # font properties

        properties = {}

        fp, format, i16, i32 = self._getformat(PCF_PROPERTIES)

        nprops = i32(fp.read(4))

        # read property description
        p = []
        for i in range(nprops):
            p.append((i32(fp.read(4)), ord(fp.read(1)), i32(fp.read(4))))
        if nprops & 3:
            fp.seek(4 - (nprops & 3), 1) # pad

        data = fp.read(i32(fp.read(4)))

        for k, s, v in p:
            k = sz(data, k)
            if s:
                v = sz(data, v)
            properties[k] = v

        return properties

    def _load_metrics(self):

        #
        # font metrics

        metrics = []

        fp, format, i16, i32 = self._getformat(PCF_METRICS)

        append = metrics.append

        if (format & 0xff00) == 0x100:

            # "compressed" metrics
            for i in range(i16(fp.read(2))):
                left = ord(fp.read(1)) - 128
                right = ord(fp.read(1)) - 128
                width = ord(fp.read(1)) - 128
                ascent = ord(fp.read(1)) - 128
                descent = ord(fp.read(1)) - 128
                xsize = right - left
                ysize = ascent + descent
                append(
                    (xsize, ysize, left, right, width,
                     ascent, descent, 0)
                    )

        else:

            # "jumbo" metrics
            for i in range(i32(fp.read(4))):
                left = i16(fp.read(2))
                right = i16(fp.read(2))
                width = i16(fp.read(2))
                ascent = i16(fp.read(2))
                descent = i16(fp.read(2))
                attributes = i16(fp.read(2))
                xsize = right - left
                ysize = ascent + descent
                append(
                    (xsize, ysize, left, right, width,
                     ascent, descent, attributes)
                    )

        return metrics

    def _load_bitmaps(self, metrics):

        #
        # bitmap data

        bitmaps = []

        fp, format, i16, i32 = self._getformat(PCF_BITMAPS)

        nbitmaps = i32(fp.read(4))

        if nbitmaps != len(metrics):
            raise IOError, "Wrong number of bitmaps"

        offsets = []
        for i in range(nbitmaps):
            offsets.append(i32(fp.read(4)))

        bitmapSizes = []
        for i in range(4):
            bitmapSizes.append(i32(fp.read(4)))

        byteorder = format & 4 # non-zero => MSB
        bitorder  = format & 8 # non-zero => MSB
        padindex  = format & 3

        bitmapsize = bitmapSizes[padindex]
        offsets.append(bitmapsize)

        data = fp.read(bitmapsize)

        pad  = BYTES_PER_ROW[padindex]
        mode = "1;R"
        if bitorder:
            mode = "1"

        for i in range(nbitmaps):
            x, y, l, r, w, a, d, f = metrics[i]
            b, e = offsets[i], offsets[i+1]
            bitmaps.append(
                Image.fromstring("1", (x, y), data[b:e], "raw", mode, pad(x))
                )

        return bitmaps

    def _load_encoding(self):

        # map character code to bitmap index
        encoding = [None] * 256

        fp, format, i16, i32 = self._getformat(PCF_BDF_ENCODINGS)

        firstCol, lastCol = i16(fp.read(2)), i16(fp.read(2))
        firstRow, lastRow = i16(fp.read(2)), i16(fp.read(2))

        default = i16(fp.read(2))

        nencoding = (lastCol - firstCol + 1) * (lastRow - firstRow + 1)

        for i in range(nencoding):
            encodingOffset = i16(fp.read(2))
            if encodingOffset != 0xFFFF:
                try:
                    encoding[i+firstCol] = encodingOffset
                except IndexError:
                    break # only load ISO-8859-1 glyphs

        return encoding
