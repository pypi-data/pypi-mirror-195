# This file is placed in the Public Domain.


import unittest


from opr.encoder import dumps
from opr.objects import Object


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):


    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)
