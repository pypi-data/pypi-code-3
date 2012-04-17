#
# Jasy - Web Tooling Framework
# Copyright 2010-2012 Zynga Inc.
#

import struct, logging

"""
Contains image format detection classes. Once the format is detect it supports image size detection, too.
"""

class ImgFile(object):
    def __init__(self, filename):
        try:
            self.fp = open(filename, "rb")
        except IOError as err:
            logging.error("Could not open file: %s" % filename)
            raise err

    def verify(self):
        raise NotImplementedError("%s: %s" % (self.__class__, "verify()"))

    def type(self):
        raise NotImplementedError("%s: %s" % (self.__class__, "type()"))

    def size(self):
        raise NotImplementedError("%s: %s" % (self.__class__, "size()"))

    def close(self):
        self.fp.close()

    def __del__(self):
        self.close()


# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
class GifFile(ImgFile):
    def verify(self):
        self.fp.seek(0)
        header = self.fp.read(6)
        signature = struct.unpack("3s3s", header[:6])
        isGif = signature[0] == b"GIF" and signature[1] in [b"87a", b"89a"]
        return isGif

    def type(self):
        return "gif"

    def size(self):
        self.fp.seek(0)
        header = self.fp.read(6+6)
        (width, height) = struct.unpack("<HH", header[6:10])
        return width, height


# http://www.libmng.com/pub/png/spec/1.2/png-1.2-pdg.html#Structure
class PngFile(ImgFile):
    def __init__(self, filename):
        ImgFile.__init__(self, filename)

    def type(self):
        return "png"

    def verify(self):
        self.fp.seek(0)
        header = self.fp.read(8)
        signature = struct.pack("8B", 137, 80, 78, 71, 13, 10, 26, 10)
        isPng = header[:8] == signature
        return isPng

    def size(self):
        self.fp.seek(0)
        header = self.fp.read(8+4+4+13+4)
        ihdr = struct.unpack("!I4s", header[8:16])
        data = struct.unpack("!II5B", header[16:29])
        (width, height, bitDepth, colorType, compressionMethod, filterMethod, interleaceMethod) = data
        return (width, height)


# http://www.obrador.com/essentialjpeg/HeaderInfo.htm
class JpegFile(ImgFile):
    def verify(self):
        self.fp.seek(0)
        signature = struct.unpack("!H", self.fp.read(2))
        isJpeg = signature[0] == 0xFFD8
        return isJpeg

    def type(self):
        return "jpeg"

    def size(self):
        self.fp.seek(2)
        
        # find FFC0 marker
        cont = self.fp.read()

        # try Baseline DCT Start-of-frame marker (SOF0) (http://en.wikipedia.org/wiki/Jpeg)
        pos  = cont.find(b"\xFF\xC0")
        if pos < 0:
            # try Progressive DCT Start-of-frame marker (SOF2)
            pos  = cont.find(b"\xFF\xC2")
        if pos < 0:  # no SOF found - give up
            return None
        pos += 4 # skip marker and length
        
        # extract values from SOF payload
        try:
            (precision, height, width) = struct.unpack("!BHH", cont[pos:pos+5])
        except struct.error:
            return None
        return (width, height)


class ImgInfo(object):
    def __init__(self, filename):
        self.__filename = filename

    classes = [PngFile, GifFile, JpegFile]

    def getSize(self):
        """
        Returns the image sizes of png, gif and jpeg files as
        (width, height) tuple
        """
        
        filename = self.__filename
        classes = self.classes

        for cls in classes:
            img = cls(filename)
            if img.verify():
                size = img.size()
                if size is not None:
                    img.close()
                    return size
            img.close()

        return None
    
    def getInfo(self):
        ''' Returns (width, height, "type") of the image'''
        filename = self.__filename
        classes = self.classes
        
        for cls in classes:
            img = cls(filename)
            if img.verify():
                return img.size()

        return None