#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'
import unittest

import bootstrap
from ValidPieDate import ValidPieDate
from ValidPieError import ValidPieError

class ValidPieDateTest(unittest.TestCase):
      def setUp(self):
          self.__v = ValidPieDate();

      def testValidDate(self):
          self.assertEqual(self.__v.clean({'year': '2007', 'month': '10', 'day': '10'}), '2007-10-10')
          self.__v.setOption('date_format', '%Y-%m-%d')
          self.assertEqual(self.__v.clean('2007-10-10'), '2007-10-10')
          self.assertEqual(self.__v.clean('2007-10-10'), '2007-10-10')
          self.__v.setOption('with_time', True)
          self.__v.setOption('date_format', '%Y-%m-%d %H')
          self.__v.addOption('datetime_output', '%Y-%m-%d %H')
          self.assertEqual(self.__v.clean('2007-10-10 23'), '2007-10-10 23')
      def testInvalidDate(self):
          self.__v.setOption('date_format', None)
          try:
            self.__v.clean({'year': '2007', 'month': '2', 'day': '31'})
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), "Invalid date {'month': '2', 'day': '31', 'year': '2007'}.")

          self.__v.setOption('date_format', '%Y-%m-%d')
          try:
            self.__v.clean('2009-2-30')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), "Invalid date 2009-2-30.")
          self.__v.setOption('date_format', '%Y-%m-%d')
          try:
            self.__v.clean('test')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), "Invalid date test.")
          self.__v.setOption('date_format', None)
          try:
            self.__v.clean('test')
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), "Invalid date test.")
          try:
            self.__v.clean({'year': 2007})
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), "Invalid date {'year': 2007}.")
          self.__v.setOption('with_time', True)
          try:
            self.__v.clean({'year': 2007, 'month': 3, 'day': '4', 'second': '55'})
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), "Invalid date {'second': '55', 'month': 3, 'day': '4', 'year': 2007}.")
          try:
            self.__v.clean({'year': 2007, 'month': 3, 'day': '4', 'second': '55', 'minute': '11'})
          except ValidPieError, e:
            self.assertEqual(e.getMessage(), "Invalid date {'second': '55', 'month': 3, 'day': '4', 'minute': '11', 'year': 2007}.")
suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieDateTest)
unittest.TextTestRunner(verbosity=2).run(suite)