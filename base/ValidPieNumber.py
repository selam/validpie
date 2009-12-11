#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidPieNumber(ValidPieBase):
  def configure(self, options ={}, messages = {}):
    self.addMessage('max', '"%(value)s" must be at most %(max)s.');
    self.addMessage('min', '"%(value)s" must be at least %(min)s.');
    self.addOption('min');
    self.addOption('max');
    self.setMessage('invalid', '"%(value)s" is not a number.');

  def doClean(self, value):
    if not isinstance(value, (unicode, str, int, float)):
        raise ValidPieError(self, 'invalid', {'value': value})
    elif isinstance(value, (unicode, str)):
        if not value.isdigit():
          raise ValidPieError(self, 'invalid', {'value': value})
    try:
      clean = float(value);
    except TypeError:
      raise ValidPieError(self, 'invalid', {'value': value})

    if self.hasOption('max') and clean > self.getOption('max'):
      raise ValidPieError(self, 'max', {'value' : value, 'max' : self.getOption('max')})

    if self.hasOption('min') and clean < self.getOption('min'):
      raise ValidPieError(self, 'min', {'value' : value, 'min' : self.getOption('min')});

    return clean;