#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import time
import unittest

import bootstrap
from ValidPieDateTime import ValidPieDateTime
from ValidPieError import ValidPieError

class ValidPieDateTimeTest(unittest.TestCase):
      def setUp(self):
          self.__v = ValidPieDateTime()

      def testValidValue(self):
          self.assertEqual(self.__v.clean('2008-11-24 15:26:31'), '2008-11-24 15:26:31')
          self.__v.setOption('date_format', None)
          t = time.time();
          self.assertEqual(self.__v.clean(int(t)), time.strftime(self.__v.getOption('datetime_output'), time.localtime(t)))


suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieDateTimeTest)
unittest.TextTestRunner(verbosity=2).run(suite)

