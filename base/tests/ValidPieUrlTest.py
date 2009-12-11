#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest

import bootstrap
from ValidPieUrl import ValidPieUrl
from ValidPieError import ValidPieError

class ValidPieUrlTest(unittest.TestCase):
  def setUp(self):
      self.__v = ValidPieUrl();

  def testValidValue(self):
      self.assertEqual(self.__v.clean('http://www.sinelist.com/'), u'http://www.sinelist.com/')

  def testInvalidValue(self):
      try:
        self.__v.clean('gopher://ddd')
        self.fail('fail if given value like that: gopher://ddd')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')
      try:
        self.__v.clean('telnet://127.0.0.1:8080/')
        self.fail('fail if given value like that: telnet://127.0.0.1:8080/')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieUrlTest)
unittest.TextTestRunner(verbosity=2).run(suite)