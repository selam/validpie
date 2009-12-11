#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest

import bootstrap
from ValidPieBoolean import ValidPieBoolean
from ValidPieError import ValidPieError

class ValidPieBooleanTest(unittest.TestCase):
  def setUp(self):
    self.__v = ValidPieBoolean();

  def testValidTrueValue(self):
    self.assertEqual(self.__v.clean('true'), True);
    self.assertEqual(self.__v.clean('yes'), True);
    self.assertEqual(self.__v.clean('y'), True);
    self.assertEqual(self.__v.clean('on'), True);
    self.assertEqual(self.__v.clean('1'), True);
    self.assertEqual(self.__v.clean(True), True);
    self.assertEqual(self.__v.clean(1), True);

  def testValidFalseValue(self):
    self.assertEqual(self.__v.clean('false'), False);
    self.assertEqual(self.__v.clean('no'), False);
    self.assertEqual(self.__v.clean('n'), False);
    self.assertEqual(self.__v.clean('off'), False);
    self.assertEqual(self.__v.clean('0'), False);
    self.assertEqual(self.__v.clean(False), False);
    self.assertEqual(self.__v.clean(None), False);
    self.assertEqual(self.__v.clean(0), False);

  def testEmptyValue(self):
    self.assertEqual(self.__v.clean(), False);

  def testInvalidValue(self):
    self.__v.setOption('required', True);
    try:
      self.assertEqual(self.__v.clean([]), False)
      self.fail('list, should not be true or false')
    except ValidPieError, e:
      self.assertEqual(e.getMessage(), 'required')
    try:
      self.assertEqual(self.__v.clean({}), False)
      self.fail('list, should not be true or false')
    except ValidPieError, e:
      self.assertEqual(e.getMessage(), 'required')
    try:
      self.assertEqual(self.__v.clean('aa'), False)
      self.fail('code is fail if given value invalid string')
    except ValidPieError, e:
      self.assertEqual(e.getMessage(), 'invalid')
    try:
      self.assertEqual(self.__v.clean(1111), False)
      self.fail('code is fail if given value invalid integer')
    except ValidPieError, e:
      self.assertEqual(e.getMessage(), 'invalid')

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieBooleanTest)
unittest.TextTestRunner(verbosity=2).run(suite)