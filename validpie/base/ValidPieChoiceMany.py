#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is part of ValidPie
# Copyright 2009 Sinelist

__author__ = 'Timu Eren<timu@sinelist.com>'

from ValidPieChoice import ValidPieChoice

class ValidPieChoiceMany(ValidPieChoice):
  def configure(self, options = {}, messages = {}):
    ValidPieChoice.configure(self, options, messages)
    self.addOption('multiple', True)