#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist


from ValidRegex import ValidRegex

class ValidEmail(ValidRegex):
  def configure(self, options = {}, messages = {}):
    options.update({
      'pattern': '^.+\\@(\\[?)[a-zA-Z1-9\\-\\.]+\\.([a-zA-Z]{2,4})(\\]?)$'
    })
    ValidRegex.configure(self, options, messages)


if __name__ == '__main__':
  import unittest
  from ValidPieError import ValidPieError

  class TestValidEmail(unittest.TestCase):
    def setUp(self):
        self.__v = ValidEmail();

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

  suite = unittest.TestLoader().loadTestsFromTestCase(TestValidEmail)
  unittest.TextTestRunner(verbosity=2).run(suite)

