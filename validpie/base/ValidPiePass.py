#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieError import ValidPieError
from ValidPieBase import ValidPieBase

class ValidPiePass(ValidPieBase):
  def doClean(self, value):
    return value;

  def clean(self, value):
    return value;

