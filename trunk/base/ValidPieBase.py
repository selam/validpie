#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2009 Sinelist

from Exceptions import InvalidArgumentException
from ValidPieError import ValidPieError

class ValidPieBase(object):
    def __init__(self, options = {}, messages = {}):
        self.requiredOptions = [];
        self.__options = {
          'required': True,
          'empty_value': None,
          'trim' : False
        };

        self.__messages = {
          'required': 'required',
          'invalid' : 'invalid'
        };

        self.__defaultMessages = {}
        self.__defaultOptions = {}

        self.configure(options, messages)

        self.setDefaultOptions(self.getOptions());
        self.setDefaultMessages(self.getMessages());

        if len(self.getRequiredOptions()) > 0:
          if len(options) == 0:
            raise InvalidArgumentException('%s requires the following option: "%s"' % (self.__class__.__name__, ', '.join(self.getRequiredOptions())))
          invalidOptions = [];
          for item in options:
              if item not in self.getRequiredOptions():
                  invalidOptions.append(item)

          if len(invalidOptions) > 0:
            raise InvalidArgumentException('%s requires the following option: "%s"' % (self.__class__.__name__, ', '.join(invalidOptions)))


        if len(self.getOptions()) > 0:
            invalidOptions = [];
            for item in options:
                if item not in self.getOptions().keys() and item not in self.getRequiredOptions():
                    invalidOptions.append(item)
            if len(invalidOptions) > 0:
                raise InvalidArgumentException('%s does not support the following options "%s"' % (self.__class__.__name__, ', '.join(invalidOptions)))

        if len(self.getMessages()) > 0:
            invalidMessages = []
            for item in messages:
                if item not in self.getMessages():
                  invalidMessages.append(item);
            if len(invalidMessages) > 0:
              raise InvalidArgumentException('%s does not support the following error codes "%s"' % (self.__class__.__name__, ', '.join(invalidMessages)))



        self.__options.update(options)
        self.__messages.update(messages)


    def setDefaultMessages(self, messages):
        """Sets default messages for all possible error codes."""
        self.__defaultMessages = messages

    def getDefaultMessages(self):
        """Returns default messages for all possible error codes."""
        return self.__defaultMessages;

    def setDefaultOptions(self, options):
        """Sets default option values."""
        self.__defaultOptions = options

    def getDefaultOptions(self):
        """Returns default option values."""
        return self.__defaultOptions

    def configure(self, options = {}, messages = {}):
        """dummy method, you can use that method in your validators"""
        pass

    def setOptions(self, options):
        """Changes all options."""
        self.__options = options;

    def getOptions(self):
        """Returns all options."""
        return self.__options

    def getOption(self, name):
        """Gets an option value."""
        return self.__options[name] if self.__options.has_key(name) else None;

    def addOption(self, option, value = None):
        """Adds a new option value with a default value."""
        self.__options[option] = value

    def setOption(self, name, value):
        """Changes an option value."""
        if name not in self.getOptions():

          raise InvalidArgumentException('%s does not support the following option: "%s"' % (self.__class__.__name__, name))
        self.addOption(name, value)

    def hasOption(self, name):
        """Returns True if the option exists."""
        return self.getOptions().has_key(name);

    def setMessage(self, name, message):
        """Changes an error message given the error code."""
        if name not in self.__messages:
            raise InvalidArgumentException('%s does not support the following error code: "%s"' %  (self.__class__.__name__, name))
        self.addMessage(name, message);

    def addMessage(self, name, message):
        """Adds a new error code with a default error message."""
        self.__messages[name] = message

    def setMessages(self, messages):
        """Changes all error messages."""
        self.__messages = messages

    def getMessages(self):
        """Returns an dict of current error messages."""
        return self.__messages

    def getMessage(self, name):
        """Returns an error message given an error code."""
        return self.__messages[name] if self.__messages.has_key(name) else None;


    def getRequiredOptions(self):
        """Returns all required option names."""
        return self.requiredOptions

    def addRequiredOption(self, option):
        """Adds a required option."""
        self.requiredOptions.append(option)

    def getRequiredOption(self, name):
        """Gets a required option."""
        return name if name in self.requiredOptions else None;

    def setInvalidMessage(self, message):
        """Sets the default invalid message"""
        self.setMessage('invalid', message)

    def setRequiredMessage(self, message):
        """Sets the default required message"""
        self.setMessage('required', message)

    def doClean(self, value):
        """Cleans the input value."""
        """Every subclass must implements this method."""
        raise NotImplementedError('doClean method must be implemented validators')

    def isEmpty(self, value):
        """Returns true if the value is empty."""
        return True if value in ('', {}, (), [], None) else False
    def getEmptyValue(self):
        """Returns an empty value for this validator."""
        return self.getOption('empty_value')

    def getErrorCodes(self):
        return self.getDefaultMessages().keys();

    def __getMessagesWithoutDefaults(self):
        """Returns all error messages with non default values."""
        messages = self.getMessages()
        for name, value in self.getDefaultMessages():
          if name in messages and messages[name] == value:
            del messages[name]

        return messages

    def __getOptionsWithoutDefaults(self):
        """Returns all options with non default values."""
        options = self.getOptions()
        for name, value in self.getDefaultOptions():
          if name in options and options[name] == value:
            del options[name]

        return options

    def clean(self, value):
        """Cleans the input value.
           This method is also responsible for trimming the input value
           and checking the required option."""
        clean = value

        if isinstance(value, (str, unicode)) and self.getOption('trim'):
          clean = value.strip();

        # value empty?
        if self.isEmpty(value):
          if self.getOption('required'):
            raise ValidPieError(self, 'required');
          return self.getEmptyValue()

        return self.doClean(clean);