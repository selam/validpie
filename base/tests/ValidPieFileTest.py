#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

import unittest

import bootstrap
from ValidPieFile import ValidPieFile
from ValidPieError import ValidPieError

class ValidPieFileTest(unittest.TestCase):
  def setUp(self):
      self.__v = ValidPieFile({'mime_types': 'web_images'});

  def testValidValues(self):
      self.assertEqual(self.__v.clean({'tmp_name': 'fixtures/validimage.jpg'}), {'tmp_name': 'fixtures/validimage.jpg', 'type': 'image/jpeg', 'size': 306})

  def testInvalidValues(self):
      try:
        self.assertEqual(self.__v.clean({'tmp_name': 'fixtures/invalidimage.jpg'}), True)
        self.fail('invalid image should not return true value')
      except ValidPieError, e:
        self.assertEqual(e.getMessage(), 'Invalid mime type "text/plain".')


suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieFileTest)
unittest.TextTestRunner(verbosity=2).run(suite)