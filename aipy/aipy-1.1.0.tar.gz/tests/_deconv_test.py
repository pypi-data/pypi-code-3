import unittest, ephem, random
import aipy as a, numpy as n

DIM = 128

class TestClean(unittest.TestCase):
    def test_clean2dc(self):
        res = n.zeros((DIM,DIM), dtype=n.complex)
        ker = n.zeros((DIM,DIM), dtype=n.complex)
        mdl = n.zeros((DIM,DIM), dtype=n.complex)
        area = n.zeros((DIM,DIM), dtype=n.int)
        self.assertRaises(ValueError, a._deconv.clean, \
            res,ker,mdl,area.astype(n.float))
        ker[0,0] = 1.
        res[0,0] = 1.; res[5,5] = 1.
        area[:4][:4] = 1
        rv = a._deconv.clean(res,ker,mdl,area,tol=1e-8)
        self.assertAlmostEqual(res[0,0], 0, 3)
        self.assertEqual(res[5,5], 1)
    def test_clean2dr(self):
        res = n.zeros((DIM,DIM), dtype=n.float)
        ker = n.zeros((DIM,DIM), dtype=n.float)
        mdl = n.zeros((DIM,DIM), dtype=n.float)
        area = n.zeros((DIM,DIM), dtype=n.int)
        self.assertRaises(ValueError, a._deconv.clean, \
            res,ker,mdl,area.astype(n.float))
        ker[0,0] = 1.
        res[0,0] = 1.; res[5,5] = 1.
        area[:4][:4] = 1
        rv = a._deconv.clean(res,ker,mdl,area,tol=1e-8)
        self.assertAlmostEqual(res[0,0], 0, 3)
    def test_clean1dc(self):
        res = n.zeros((DIM,), dtype=n.complex)
        ker = n.zeros((DIM,), dtype=n.complex)
        mdl = n.zeros((DIM,), dtype=n.complex)
        area = n.zeros((DIM,), dtype=n.int)
        self.assertRaises(ValueError, a._deconv.clean, \
            res,ker,mdl,area.astype(n.float))
        ker[0] = 1.
        res[0] = 1.; res[5] = 1.
        area[:4] = 1
        rv = a._deconv.clean(res,ker,mdl,area,tol=1e-8)
        self.assertAlmostEqual(res[0], 0, 3)
        self.assertEqual(res[5], 1)
    def test_clean1dr(self):
        res = n.zeros((DIM,), dtype=n.float)
        ker = n.zeros((DIM,), dtype=n.float)
        mdl = n.zeros((DIM,), dtype=n.float)
        area = n.zeros((DIM,), dtype=n.int)
        self.assertRaises(ValueError, a._deconv.clean, \
            res,ker,mdl,area.astype(n.float))
        ker[0] = 1.
        res[0] = 1.; res[5] = 1.
        area[:4] = 1
        rv = a._deconv.clean(res,ker,mdl,area,tol=1e-8)
        self.assertAlmostEqual(res[0], 0, 3)
        self.assertEqual(res[5], 1)
    

if __name__ == '__main__':
    unittest.main()
