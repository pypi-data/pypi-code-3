# -*- coding: utf-8 -*-
"""
Listing of constants that will be used throughout the program
"""

from __future__ import unicode_literals, absolute_import

import re

import os
import sys
from os.path import join, split, realpath

VIDEO_EXTENSIONS = set(['.mkv', '.ogm', '.asf', '.asx', '.avi', '.flv',
                        '.mov', '.mp4', '.mpg', '.rm', '.swf', '.vob',
                        '.wmv', '.mpeg'])

PROJECT_SOURCE_PATH = split(realpath(__file__))[0]
PROJECT_PATH = split(PROJECT_SOURCE_PATH)[0]
WEB_SOURCES_PATH = join(PROJECT_SOURCE_PATH, 'web_sources')

RESOURCE_PATH = os.path.join("eplist", "resources")

if sys.platform == "win32":
    RESOURCE_PATH = os.path.join(os.environ['APPDATA'], RESOURCE_PATH)
else:  # *nix / solaris
    RESOURCE_PATH = os.path.join("~", ".{}".format(RESOURCE_PATH))
    RESOURCE_PATH = os.path.expanduser(RESOURCE_PATH)


SHOW_NOT_FOUND = []

regexList = []

NUM_DICT = {'0': '', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
        '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen',
        '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', '17': 'seventeen',
        '18': 'eighteen', '19': 'nineteen', '20': 'twenty', '30': 'thirty',
        '40': 'forty', '50': 'fifty', '60': 'sixty', '70': 'seventy',
        '80': 'eighty', '90': 'ninety'}


# If you wish to use braces for matching ranges like {1,10} you need to escape
# the braces by doubling them to prevent pythons formatting from breaking.
# eg: {1,10} becomes {{1, 10}}
types = ['ova', 'ona', 'extra', 'special', 'movie', 'dvd', 'bluray']
types = r'|'.join(types)

regex_vars = {
'sep': r'[\-\~\.\_\s]',
'sum': r'.*[\[\(](?P<sum>[a-z0-9]{{8}}[\]\)])',
'year': r'(:P<year>(19|20)?\d\d)',
'episode': r'(e|ep|episode)?{sep}*?(?P<episode>\d+)(?:v\d)?',  # ex: e3v2
'season': r'(s|season)?{sep}*?(?P<season>\d+)',
'series': r'(?P<series>.*)',
'subgroup': r'(?P<group>\[.*\])',
'special': r'(?P<type>{specical_types}){sep}+(?P<special>\d+)',
'specical_types': types,
}

# Substitute any regex variables that may have been used within later dictionary entries
regex_vars = {r: regex_vars[r].format(**regex_vars) for r in regex_vars}

regexList = [
    r'^(?P<series>.*?) - Season (?P<season>\d+) - Episode (?P<episode>\d*) - .*',
    r'^(?P<series>.*?) - Episode (?P<episode>\d*) - .*',  # My usual format
    r'^{series}{sep}+{special}',
    r'^{series}{sep}+{episode}',
    r'^{series}{sep}+{season}{sep}*{episode}',
    r'^{series}{sep}+{season}{sep}*{episode}{sep}*{sum}?',
    r'^{series}{sep}+{episode}',
    r'^(?P<series>.*) - OVA (?P<special>\d+) - \w*',
    r'^{series}{sep}*{special}',
    r'{series}{sep}*(op|ed){sep}*(?P<junk>\d*)',  # Show intro /outro music
    r'{episode}',  # More of a general catch-all regex
            ]

## Substitute the dictionary variables in to the unformatted regex
regexList = [r.format(**regex_vars) for r in regexList]
regexList = [re.compile(regex) for regex in regexList]

checksum_regex = re.compile(r'[\[\(](?P<sum>[a-f0-9]{8})[\]\)]', re.I)
remove_junk_regex = re.compile(r'[\[\(].*?[\]\]]', re.I)
bracket_season_regex = re.compile(r'[\[\(]{season}X{episode}[\]\)]'.format(**regex_vars), re.I)
