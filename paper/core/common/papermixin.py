# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# Paper - Open Source PDF Manipulation                                        #
# --------------------------------------------------------------------------- #
# Copyright (c) 2017 Paper Developers                                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the Lesser GNU Public License as published by the Free   #
# Software Foundation; version 3 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the Lesser GNU Public License for     #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the Lesser GNU Public License along      #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
Provide Error Handling and logging Services
"""
import logging
import inspect

from paper.core.common import trace_error_handler

DO_NOT_TRACE_EVENTS = ['paintEvent', 'drag_enter_event', 'drop_event', 'resizeEvent']


class PaperMixin(object):
    """
    Base Calling object for Paper classes.
    """
    def __init__(self, *args, **kwargs):
        super(PaperMixin, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger("%s.%s" % (self.__module__, self.__class__.__name__))
        if self.logger.getEffectiveLevel() == logging.DEBUG:
            for name, m in inspect.getmembers(self, inspect.ismethod):
                if name not in DO_NOT_TRACE_EVENTS:
                    if not name.startswith("_") and not name.startswith("log"):
                        setattr(self, name, self.logging_wrapper(m, self))

    def logging_wrapper(self, func, parent):
        """
        Code to added debug wrapper to work on called functions within a decorated class.
        """
        def wrapped(*args, **kwargs):
            parent.logger.debug("Entering %s" % func.__name__)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if parent.logger.getEffectiveLevel() <= logging.ERROR:
                    parent.logger.error('Exception in %s : %s' % (func.__name__, e))
                raise e
        return wrapped

    def log_debug(self, message):
        """
        Common log debug handler
        """
        self.logger.debug(message)

    def log_info(self, message):
        """
        Common log info handler
        """
        self.logger.info(message)

    def log_error(self, message):
        """
        Common log error handler which prints the calling path
        """
        trace_error_handler(self.logger)
        self.logger.error(message)

    def log_exception(self, message):
        """
        Common log exception handler which prints the calling path
        """
        trace_error_handler(self.logger)
        self.logger.exception(message)
