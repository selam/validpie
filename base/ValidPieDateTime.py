#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieDate import ValidPieDate

class ValidPieDateTime(ValidPieDate):
  def configure(self, options = {}, messages = {}):
    ValidPieDate.configure(self, options, messages)
    self.setOption('with_time', True)
    self.addOption('date_format', '%Y-%m-%d %H:%M:%S')
