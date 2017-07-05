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
Provide Registry Services
"""
from paper.core.common import ComponentRegistry, de_hump


class RegistryMixin(object):
    """
    This adds registry components to classes to use at run time.
    """
    def __init__(self, parent):
        """
        Register the class and bootstrap hooks.
        """
        try:
            super(RegistryMixin, self).__init__(parent)
        except TypeError:
            super(RegistryMixin, self).__init__()
        ComponentRegistry().register(de_hump(self.__class__.__name__), self)
        ComponentRegistry().register_function('bootstrap_initialise', self.bootstrap_initialise)
        ComponentRegistry().register_function('bootstrap_post_set_up', self.bootstrap_post_set_up)

    def bootstrap_initialise(self):
        """
        Dummy method to be overridden
        """
        pass

    def bootstrap_post_set_up(self):
        """
        Dummy method to be overridden
        """
        pass
