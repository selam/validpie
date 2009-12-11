#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest
import time

import bootstrap
from Exceptions import InvalidArgumentException
from ValidPieTime import ValidPieTime
from ValidPieError import ValidPieError

class ValidPieTimeTest(unittest.TestCase):
      def setUp(self):
          self.__v = ValidPieTime();

      def testValidValue(self):
          self.__v.setOption('required', False)
          self.assertEqual(self.__v.clean(None), None, 'clean() returns null if not required')
          self.assertEqual(self.__v.clean({'hour': '', 'minute': '', 'second': ''}), None, 'clean() returns null if not required')
          self.__v.setOption('time_format', '%H:%M:%S')
          self.assertEqual(self.__v.clean('16:35:12'), '16:35:12', 'clean() accepts times parsable time')
          t = time.time();
          self.__v.setOption('time_format', None)
          self.assertEqual(self.__v.clean(t), time.strftime(self.__v.getOption('time_output'), time.localtime(t)))
          self.assertEqual(self.__v.clean({'hour': 20, 'minute': 10, 'second': 15}), '20:10:15', 'clean() accepts times as dict')
          self.assertEqual(self.__v.clean({'hour': '20', 'minute': '10', 'second': '15'}), '20:10:15', 'clean() accepts times as dict')
          self.assertEqual(self.__v.clean({'hour': '0', 'minute': '0', 'second': '0'}), '00:00:00', 'clean() accepts times as dict')
          self.assertEqual(self.__v.clean({'hour': 0, 'minute': 0, 'second': 0}), '00:00:00', 'clean() accepts times as dict')
          self.__v.setOption('time_output', '%H/%M/%S')
          self.assertEqual(self.__v.clean({'hour': 11, 'minute': 15, 'second': 56}), '11/15/56', 'time output format change')

      def testInvalidValue(self):
          try:
            self.__v.clean('not an time')
            self.fail('raise a ValidPieError if the time is a string and is not parsable')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), 'invalid')
          try:
            self.__v.clean({'hour': '', 'minute': '0', 'second': '0'})
            self.fail('raise a ValidPieError if the time not valid')
          except ValidPieError, e:
            self.assertEqual(e.getCode(), 'invalid')
          try:
            self.__v.clean({'hour': '', 'minute': '1', 'second': '15'})
            self.fail('raise a ValidPieError if the time not valid')
          except ValidPieError, e:
            self.assertEqual(e.getCode(), 'invalid')
          try:
            self.__v.clean({'hour': '-2', 'minute': '1', 'second': '15'})
            self.fail('raise a ValidPieError if the time not valid')
          except ValidPieError, e:
            self.assertEqual(e.getCode(), 'invalid')
          try:
            self.__v.setOption('required', True)
            self.__v.clean({'hour': '', 'minute': '', 'second': ''})
            self.fail('raise a ValidPieError if the time is empty')
          except ValidPieError, e:
            self.assertEqual(e.getCode(), 'required')
          try:
            self.__v.setOption('required', True)
            self.__v.clean(None)
            self.fail('raise a ValidPieError if the time is empty')
          except ValidPieError, e:
            self.assertEqual(e.getCode(), 'required')
          try:
            self.__v.setOption('required', True)
            self.__v.clean({'hour': None, 'minute': None, 'second': None})
            self.fail('raise a ValidPieError if the time is empty')
          except ValidPieError, e:
            self.assertEqual(e.getCode(), 'required')

suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieTimeTest)
unittest.TextTestRunner(verbosity=2).run(suite)