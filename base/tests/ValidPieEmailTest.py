#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest

import bootstrap
from ValidPieEmail import ValidPieEmail
from ValidPieError import ValidPieError

class ValidPieEmailTest(unittest.TestCase):
  def setUp(self):
      self.__v = ValidPieEmail();

  def testValidValue(self):
      self.assertEqual(self.__v.clean('timu@sinelist.com'), 'timu@sinelist.com')

  def testInvalidValue(self):
      try:
        self.__v.clean('timu@sinelist')
        self.fail('fail if given value like that: timu@sinelist')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')
      try:
        self.__v.clean('timu@.com')
        self.fail('fail if given value like that: timu@.com')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieEmailTest)
unittest.TextTestRunner(verbosity=2).run(suite)