# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         scala.py
# Purpose:      reading and translation of the Scala scale format
#
# Authors:      Christopher Ariza
#
# Copyright:    (c) 2011 The music21 Project
# License:      LGPL
#-------------------------------------------------------------------------------
'''
This module defines classes for representing Scala scale data, including Scala pitch representations, storage, and files. 

The Scala format is defined at the following URL:
http://www.huygens-fokker.org/scala/scl_format.html
We thank Manuel Op de Coul for allowing us to include the repository (as of May 11, 2011) with music21

Utility functions are also provided to search and find scales in the Scala scale archive. File names can be found with the :func:`~music21.scala.search` function.

To create a :class:`~music21.scale.ScalaScale` instance, simply provide a root pitch and the name of the scale. Scale names are given as a the scala .scl file name. 

>>> from music21 import *
>>> mbiraScales = scala.search('mbira')
>>> mbiraScales
['mbira_banda.scl', 'mbira_banda2.scl', 'mbira_gondo.scl', 'mbira_kunaka.scl', 'mbira_kunaka2.scl', 'mbira_mude.scl', 'mbira_mujuru.scl', 'mbira_zimb.scl']


For most people you'll want to do something like this:

>>> sc = scale.ScalaScale('a4', 'mbira_banda.scl')
>>> sc.pitches
[A4, B4(-15c), C#5(-11c), D#5(-7c), E~5(+6c), F#5(+14c), G~5(+1c), B-5(+2c)]

'''

import os
import unittest, doctest
import math, codecs
try:
    import StringIO # python 2 
except:
    from io import StringIO # python3 (also in python 2.6+)



import music21 

from music21 import common
from music21 import interval
# scl is the library of scala files
from music21.scala import scl

from music21 import environment
_MOD = "pitch.py"
environLocal = environment.Environment(_MOD)




#-------------------------------------------------------------------------------
def getPaths():    
    '''Get all scala scale paths. This is called once or the module and cached as SCALA_PATHS, which should be used instead of calls to this function. 

    >>> from music21 import scala
    >>> a = scala.getPaths()
    >>> len(a) >= 3800
    True
    '''
    moduleName = scl
    if not hasattr(moduleName, '__path__'):
        # when importing a package name (a directory) the moduleName        
        # may be a list of all paths contained within the package
        # this seems to be dependent on the context of the call:
        # from the command line is different than from the interpreter
        dirListing = moduleName
    else:
        # returns a list with one or more paths
        # the first is the path to the directory that contains xml files
        dir = moduleName.__path__[0] 
        dirListing = [os.path.join(dir, x) for x in os.listdir(dir)]

    paths = {} # return a dictionary with keys and list of alternate names
    for fp in dirListing:
        if fp.endswith('.scl'):
            paths[fp] = []
            # store alternative name representations
            # store version with no extension
            dir, fn = os.path.split(fp)
            fn = fn.replace('.scl', '')
            paths[fp].append(fn)
            # store version with removed underscores
            dir, fn = os.path.split(fp)
            fn = fn.lower()
            fn = fn.replace('.scl', '')
            fn = fn.replace('_', '')
            fn = fn.replace('-', '')
            paths[fp].append(fn)

    return paths


SCALA_PATHS = getPaths()


#-------------------------------------------------------------------------------



class ScalaPitch(object):
    '''Representation of a scala pitch notation

    >>> from music21 import *
    >>> sp = scala.ScalaPitch(' 1066.667 cents')
    >>> print sp.parse()
    1066.667

    >>> sp = scala.ScalaPitch(' 2/1')
    >>> sp.parse()
    1200.0
    >>> sp.parse('100.0 C#')
    100.0
    >>> [sp.parse(x) for x in ['89/84', '55/49', '44/37', '63/50', '4/3', '99/70', '442/295', '27/17', '37/22', '98/55', '15/8', '2/1']]
    [100.09920982..., 199.9798432913..., 299.973903610..., 400.108480470..., 498.044999134..., 600.08832376157..., 699.9976981706..., 800.90959309..., 900.02609638..., 1000.020156708..., 1088.268714730..., 1200.0]
    '''

    # pitch values; if has a period, is cents, otherwise a ratio
    # above the implied base ratio
    # integer values w/ no period or slash: 2 is 2/1

    def __init__(self, sourceString=None):

        self.src = None
        if sourceString is not None:
            self._setSrc(sourceString)

        # resole all values into cents shifts
        self.cents = None

    def _setSrc(self, raw):
        raw = raw.strip()
        # get decimals and fractions
        raw, junk = common.getNumFromStr(raw, numbers='0123456789./')
        self.src = raw.strip()

    def parse(self, sourceString=None):
        '''Parse the source string and set self.cents.
        '''
        if sourceString is not None:
            self._setSrc(sourceString)

        if '.' in self.src: # cents
            self.cents = float(self.src)
        else: # its a ratio
            if '/' in self.src:
                n, d = self.src.split('/')
                n, d = float(n), float(d)
            else:
                n = float(self.src)
                d = 1.0
            # http://www.sengpielaudio.com/calculator-centsratio.htm
            self.cents = 1200.0 * math.log((n / d), 2)
        return self.cents




