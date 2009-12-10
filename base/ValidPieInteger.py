#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidPieInteger(ValidPieBase):

  def configure(self, options ={}, messages = {}):
    self.addMessage('max', '"%(value)s" must be at most %(max)s.')
    self.addMessage('min', '"%(value)s" must be at least %(min)s.')

    self.addOption('min');
    self.addOption('max');

    self.setMessage('invalid', '"%(value)s" is not an integer.')


  def doClean(self, value):
    try:
      clean = int(value);
    except ValueError:
      raise ValidPieError(self, 'invalid', {'value': value})

    if (str(clean) != value):
      ValidPieError(self, 'invalid', {'value' : value});

    if self.hasOption('max') and clean > self.getOption('max'):
      raise ValidPieError(self, 'max', {'value' : value, 'max' :self.getOption('max')})

    if self.hasOption('min') and clean < self.getOption('min'):
      raise ValidPieError(self, 'min', {'value' : value, 'min' :self.getOption('min')})

    return clean;


