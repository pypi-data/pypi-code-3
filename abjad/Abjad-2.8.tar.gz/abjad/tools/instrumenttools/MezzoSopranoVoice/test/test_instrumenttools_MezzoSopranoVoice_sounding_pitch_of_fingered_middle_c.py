from abjad import *


def test_instrumenttools_MezzoSopranoVoice_sounding_pitch_of_fingered_middle_c_01():

    voice = instrumenttools.MezzoSopranoVoice()

    assert voice.sounding_pitch_of_fingered_middle_c == "c'"