class ScalaStorage(object):
    '''Object representation of data stored in a Scale scale file. This objeject is used to access Scala information stored in a file. To create a music21 scale with a Scala file, use :class:`~music21.scale.ScalaScale`.

    This is not called ScalaScale, as this name clashes with the :class:`~music21.scale.ScalaScale` that uses this object.
    '''
    def __init__(self, sourceString=None, fileName=None):
        self.src = sourceString
        self.fileName = fileName # store source file anme

        # added in parsing:
        self.description = None
        
        # lower limit is 0, as degree 0, or the 1/1 ratio, is implied
        # assumes octave equivalence?
        self.pitchCount = None # number of lines w/ pitch values will follow        
        self.pitchValues = []

    def parse(self):
        '''Parse a scala file delivered as a long string with line breaks
        '''
        lines = self.src.split('\n')
        count = 0 # count non-comment lines
        for i, l in enumerate(lines):
            l = l.strip()
            #environLocal.printDebug(['l', l, self.fileName, i])
            if l.startswith('!'):
                if i == 0 and self.fileName is None: # try to get from first l      
                    if '.scl' in l: # its got the file name 
                        self.fileName = l[1:].strip() # remove leading !
                continue # comment
            else:
                count += 1
            if count == 1: # 
                if l != '': # may be empty
                    self.description = l
            elif count == 2:
                if l != '':
                    self.pitchCount = int(l)
            else: # remaining counts are pitches
                if l != '':
                    sp = ScalaPitch(l)
                    sp.parse()
                    self.pitchValues.append(sp)
  
    def getCentsAboveTonic(self):
        '''Return a list of cent values above the implied tonic.
        '''
        return [sp.cents for sp in self.pitchValues]    
    

    def getAdjacentCents(self):
        '''Get cents values between adjacent intervals.
        '''
        post = []
        location = 0
        for c in self.getCentsAboveTonic():
            dif = c - location
            #environLocal.printDebug(['getAdjacentCents', 'c', c, 'location', location, 'dif', dif])
            post.append(dif)
            location = c # set new location
        return post

    def setAdjacentCents(self, centList):
        '''Given a list of adjacent cent values, create the necessary ScalaPitch  objects and update the 
        '''
        self.pitchValues = []
        location = 0
        for c in centList:
            sp = ScalaPitch()
            sp.cents = location + c
            location = sp.cents
            self.pitchValues.append(sp)
        self.pitchCount = len(self.pitchValues)


    def getIntervalSequence(self):
        '''Get the scale as a list of Interval objects.
        '''
        post = []
        for c in self.getAdjacentCents():
            # convert cent values to semitone values to create intervals
            post.append(interval.Interval(c*.01))
        return post

    def setIntervalSequence(self, iList):
        '''Set the scale from a list of Interval objects.
        '''
        self.pitchValues = []
        location = 0
        for i in iList:
            # convert cent values to semitone values to create intervals
            sp = ScalaPitch()
            sp.cents = location + i.cents
            location = sp.cents
            self.pitchValues.append(sp)
        self.pitchCount = len(self.pitchValues)

    def getFileString(self):
        '''Return a string suitable for writing a Scale file
        '''
        msg = []
        if self.fileName is not None:
            msg.append('! %s' % self.fileName)
        # conventional to add a comment space
        msg.append('!')

        if self.description is not None:
            msg.append(self.description)
        else: # must supply empty line
            msg.append('')

        if self.pitchCount is not None:
            msg.append(str(self.pitchCount))
        else: # must supply empty line
            msg.append('')
    
        # conventional to add a comment space
        msg.append('!')
        for sp in self.pitchValues:
            msg.append(str(sp.cents))
        # add space
        msg.append('') 

        return '\n'.join(msg)


