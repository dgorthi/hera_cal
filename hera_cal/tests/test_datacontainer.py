import unittest
from hera_cal import datacontainer
import numpy as np

class TestDataContainer(unittest.TestCase):

    def setUp(self):
        self.bls = [(1, 2), (2, 3), (3, 4), (1, 3), (2, 4)]  # not (1,4)
        self.pols = ['xx', 'yy']
        self.blpol = {}
        for bl in self.bls:
            self.blpol[bl] = {}
            for pol in self.pols:
                self.blpol[bl][pol] = 1j
        self.polbl = {}
        for pol in self.pols:
            self.polbl[pol] = {}
            for bl in self.bls:
                self.polbl[pol][bl] = 1j
        self.both = {}
        for pol in self.pols:
            for bl in self.bls:
                self.both[bl + (pol,)] = 1j

    def test_init(self):
        dc = datacontainer.DataContainer(self.blpol)
        for k in dc._data.keys():
            self.assertEqual(len(k), 3)
        self.assertEqual(set(self.bls), dc._bls)
        self.assertEqual(set(self.pols), dc._pols)
        dc = datacontainer.DataContainer(self.polbl)
        for k in dc._data.keys():
            self.assertEqual(len(k), 3)
        self.assertEqual(set(self.bls), dc._bls)
        self.assertEqual(set(self.pols), dc._pols)
        dc = datacontainer.DataContainer(self.both)
        for k in dc._data.keys():
            self.assertEqual(len(k), 3)
        self.assertEqual(set(self.bls), dc._bls)
        self.assertEqual(set(self.pols), dc._pols)
        self.assertRaises(
            AssertionError, datacontainer.DataContainer, {(1, 2, 3, 4): 2})

    def test_bls(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(set(self.bls), dc.bls())
        self.assertEqual(set(self.bls), dc.bls('xx'))
        self.assertEqual(set(self.bls), dc.bls('yy'))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(set(self.bls), dc.bls())
        self.assertEqual(set(self.bls), dc.bls('xx'))
        self.assertEqual(set(self.bls), dc.bls('yy'))
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(set(self.bls), dc.bls())
        self.assertEqual(set(self.bls), dc.bls('xx'))
        self.assertEqual(set(self.bls), dc.bls('yy'))

    def test_pols(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(set(self.pols), dc.pols())
        self.assertEqual(set(self.pols), dc.pols((1, 2)))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(set(self.pols), dc.pols())
        self.assertEqual(set(self.pols), dc.pols((1, 2)))
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(set(self.pols), dc.pols())
        self.assertEqual(set(self.pols), dc.pols((1, 2)))

    def test_keys(self):
        dc = datacontainer.DataContainer(self.blpol)
        keys = dc.keys()
        self.assertEqual(len(keys), len(self.pols) * len(self.bls))
        dc = datacontainer.DataContainer(self.polbl)
        keys = dc.keys()
        self.assertEqual(len(keys), len(self.pols) * len(self.bls))
        dc = datacontainer.DataContainer(self.both)
        keys = dc.keys()
        self.assertEqual(len(keys), len(self.pols) * len(self.bls))

    def test_getitem(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(dc[(1, 2, 'xx')], 1j)
        self.assertEqual(dc[(2, 1, 'xx')], -1j)
        self.assertEqual(dc[(1, 2)], {'xx': 1j, 'yy': 1j})
        self.assertEqual(set(dc['xx'].keys()), set(self.bls))
        self.assertEqual(dc[(1, 2, 'xx')], dc.get_data((1, 2, 'xx')))
        self.assertEqual(dc[(1, 2, 'xx')], dc.get_data(1, 2, 'xx'))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(dc[(1, 2, 'xx')], 1j)
        self.assertEqual(dc[(2, 1, 'xx')], -1j)
        self.assertEqual(dc[(1, 2)], {'xx': 1j, 'yy': 1j})
        self.assertEqual(set(dc['xx'].keys()), set(self.bls))
        self.assertEqual(dc[(2, 1, 'xx')], dc.get_data((2, 1, 'xx')))
        self.assertEqual(dc[(2, 1, 'xx')], dc.get_data(2, 1, 'xx'))
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(dc[(1, 2, 'xx')], 1j)
        self.assertEqual(dc[(2, 1, 'xx')], -1j)
        self.assertEqual(dc[(1, 2)], {'xx': 1j, 'yy': 1j})
        self.assertEqual(set(dc['xx'].keys()), set(self.bls))
        self.assertEqual(dc[(1, 2)], dc.get_data((1, 2)))
        self.assertEqual(dc[(1, 2)], dc.get_data(1, 2))



    def test_has_key(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertTrue(dc.has_key((2, 3, 'yy')))
        self.assertTrue(dc.has_key((2, 3), 'yy'))
        self.assertTrue(dc.has_key((3, 2), 'yy'))
        self.assertFalse(dc.has_key('xy'))
        self.assertFalse(dc.has_key((5, 6)))
        self.assertFalse(dc.has_key((1, 2, 'xy')))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertTrue(dc.has_key((2, 3, 'yy')))
        self.assertTrue(dc.has_key((2, 3), 'yy'))
        self.assertTrue(dc.has_key((3, 2), 'yy'))
        self.assertFalse(dc.has_key('xy'))
        self.assertFalse(dc.has_key((5, 6)))
        self.assertFalse(dc.has_key((1, 2, 'xy')))
        dc = datacontainer.DataContainer(self.both)
        self.assertTrue(dc.has_key((2, 3, 'yy')))
        self.assertTrue(dc.has_key((2, 3), 'yy'))
        self.assertTrue(dc.has_key((3, 2), 'yy'))
        self.assertFalse(dc.has_key('xy'))
        self.assertFalse(dc.has_key((5, 6)))
        self.assertFalse(dc.has_key((1, 2, 'xy')))

    def test_has_bl(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertTrue(dc.has_bl((2, 3)))
        self.assertFalse(dc.has_bl((0, 3)))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertTrue(dc.has_bl((2, 3)))
        self.assertFalse(dc.has_bl((0, 3)))
        dc = datacontainer.DataContainer(self.both)
        self.assertTrue(dc.has_bl((2, 3)))
        self.assertFalse(dc.has_bl((0, 3)))

    def test_has_pol(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertTrue(dc.has_pol('xx'))
        self.assertFalse(dc.has_pol('xy'))
        dc = datacontainer.DataContainer(self.polbl)
        self.assertTrue(dc.has_pol('xx'))
        self.assertFalse(dc.has_pol('xy'))
        dc = datacontainer.DataContainer(self.both)
        self.assertTrue(dc.has_pol('xx'))
        self.assertFalse(dc.has_pol('xy'))

    def test_get(self):
        dc = datacontainer.DataContainer(self.blpol)
        self.assertEqual(dc.get((1, 2), 'yy'), 1j)
        self.assertEqual(dc.get((2, 1), 'yy'), -1j)
        dc = datacontainer.DataContainer(self.polbl)
        self.assertEqual(dc.get((1, 2), 'yy'), 1j)
        self.assertEqual(dc.get((2, 1), 'yy'), -1j)
        dc = datacontainer.DataContainer(self.both)
        self.assertEqual(dc.get((1, 2), 'yy'), 1j)
        self.assertEqual(dc.get((2, 1), 'yy'), -1j)


if __name__ == '__main__':
    unittest.main()
