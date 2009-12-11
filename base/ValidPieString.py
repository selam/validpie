#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidPieString(ValidPieBase):
  def configure(self, options = {}, messages = {}):
    self.addMessage('max_length', '"%(value)s" is too long (%(max_length)s characters max).')
    self.addMessage('min_length', '"%(value)s" is too short (%(min_length)s characters min).')

    self.addOption('max_length')
    self.addOption('min_length')

    self.setOption('empty_value', '')


  def doClean(self, value):
      if not isinstance(value, basestring):
        if isinstance(value, (int, float)):
          value = str(value)
        elif isinstance(value, (list, tuple, dict, None)):
          raise ValidPieError(self, 'invalid', {'value': value})
      try:
        clean = unicode(str(value), 'UTF-8')
      except UnicodeEncodeError, e:
        clean = value

      if self.hasOption('max_length') and len(clean) > self.getOption('max_length'):
         raise ValidPieError(self, 'max_length', {'value': clean, 'max_length': self.getOption('max_length')})

      if self.hasOption('min_length') and len(clean) < self.getOption('min_length'):
        raise ValidPieError(self, 'min_length', {'value': clean, 'min_length': self.getOption('min_length')})

      return clean;