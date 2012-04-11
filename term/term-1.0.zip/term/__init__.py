"""The term module is intended to replace the tty module."""

# Authors: Steen Lumholt, Stefan H. Holek

import os
import re

from termios import *

__all__ = ["setraw", "setcbreak", "rawmode", "cbreakmode", "opentty", "getyx", "getmaxyx",
           "IFLAG", "OFLAG", "CFLAG", "LFLAG", "ISPEED", "OSPEED", "CC"]

# Indexes for termios list.
IFLAG = 0
OFLAG = 1
CFLAG = 2
LFLAG = 3
ISPEED = 4
OSPEED = 5
CC = 6


def setraw(fd, when=TCSAFLUSH, min=1, time=0):
    """Put the terminal in raw mode."""
    mode = tcgetattr(fd)
    mode[IFLAG] = mode[IFLAG] & ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON)
    mode[OFLAG] = mode[OFLAG] & ~(OPOST)
    mode[CFLAG] = mode[CFLAG] & ~(CSIZE | PARENB)
    mode[CFLAG] = mode[CFLAG] | CS8
    mode[LFLAG] = mode[LFLAG] & ~(ECHO | ICANON | IEXTEN | ISIG)
    mode[CC][VMIN] = min
    mode[CC][VTIME] = time
    tcsetattr(fd, when, mode)


def setcbreak(fd, when=TCSAFLUSH, min=1, time=0):
    """Put the terminal in cbreak mode."""
    mode = tcgetattr(fd)
    mode[LFLAG] = mode[LFLAG] & ~(ECHO | ICANON)
    mode[CC][VMIN] = min
    mode[CC][VTIME] = time
    tcsetattr(fd, when, mode)


class rawmode(object):
    """Context manager to put the terminal in raw mode."""

    def __init__(self, fd, when=TCSAFLUSH, min=1, time=0):
        self.fd = fd
        self.when = when
        self.min = min
        self.time = time

    def __enter__(self):
        self.savedmode = tcgetattr(self.fd)
        setraw(self.fd, self.when, self.min, self.time)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.savedmode)


class cbreakmode(object):
    """Context manager to put the terminal in cbreak mode."""

    def __init__(self, fd, when=TCSAFLUSH, min=1, time=0):
        self.fd = fd
        self.when = when
        self.min = min
        self.time = time

    def __enter__(self):
        self.savedmode = tcgetattr(self.fd)
        setcbreak(self.fd, self.when, self.min, self.time)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.savedmode)


class opentty(object):
    """Context manager returning an rw stream connected to /dev/tty.

    The stream is None if the device could not be opened.
    """
    device = '/dev/tty'

    def __init__(self, bufsize=1):
        self.bufsize = bufsize

    def __enter__(self):
        self.tty = None
        try:
            fd = os.open(self.device, os.O_RDWR | os.O_NOCTTY)
            self.tty = os.fdopen(fd, 'w+', self.bufsize)
        except EnvironmentError:
            pass
        return self.tty

    def __exit__(self, *ignored):
        if self.tty is not None:
            self.tty.close()


def _readyx(stream):
    """Read a CSI R formatted response from stream."""
    p = ''
    c = stream.read(1)
    while c:
        p += c
        if c == 'R':
            break
        c = stream.read(1)
    if p:
        m = re.search(r'\[(\d+);(\d+)R', p)
        if m is not None:
            return int(m.group(1), 10), int(m.group(2), 10)
    return 0, 0


def getyx():
    """Return the cursor position as 1-based (row, col) tuple.

    row and col are 0 if the terminal does not support DSR 6.
    """
    with opentty() as tty:
        row = col = 0
        if tty is not None:
            with cbreakmode(tty, min=0, time=1):
                tty.write('\033[6n')
                row, col = _readyx(tty)
        return row, col


def getmaxyx():
    """Return the terminal window dimensions as (maxrow, maxcol) tuple.

    maxrow and maxcol are 0 if the terminal does not support DSR 6.
    """
    with opentty() as tty:
        maxrow = maxcol = 0
        if tty is not None:
            with cbreakmode(tty, min=0, time=1):
                savedyx = getyx()
                tty.write('\033[10000;10000f\033[6n')
                maxrow, maxcol = _readyx(tty)
                tty.write('\033[%d;%df' % savedyx)
        return maxrow, maxcol

