#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidPieBoolean(ValidPieBase):
  def configure(self, options = {}, messages = {}):
      self.addOption('true_values',  ('true', 't', 'yes', 'y', 'on', '1',True, 1));
      self.addOption('false_values', ('false', 'f', 'no', 'n', 'off', '0', False, None, 0));

      self.setOption('required', False);
      self.setOption('empty_value', False);

  def doClean(self, value=None):
    if value in self.getOption('true_values'):
      return True
    elif value in self.getOption('false_values'):
      return False
    else:
      raise ValidPieError(self, 'invalid', {'value' : value})
