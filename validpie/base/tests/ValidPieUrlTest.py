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
      self.__urls = {
          'validurls': [
              'http://www.sinelist.com',
              'http://sinelist.com',
              'https://sinelist.com',
              'https://www.sinelist.com',
              'http://www.sinelist.com:80/',
              'https://www.sinelist.com:80/',
              'https://sinelist.com:80/',
              'http://sinelist.com:80/',
              'http://www.sinelist.com/nofile.tgz'
              'ftp://www.sinelist.com',
              'ftp://sinelist.com',
              'ftps://sinelist.com',
              'ftps://www.sinelist.com',
              'ftp://www.sinelist.com:21/',
              'ftps://www.sinelist.com:21/',
              'ftps://sinelist.com:21/',
              'ftp://sinelist.com:21/',
              'ftp://www.sinelist.com/nofile.tgz'
          ],
          'invalidurls': [
            'sinelist.com',
            'http:/sinelist.com',
            'http://sinelist.com::sl',
          ]
        }
  def testValidValue(self):
      for url in self.__urls['validurls']:
          self.assertEqual(self.__v.clean(url), url)

  def testInvalidValue(self):
      for url in self.__urls['invalidurls']:
        try:
          self.__v.clean(url)
          self.fail('fail if given value like that: %s' % url)
        except ValidPieError, e:
          self.assertEqual(e.getMessage(), 'invalid')


suite = unittest.TestLoader().loadTestsFromTestCase(ValidPieUrlTest)
unittest.TextTestRunner(verbosity=2).run(suite)