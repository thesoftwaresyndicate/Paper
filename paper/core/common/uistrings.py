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
The :mod:`uistrings` module provides standard strings for Paper.
"""
import logging

from paper.core.common import translate


log = logging.getLogger(__name__)


class UiStrings(object):
    """
    Provide standard strings for objects to use.
    """
    __instance__ = None

    def __new__(cls):
        """
        Override the default object creation method to return a single instance.
        """
        if not cls.__instance__:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        """
        These strings should need a good reason to be retranslated elsewhere.
        Should some/more/less of these have an &amp; attached?
        """
        self.About = translate('Paper.Ui', 'About')
        self.Add = translate('Paper.Ui', '&Add')
        self.Advanced = translate('Paper.Ui', 'Advanced')
        self.Browse = translate('Paper.Ui', 'Browse...')
        self.Cancel = translate('Paper.Ui', 'Cancel')
        self.ConfirmDelete = translate('Paper.Ui', 'Confirm Delete')
        self.Default = translate('Paper.Ui', 'Default')
        self.Delete = translate('Paper.Ui', '&Delete')
        self.Duplicate = translate('Paper.Ui', 'Duplicate Error')
        self.Edit = translate('Paper.Ui', '&Edit')
        self.Error = translate('Paper.Ui', 'Error')
        self.Export = translate('Paper.Ui', 'Export')
        self.File = translate('Paper.Ui', 'File')
        self.FontSizePtUnit = translate('Paper.Ui', 'pt', 'Abbreviated font pointsize unit')
        self.Help = translate('Paper.Ui', 'Help')
        self.LayoutStyle = translate('Paper.Ui', 'Layout style:')
        self.Load = translate('Paper.Ui', 'Load')
        self.New = translate('Paper.Ui', 'New')
        self.Open = translate('Paper.Ui', 'Open')
        self.Paper = translate('Paper.Ui', 'Paper')
        self.Preview = translate('Paper.Ui', 'Preview')
        self.SelectDelete = translate('Paper.Ui', 'You must select an item to delete.')
        self.SelectEdit = translate('Paper.Ui', 'You must select an item to edit.')
        self.Settings = translate('Paper.Ui', 'Settings')
        self.Save = translate('Paper.Ui', 'Save')
        self.SaveAs = translate('Paper.Ui', 'Save As')
        self.Tools = translate('Paper.Ui', 'Tools')
        self.UnsupportedFile = translate('Paper.Ui', 'Unsupported File')
        self.Version = translate('Paper.Ui', 'Version')
        self.View = translate('Paper.Ui', 'View')
        self.ViewMode = translate('Paper.Ui', 'View Mode')
