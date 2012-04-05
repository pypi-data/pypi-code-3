import copy
import unittest, doctest


import music21
from music21 import meter
from music21 import lily as lilyModule
from music21 import note
from music21 import stream


class PolyphonicSnippet(stream.Score):
    '''
    a polyphonic snippet is a little Score-ette that represents an incipit or a cadence or something of that sort of a piece
    
    it is initialized with the contents of five excel cells -- the first three represent the notation of the 
    cantus, tenor, and contratenor, respectively.  the fourth is the cadence type (optional), the fifth
    is the time signature if not the same as the time signature of the parentPiece.
    

    >>> from music21 import *
    >>> cantus = trecento.trecentoCadence.TrecentoCadenceStream("c'2. d'8 c'4 a8 f4 f8 a4 c'4 c'8", '6/8')
    >>> tenor = trecento.trecentoCadence.TrecentoCadenceStream("F1. f2. e4. d", '6/8')
    >>> ps = trecento.polyphonicSnippet.PolyphonicSnippet([cantus, tenor, None, "8-8", "6/8"], parentPiece = "mom")
    >>> ps.elements
    [<music21.stream.Part ...>, <music21.stream.Part ...>]
    >>> ps.elements[0] is cantus
    True
    >>> ps.elements[0].classes
    ['Part', 'TrecentoCadenceStream', 'TinyNotationStream', 'Stream', 'Music21Object', 'JSONSerializer', 'object']
    >>> #_DOCS_SHOW ps.show()
    
    
    
    .. image:: images/trecento-polyphonicSnippet1.*
            :width: 450

    
    
    OMIT_FROM_DOCS
    
    >>> dummy = trecento.polyphonicSnippet.PolyphonicSnippet()
    >>> dummy.elements
    []
    >>> dumClass = dummy.__class__
    >>> dumClass
    <class 'music21.trecento.polyphonicSnippet.PolyphonicSnippet'>
    >>> dumdum = dumClass()
    >>> dumdum.__class__
    <class 'music21.trecento.polyphonicSnippet.PolyphonicSnippet'>
    >>> ps2 = ps.__class__()
    >>> ps2.elements
    []
    
    >>> dummy2 = trecento.polyphonicSnippet.Incipit()
    >>> dummy2.elements
    []
    
    '''
    
    def __init__(self, fiveExcelCells = None, parentPiece = None):
        stream.Score.__init__(self)
        if fiveExcelCells == None:
            fiveExcelCells = []
        if fiveExcelCells != []:        
            if len(fiveExcelCells) != 5:
                raise Exception("Need five Excel Cells to make a PolyphonicSnippet object")
    
            for part in fiveExcelCells[0:3]:
                if part is not None and hasattr(part, 'isStream') and part.isStream == True:
                    part.__class__ = stream.Part
                    part.classes.insert(0, 'Part')
            
            self.cadenceType = fiveExcelCells[3]
            self.timeSig = meter.TimeSignature(fiveExcelCells[4])
            self.parentPiece = parentPiece
            self.cantus = fiveExcelCells[0]
            self.tenor  = fiveExcelCells[1]
            self.contratenor = fiveExcelCells[2]
            
            if self.contratenor == "" or self.contratenor is None: 
                self.contratenor = None
            else:
                self.contratenor.id = 'Ct'
            if self.tenor == "" or self.tenor is None: 
                self.tenor = None
            else:
                self.tenor.id = 'T'

            if self.cantus == "" or self.cantus is None: 
                self.cantus = None
            else:
                self.cantus.id = 'C'

    
            self._appendParts()
            self._padParts()

    def _appendParts(self):
        '''
        appends each of the parts to the current score.
        '''
        foundTs = False
        for thisVoice in [self.cantus, self.contratenor, self.tenor]:        
            # thisVoice is a type of stream.Stream()
            
            if thisVoice is not None:
                if foundTs == False and len(thisVoice.getElementsByClass(meter.TimeSignature)) > 0:
                    foundTs = True
                thisVoice.makeNotation(inPlace = True)
                self.insert(0, thisVoice)
                
        if foundTs == False:
            self.insert(0, self.timeSig)
        self.rightBarline = 'final'


    def _padParts(self):
        foundTs = False
        for thisVoice in self.parts:        
            # thisVoice is a type of stream.Stream()
            
            if thisVoice is not None:
                if hasattr(self, 'frontPadLine'):
                    self.frontPadLine(thisVoice)
                elif hasattr(self, 'backPadLine'):
                    self.backPadLine(thisVoice)

        

    def headerWithPageNums(self):
        '''returns a string that prints an appropriate header for this cadence'''
        if (self.parentPiece is not None):
            parentPiece = self.parentPiece
            headOut = " \\header { \n piece = \\markup \\bold \""
            if (parentPiece.fischerNum):
                headOut += str(parentPiece.fischerNum) + ". " 
            if parentPiece.title:
                headOut += parentPiece.title
            if (parentPiece.pmfcVol and parentPiece.pmfcPageRange()):
                headOut += " PMFC " + str(parentPiece.pmfcVol) + " " + parentPiece.pmfcPageRange()
            headOut += "\" \n}\n";
            return headOut
        else:
            return ""

    def headerWithCadenceName(self):
        pass
    
    def header(self):
        return self.headerWithPageNums()
                    
    def lilyFromStream(self, thisStream):
        lilyOut = lilyModule.LilyString("  \\new Staff { " + thisStream.bestClef().lily.value + " " + thisStream.lily.value + " } \n")
        return lilyOut
    
    def _getLily(self):
        thesepartStreams = self.parts
        timeSig = self.timeSig

        lilyOut = lilyModule.LilyString("\\score {\n")
        lilyOut += "<< \\time " + str(timeSig) + "\n"
        for thisStream in thesepartStreams:
            lilyOut += self.lilyFromStream(thisStream)

        lilyOut += ">>\n"
        lilyOut += self.header() + "}\n"
        return lilyOut

    lily = property(_getLily)

    def findLongestCadence(self):
        '''
        returns the length. (in quarterLengths) for the longest line
        in the parts
        
        >>> from music21 import *
        >>> s1 = stream.Part([note.WholeNote()])
        >>> s2 = stream.Part([note.HalfNote()])
        >>> s3 = stream.Part([note.QuarterNote()])
        >>> fiveExcelRows = [s1, s2, s3, '', '2/2']
        >>> ps = trecento.polyphonicSnippet.PolyphonicSnippet(fiveExcelRows)
        >>> ps.findLongestCadence()
        4.0
        
        '''
        longestLineLength = 0
        for thisStream in self.parts:
            if thisStream is None:
                continue
            thisLength = thisStream.duration.quarterLength
            if thisLength > longestLineLength:
                longestLineLength = thisLength
        self.longestLineLength = longestLineLength
        return longestLineLength

    def measuresShort(self, thisStream):
        '''
        returns the number of measures short that each stream is compared to the longest stream.
        
        
        >>> from music21 import *
        >>> s1 = stream.Part([note.WholeNote()])
        >>> s2 = stream.Part([note.HalfNote()])
        >>> s3 = stream.Part([note.QuarterNote()])
        >>> fiveExcelRows = [s1, s2, s3, '', '1/2']
        >>> ps = trecento.polyphonicSnippet.PolyphonicSnippet(fiveExcelRows)
        >>> ps.findLongestCadence()
        4.0
        >>> ps.measuresShort(s2)
        1.0
        >>> ps.measuresShort(s3)
        1.5
        >>> ps.measuresShort(s1)
        0.0
        '''

        
        timeSigLength = self.timeSig.barDuration.quarterLength
        thisStreamLength = thisStream.duration.quarterLength
        shortness = self.findLongestCadence() - thisStreamLength
        shortmeasures = shortness/timeSigLength
        return shortmeasures



