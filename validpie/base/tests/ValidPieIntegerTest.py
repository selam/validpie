#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest

import bootstrap
from ValidPieInteger import ValidPieInteger
from ValidPieError import ValidPieError


class ValidPieIntegerTest(unittest.TestCase):
  def setUp(self):
      self.__v = ValidPieInteger({'min': 1, 'max': 5}, {'invalid': 'invalid'});

  def testValidValue(self):
      self.assertEqual(self.__v.clean('1'), 1)

  def testInvalidValue(self):
      try:
        self.__v.clean('si')
        self.fail('fail if given value is string (a-z)')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')
      try:
        self.__v.clean('A')
        self.fail('fail if given value is string (A-Z)')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieIntegerTest)
unittest.TextTestRunner(verbosity=2).run(suite)