#-------------------------------------------------------------------------------
class ScalaFile(object):
    '''
    Interface for reading and writing scala files. On reading, returns a :class:`~music21.scala.ScalaStorage` object.

    >>> from music21 import *
    >>> sf = scala.ScalaFile() 
    '''
    
    def __init__(self, data=None): 
        self.fileName = None
        self.file = None
        # store data source if provided
        self.data = data

    def open(self, fp, mode='r'): 
        '''Open a file for reading
        '''
        self.file = codecs.open(fp, mode, encoding='utf-8')
        self.fileName = os.path.basename(fp)

    def openFileLike(self, fileLike):
        '''Assign a file-like object, such as those provided by StringIO, as an open file object.
        '''
        self.file = fileLike # already 'open'
    
    def __repr__(self): 
        r = "<ScalaFile>" 
        return r 
    
    def close(self): 
        self.file.close() 
    
    def read(self): 
        '''Read a file. Note that this calls readstring, which processes all tokens. 

        If `number` is given, a work number will be extracted if possible. 
        '''
        return self.readstr(self.file.read()) 

    def readstr(self, strSrc): 
        '''Read a string and process all Tokens. Returns a ABCHandler instance.
        '''
        ss = ScalaStorage(strSrc, self.fileName)
        ss.parse()
        self.data = ss
        return ss

    def write(self): 
        ws = self.writestr()
        self.file.write(ws) 
    
    def writestr(self): 
        if isinstance(self.data, ScalaStorage):
            return self.data.getFileString()
        # handle Scale or other objects
        

#-------------------------------------------------------------------------------
def parse(target):
    '''Get a :class:`~music21.scala.ScalaStorage` object from the bundled SCL archive or a file path. 

    >>> from music21 import scala
    >>> ss = scala.parse('balafon6')
    >>> ss.description
    u'Observed balafon tuning from Burma, Helmholtz/Ellis p. 518, nr.84'
    >>> [str(i) for i in ss.getIntervalSequence()]
    ['<music21.interval.Interval m2 (+14c)>', '<music21.interval.Interval M2 (+36c)>', '<music21.interval.Interval M2>', '<music21.interval.Interval m2 (+37c)>', '<music21.interval.Interval M2 (-49c)>', '<music21.interval.Interval M2 (-6c)>', '<music21.interval.Interval M2 (-36c)>']


    >>> scala.parse('incorrectFileName.scl') == None
    True


    >>> ss = scala.parse('barbourChrom1')
    >>> ss.description
    u"Barbour's #1 Chromatic"
    >>> ss.fileName
    'barbour_chrom1.scl'


    >>> ss = scala.parse('blackj_gws.scl')
    >>> ss.description
    u'Detempered Blackjack in 1/4 kleismic marvel tuning'
    '''
    match = None
    # this may be a file path to a scala file
    if os.path.exists(target) and target.endswith('.scl'):
        match = target

    # try from stored collections
    # remove any spaces
    target = target.replace(' ', '')
    if match is None:
        for fp in SCALA_PATHS.keys():
            dir, fn = os.path.split(fp)
            # try exact match
            if target.lower() == fn.lower():
                match = fp
                break

    # try again, from cached reduced expressions
    if match is None:        
        for fp in SCALA_PATHS.keys():
            # look at alternative names
            for alt in SCALA_PATHS[fp]:
                if target.lower() == alt:
                    match = fp
                    break
    if match is None:
        # accept partial matches
        for fp in SCALA_PATHS.keys():
            # look at alternative names
            for alt in SCALA_PATHS[fp]:
                if target.lower() in alt:
                    match = fp
                    break

    # might put this in a try block
    if match is not None:
        sf = ScalaFile()
        sf.open(match)
        ss = sf.read()
        sf.close()
        return ss


def search(target):
    '''Search the scala archive for matches based on a string

    >>> from music21 import *
    >>> mbiraScales = scala.search('mbira')
    >>> mbiraScales
    ['mbira_banda.scl', 'mbira_banda2.scl', 'mbira_gondo.scl', 'mbira_kunaka.scl', 'mbira_kunaka2.scl', 'mbira_mude.scl', 'mbira_mujuru.scl', 'mbira_zimb.scl']
    '''
    match = []
    # try from stored collections
    # remove any spaces
    target = target.replace(' ', '')
    for fp in SCALA_PATHS.keys():
        dir, fn = os.path.split(fp)
        # try exact match
        if target.lower() == fn.lower():
            if fp not in match:
                match.append(fp)

    # accept partial matches
    for fp in SCALA_PATHS.keys():
        # look at alternative names
        for alt in SCALA_PATHS[fp]:
            if target.lower() in alt:
                if fp not in match:
                    match.append(fp)
    names = []
    for fp in match:
        names.append(os.path.basename(fp))
    names.sort()
    return names



#-------------------------------------------------------------------------------
class TestExternal(unittest.TestCase):
    
    def runTest(self):
        pass
    
    def testSingle(self):
        a = Pitch()
        a.name = 'c#'
        a.show()



