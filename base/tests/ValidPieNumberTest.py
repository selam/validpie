#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

import unittest

import bootstrap
from ValidPieNumber import ValidPieNumber
from ValidPieError import ValidPieError

class ValidPieNumberTest(unittest.TestCase):
    def setUp(self):
      self.__v = ValidPieNumber();

    def testValidValue(self):
      self.assertEqual(self.__v.clean('1'), 1.0)
      self.assertEqual(self.__v.clean(1), 1.0)
      self.assertEqual(self.__v.clean(0), 0.0)
      self.assertEqual(self.__v.clean(2), 2.0)

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieNumberTest)
unittest.TextTestRunner(verbosity=2).run(suite)