class Incipit(PolyphonicSnippet):
    snippetName = ""

    def backPadLine(self, thisStream):
        '''
        Pads a Stream with a bunch of rests at the
        end to make it the same length as the longest line

        >>> from music21 import *
        >>> ts = meter.TimeSignature('1/4')
        >>> s1 = stream.Part([ts])
        >>> s1.repeatAppend(note.QuarterNote(), 4)
        >>> s2 = stream.Part([ts])
        >>> s2.repeatAppend(note.QuarterNote(), 2)
        >>> s3 = stream.Part([ts])
        >>> s3.repeatAppend(note.QuarterNote(), 1)
        >>> fiveExcelRows = [s1, s2, s3, '', '1/4']
        >>> ps = trecento.polyphonicSnippet.Incipit(fiveExcelRows)
        >>> ps.backPadLine(s2)
        >>> s2.show('text')
        {0.0} <music21.stream.Measure 1 offset=0.0>
            {0.0} <music21.meter.TimeSignature 1/4>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.note.Note C>
        {1.0} <music21.stream.Measure 2 offset=1.0>
            {0.0} <music21.note.Note C>
        {2.0} <music21.stream.Measure 3 offset=2.0>
            {0.0} <music21.note.Rest rest>
        {3.0} <music21.stream.Measure 4 offset=3.0>
            {0.0} <music21.note.Rest rest>
            {1.0} <music21.bar.Barline style=final>
            
        '''
        shortMeasures = int(self.measuresShort(thisStream))

        if (shortMeasures > 0):
            shortDuration = self.timeSig.barDuration
            hasMeasures = thisStream.hasMeasures()
            if hasMeasures:
                lastMeasure = thisStream.getElementsByClass('Measure')[-1]
                maxMeasures = lastMeasure.number
                oldRightBarline = lastMeasure.rightBarline
                lastMeasure.rightBarline = None

            for i in range(0, shortMeasures):
                newRest = note.Rest()
                newRest.duration = copy.deepcopy(shortDuration)    
                newRest.transparent = 1
                if hasMeasures:
                    m = stream.Measure()
                    m.number = maxMeasures + 1 + i
                    m.append(newRest)
                    thisStream.append(m)
                else:
                    thisStream.append(newRest)
                
                if i == 0:
                    newRest.startTransparency = 1
                elif i == (shortMeasures - 1):
                    newRest.stopTransparency = 1

            if hasMeasures:
                lastMeasure = thisStream.getElementsByClass('Measure')[-1]
                lastMeasure.rightBarline = oldRightBarline



