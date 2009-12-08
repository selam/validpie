#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieRegex import ValidPieRegex


class ValidPieUrl(ValidPieRegex):
  def configure(self, options = {}, messages = {}):
    options.update({
      'pattern': '^(https?|ftps|http|ftp?)://(([a-z0-9-]+\.)+[a-z]{2,6}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:[0-9]+)?($|/?|/\S+)$'
    })

    ValidRegex.configure(self, options, messages)

if __name__ == '__main__':
  import unittest
  from ValidPieError import ValidPieError

  class TestValidUrl(unittest.TestCase):
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

  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidUrl)
  unittest.TextTestRunner(verbosity=2).run(suite)