class Test(unittest.TestCase):
    
    def runTest(self):
        pass

    def testScalaScaleA(self):
        msg = '''! slendro5_2.scl
!
A slendro type pentatonic which is based on intervals of 7, no. 2               
 5
!
 7/6
 4/3
 3/2
 7/4
 2/1
'''
        ss = ScalaStorage(msg)
        ss.parse()
        self.assertEqual(ss.pitchCount, 5)
        self.assertEqual(ss.fileName, 'slendro5_2.scl')
        self.assertEqual(len(ss.pitchValues), 5)
        self.assertEqual([str(x.cents) for x in ss.pitchValues], ['266.870905604', '498.044999135', '701.955000865', '968.825906469', '1200.0'])

        self.assertEqual([str(x) for x in ss.getCentsAboveTonic()], ['266.870905604', '498.044999135', '701.955000865', '968.825906469', '1200.0'])
        # sent values between scale degrees
        self.assertEqual([str(x) for x in ss.getAdjacentCents()], ['266.870905604', '231.174093531', '203.910001731', '266.870905604', '231.174093531'] )

        self.assertEqual([str(x) for x in ss.getIntervalSequence()], ['<music21.interval.Interval m3 (-33c)>', '<music21.interval.Interval M2 (+31c)>', '<music21.interval.Interval M2 (+4c)>', '<music21.interval.Interval m3 (-33c)>', '<music21.interval.Interval M2 (+31c)>'])

    def testScalaScaleB(self):
        msg = '''! fj-12tet.scl
!  
Franck Jedrzejewski continued fractions approx. of 12-tet 
 12
!  
89/84
55/49
44/37
63/50
4/3
99/70
442/295
27/17
37/22
98/55
15/8
2/1

'''
        ss = ScalaStorage(msg)
        ss.parse()
        self.assertEqual(ss.pitchCount, 12)
        self.assertEqual(ss.fileName, 'fj-12tet.scl')
        self.assertEqual(ss.description, 'Franck Jedrzejewski continued fractions approx. of 12-tet')

        self.assertEqual([str(x) for x in ss.getCentsAboveTonic()], ['100.099209825', '199.979843291', '299.97390361', '400.10848047', '498.044999135', '600.088323762', '699.997698171', '800.909593096', '900.02609639', '1000.02015671', '1088.26871473', '1200.0'])

        self.assertEqual([str(x) for x in ss.getAdjacentCents()], ['100.099209825', '99.8806334662', '99.9940603187', '100.13457686', '97.9365186644', '102.043324627', '99.9093744091', '100.911894925', '99.1165032942', '99.9940603187', '88.2485580216', '111.73128527'])

        self.assertEqual([str(x) for x in ss.getIntervalSequence()], ['<music21.interval.Interval m2 (+0c)>', '<music21.interval.Interval m2 (0c)>', '<music21.interval.Interval m2 (0c)>', '<music21.interval.Interval m2 (+0c)>', '<music21.interval.Interval m2 (-2c)>', '<music21.interval.Interval m2 (+2c)>', '<music21.interval.Interval m2 (0c)>', '<music21.interval.Interval m2 (+1c)>', '<music21.interval.Interval m2 (-1c)>', '<music21.interval.Interval m2 (0c)>', '<music21.interval.Interval m2 (-12c)>', '<music21.interval.Interval m2 (+12c)>'])


        # test loading a new scala object from adjacent sets
        ss2 = ScalaStorage()
        ss2.setAdjacentCents(ss.getAdjacentCents())
        
        self.assertEqual([str(x) for x in ss2.getCentsAboveTonic()], ['100.099209825', '199.979843291', '299.97390361', '400.10848047', '498.044999135', '600.088323762', '699.997698171', '800.909593096', '900.02609639', '1000.02015671', '1088.26871473', '1200.0'])


    def testScalaFileA(self):
        
        msg = '''! arist_chromenh.scl
!
Aristoxenos' Chromatic/Enharmonic, 3 + 9 + 18 parts
 7
!
 50.00000
 200.00000
 500.00000
 700.00000
 750.00000
 900.00000
 2/1
'''
        sf = ScalaFile()
        ss = sf.readstr(msg)
        self.assertEqual(ss.pitchCount, 7)
        
        # all but last will be the same
        #print ss.getFileString()
        self.assertEqual(ss.getFileString()[:1], msg[:1])

        self.assertEqual([str(x) for x in ss.getIntervalSequence()], ['<music21.interval.Interval P1 (+50c)>', '<music21.interval.Interval m2 (+50c)>', '<music21.interval.Interval m3>', '<music21.interval.Interval M2>', '<music21.interval.Interval P1 (+50c)>', '<music21.interval.Interval m2 (+50c)>', '<music21.interval.Interval m3>'])

#-------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER = []


if __name__ == "__main__":
    # sys.arg test options will be used in mainTest()
    music21.mainTest(Test)


#------------------------------------------------------------------------------
# eof






