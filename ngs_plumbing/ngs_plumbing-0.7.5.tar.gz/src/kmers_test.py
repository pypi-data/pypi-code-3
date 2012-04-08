# This file is part of ngs_plumbing.

# ngs_plumbing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ngs_plumbing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ngs_plumbing.  If not, see <http://www.gnu.org/licenses/>.

# Copyright 2012 Laurent Gautier

import unittest
import io
import struct
import ngs_plumbing.kmers as kmers
from ngs_plumbing import dna
from ngs_plumbing import _libdna
import ngs_plumbing.fasta as fasta

class KmerTestCase(unittest.TestCase):

    def setUp(self):
        string = b'ATAAGCGGCT' + b'GATCGTAGCG' + \
            b'TTACGTTTTT' + b'TT' +\
            b'AATCGTAGGG' + \
            b'ATTCGCGGAT' +\
            b'TTTCGAAAAA' + b'AA' +\
            b'AAAAAAAAAA' + b'GATCGTAGCG' + \
            b'AAAAATTTTT' + b'TT' +\
            b'AATCGTAGGG' + \
            b'ATTCGCGGAT' +\
            b'TTTTTTTTTT' + b'TT'
        self._string = string


    def test_kmer_iter(self):
        string = self._string
        K = 17

        # step 1
        step = 1
        vec = dna.PackedDNABytes(string)
        res = tuple(kmers.kmerbytes_frombit2_iter(vec, K, step = step))

        offset = 0
        self.assertEqual(string[offset:(offset+K)], 
                         res[offset])
        offset = step
        self.assertEqual(string[offset:(offset+K)], 
                         res[offset])

        # step 8
        step = 8
        vec = dna.PackedDNABytes(string)
        res = tuple(kmers.kmerbytes_frombit2_iter(vec, K, step = step))

        self.assertEqual(string[step:(step+K)], 
                         res[1])




def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(KmerTestCase)
    return suite


def main():
    r = unittest.TestResult()
    suite().run(r)
    return r

if __name__ == "__main__":
    tr = unittest.TextTestRunner(verbosity = 2)
    suite = suite()
    tr.run(suite)

