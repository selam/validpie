#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest

import bootstrap
from ValidPieChoice import ValidPieChoice
from ValidPieError import ValidPieError

class ValidPieChoiceTest(unittest.TestCase):
  def setUp(self):
    try:
      self.__v = ValidPieChoice();
    except Exception, e:
      self.assertEqual(e.getMessage(), 'ValidPieChoice requires the following option: "choices"')
    self.__v = ValidPieChoice({'choices': ['a', 'b', 'c']});

  def testValidTrueValue(self):
      self.assertEqual(self.__v.clean('a'), 'a')
      self.assertEqual(self.__v.clean('b'), 'b')
      self.assertEqual(self.__v.clean('c'), 'c')

  def testValidCallableValue(self):
      class callableValue(object):
          def __call__(self):
            return ['a', 'b']

      callableObject = callableValue();

      self.__v.setOption('choices', callableObject)
      self.assertEqual(self.__v.clean('a'), 'a')

  def testEmptyValue(self):
      try:
        self.assertEqual(self.__v.clean(''), '')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'required')
  def testInvalidValue(self):
      try:
        self.assertEqual(self.__v.clean('aa'), 'a')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'invalid')

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieChoiceTest)
unittest.TextTestRunner(verbosity=2).run(suite)