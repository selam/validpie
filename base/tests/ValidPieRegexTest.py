#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest

import bootstrap
from ValidPieRegex import ValidPieRegex
from ValidPieError import ValidPieError


import unittest
class ValidPieRegexTest(unittest.TestCase):
    def setUp(self):
      self.__v = ValidPieRegex({'pattern': r'deneme'}, {'invalid': 'invalid "%(value)s"'})

    def testValidValue(self):
      value = self.__v.clean('deneme');
      self.assertEqual(value, u'deneme')

    def testInvalidValue(self):
      try:
        value = self.__v.clean('sarkimi soylerken');
        self.fail('fail if not match')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), u'invalid "sarkimi soylerken"')

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieRegexTest)
unittest.TextTestRunner(verbosity=2).run(suite)