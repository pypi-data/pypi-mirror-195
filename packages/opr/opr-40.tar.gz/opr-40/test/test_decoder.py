# This file is placed in the Public Domain.


import unittest


from opr.decoder import loads
from opr.encoder import dumps
from opr.objects import Object


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, "bla")