class FrontPaddedSnippet(PolyphonicSnippet):
    snippetName = ""

    def frontPadLine(self, thisStream):
        '''Pads a line with a bunch of rests at the
        front to make it the same length as the longest line
        
        >>> from music21 import *
        >>> ts = meter.TimeSignature('1/4')
        >>> s1 = stream.Part([ts])
        >>> s1.repeatAppend(note.QuarterNote(), 4)
        >>> s2 = stream.Part([ts])
        >>> s2.repeatAppend(note.QuarterNote(), 2)
        >>> s3 = stream.Part([ts])
        >>> s3.repeatAppend(note.QuarterNote(), 1)
        >>> fiveExcelRows = [s1, s2, s3, '', '1/4']
        >>> ps = trecento.polyphonicSnippet.FrontPaddedSnippet(fiveExcelRows)
        >>> ps.frontPadLine(s2)
        >>> s2.show('text')
        {0.0} <music21.stream.Measure 1 offset=0.0>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.meter.TimeSignature 1/4>
            {0.0} <music21.note.Rest rest>
        {1.0} <music21.stream.Measure 2 offset=1.0>
            {0.0} <music21.note.Rest rest>
        {2.0} <music21.stream.Measure 3 offset=2.0>
            {0.0} <music21.note.Note C>
        {3.0} <music21.stream.Measure 4 offset=3.0>
            {0.0} <music21.note.Note C>
            {1.0} <music21.bar.Barline style=final>
            
        '''
        shortMeasures = int(self.measuresShort(thisStream))

        if (shortMeasures > 0):
            shortDuration = self.timeSig.barDuration
            offsetShift = shortDuration.quarterLength * shortMeasures        
            hasMeasures = thisStream.hasMeasures()


            if hasMeasures:
                allM = thisStream.getElementsByClass('Measure')
                oldFirstM = allM[0]
                for m in allM:
                    m.number += shortMeasures
                    m.setOffsetBySite(thisStream, m.getOffsetBySite(thisStream) + offsetShift)
            else:
                for thisNote in thisStream.notesAndRests:
                    thisNote.setOffsetBySite(thisStream, thisNote.getOffsetBySite(thisStream) + offsetShift) 


            for i in range(0, shortMeasures):
                newRest = note.Rest()
                newRest.duration = copy.deepcopy(shortDuration)    
                newRest.transparent = 1
                if hasMeasures:
                    m = stream.Measure()
                    m.number = 1 + i
                    m.append(newRest)
                    thisStream.insert(shortDuration.quarterLength * i, m)
                else:
                    thisStream.insert(shortDuration.quarterLength * i, newRest)                
                if i == 0:
                    newRest.startTransparency = 1
                elif i == (shortMeasures - 1):
                    newRest.stopTransparency = 1

            if hasMeasures:
                newFirstM = thisStream.getElementsByClass('Measure')[0]
                oldFirstMEls = copy.copy(oldFirstM.elements)
                for n in oldFirstMEls:
                    if isinstance(n, note.GeneralNote):
                        pass
                    else:
                        nOffset = n.offset
                        oldFirstM.remove(n)
                        newFirstM.insert(nOffset, n)
        

    def header(self):
        headOut = " \\header { \n piece = \"" + self.parentPiece.title
        if (self.snippetName):
            headOut += " -- " + self.snippetName + " "
        headOut += " \" \n}\n";
        return headOut




class Test(unittest.TestCase):
    pass

    def runTest(self):
        pass

    def testCopyAndDeepcopy(self):
        '''Test copying all objects defined in this module
        '''
        import sys
        for part in sys.modules[self.__module__].__dict__.keys():
            if part.startswith('_') or part.startswith('__'):
                continue
            elif part in ['Test', 'TestExternal']:
                continue
            elif callable(part):
                #environLocal.printDebug(['testing copying on', part])
                obj = getattr(module, part)()
                a = copy.copy(obj)
                b = copy.deepcopy(obj)
                self.assertNotEqual(a, obj)
                self.assertNotEqual(b, obj)



#------------------------------------------------------------------------------
# eof

if __name__ == "__main__":
    music21.mainTest(Test)
