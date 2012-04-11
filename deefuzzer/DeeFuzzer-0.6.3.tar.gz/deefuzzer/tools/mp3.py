#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright Guillaume Pellerin (2006-2009)

# <yomguy@parisson.com>

# This software is a computer program whose purpose is to stream audio
# and video data through icecast2 servers.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Author: Guillaume Pellerin <yomguy@parisson.com>

import os
import string
import datetime
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3, MPEGInfo
from mutagen import id3
from tools import *

EasyID3.valid_keys["comment"]="COMM::'XXX'"
EasyID3.valid_keys["copyright"]="TCOP::'XXX'"

class Mp3:
    """A MP3 file object"""

    def __init__(self, media):
        self.media = media
        self.item_id = ''
        self.source = self.media
        self.options = {}
        self.bitrate_default = '192'
        self.cache_dir = os.sep + 'tmp'
        self.keys2id3 = {'title': 'TIT2',
                    'artist': 'TPE1',
                    'album': 'TALB',
                    'date': 'TDRC',
                    'comment': 'COMM',
                    'genre': 'TCON',
                    'copyright': 'TCOP',
                    }
        self.mp3 = MP3(self.media, ID3=EasyID3)
        self.info = self.mp3.info
        self.bitrate = int(str(self.info.bitrate)[:-3])
        self.length = datetime.timedelta(0,self.info.length)
        try:
            self.metadata = self.get_file_metadata()
        except:
            self.metadata = {'title': '',
                    'artist': '',
                    'album': '',
                    'date': '',
                    'comment': '',
                    'genre': '',
                    'copyright': '',
                    }

        self.description = self.get_description()
        self.mime_type = self.get_mime_type()
        self.media_info = get_file_info(self.media)
        self.file_name = self.media_info[0]
        self.file_title = self.media_info[1]
        self.file_ext = self.media_info[2]
        self.extension = self.get_file_extension()
        self.size = os.path.getsize(media)
        #self.args = self.get_args()

    def get_format(self):
        return 'MP3'

    def get_file_extension(self):
        return 'mp3'

    def get_mime_type(self):
        return 'audio/mpeg'

    def get_description(self):
        return "MPEG audio Layer III"

    def get_file_metadata(self):
        metadata = {}
        for key in self.keys2id3.keys():
            try:
                metadata[key] = self.mp3[key][0]
            except:
                metadata[key] = ''
        return metadata

    def write_tags(self):
        """Write all ID3v2.4 tags by mapping dub2id3_dict dictionnary with the
            respect of mutagen classes and methods"""

        self.mp3.add_tags()
        self.mp3.tags['TIT2'] = id3.TIT2(encoding=2, text=u'text')
        self.mp3.save()

        #media_id3 = id3.ID3(self.media)
        #for tag in self.metadata.keys():
            #if tag in self.dub2id3_dict.keys():
                #frame_text = self.dub2id3_dict[tag]
                #value = self.metadata[tag]
                #frame = mutagen.id3.Frames[frame_text](3,value)
            #try:
                #media_id3.add(frame)
            #except:
                #raise IOError('ExporterError: cannot tag "'+tag+'"')

        #try:
            #media_id3.save()
        #except:
            #raise IOError('ExporterError: cannot write tags')

        media = id3.ID3(self.media)
        media.add(id3.TIT2(encoding=3, text=self.metadata['title'].decode('utf8')))
        media.add(id3.TP1(encoding=3, text=self.metadata['artist'].decode('utf8')))
        media.add(id3.TAL(encoding=3, text=self.metadata['album'].decode('utf8')))
        media.add(id3.TDRC(encoding=3, text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        media.add(id3.TCO(encoding=3, text=self.metadata['genre'].decode('utf8')))
        try:
            media.save()
        except:
            raise IOError('ExporterError: cannot write tags')


