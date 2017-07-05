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
This class contains the core default settings.
"""
import datetime
import logging
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from paper.core.common import UiStrings, is_win, is_linux


log = logging.getLogger(__name__)


# Fix for bug #1014422.
X11_BYPASS_DEFAULT = True
if is_linux():
    # Default to False on Gnome.
    X11_BYPASS_DEFAULT = bool(not os.environ.get('GNOME_DESKTOP_SESSION_ID'))
    # Default to False on Xfce.
    if os.environ.get('DESKTOP_SESSION') == 'xfce':
        X11_BYPASS_DEFAULT = False


def recent_files_conv(value):
    """
    If the value is not a list convert it to a list
    :param value: Value to convert
    :return: value as a List
    """
    if isinstance(value, list):
        return value
    elif isinstance(value, str):
        return [value]
    elif isinstance(value, bytes):
        return [value.decode()]
    return []


class AppSettings(QtCore.QSettings):
    """
    Class to wrap QSettings.

    * Exposes all the methods of QSettings.
    * Adds functionality for Paper Portable. If the ``defaultFormat`` is set to
      ``IniFormat``, and the path to the Ini file is set using ``set_filename``,
      then the Settings constructor (without any arguments) will create a Settings
      object for accessing settings stored in that Ini file.

    ``__default_settings__``
        This dict contains all core settings with their default values.

    ``__obsolete_settings__``
        Each entry is structured in the following way::

            ('general/enable slide loop', 'advanced/slide limits', [(SlideLimits.Wrap, True), (SlideLimits.End, False)])

        The first entry is the *old key*; it will be removed.

        The second entry is the *new key*; we will add it to the config. If this is just an empty string, we just remove
        the old key. The last entry is a list containing two-pair tuples. If the list is empty, no conversion is made.
        If the first value is callable i.e. a function, the function will be called with the old setting's value.
        Otherwise each pair describes how to convert the old setting's value::

            (SlideLimits.Wrap, True)

        This means, that if the value of ``general/enable slide loop`` is equal (``==``) ``True`` then we set
        ``advanced/slide limits`` to ``SlideLimits.Wrap``. **NOTE**, this means that the rules have to cover all cases!
        So, if the type of the old value is bool, then there must be two rules.
    """
    __default_settings__ = {
        'advanced/add page break': False,
        'advanced/alternate rows': not is_win(),
        'advanced/data path': '',
        'advanced/default color': '#ffffff',
        'advanced/default image': ':/graphics/paper-splash-screen.png',
        'advanced/enable exit confirmation': True,
        'advanced/is portable': False,
        'advanced/max recent files': 20,
        'advanced/recent file count': 4,
        'advanced/x11 bypass wm': X11_BYPASS_DEFAULT,
        'crashreport/last directory': '',
        'formattingTags/html_tags': '',
        'core/has run wizard': False,
        'core/language': '[en]',
        'core/last version test': '',
        'core/recent files': [],
        'core/save prompt': False,
        'core/show splash': True,
        'core/update check': True,
        'core/view mode': 'default',
        'core/application version': '0.0',
        'SettingsImport/file_date_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'SettingsImport/Make_Changes': 'At_Own_RISK',
        'SettingsImport/type': 'Paper_settings_export',
        'SettingsImport/version': '',
        'user interface/main window splitter geometry': QtCore.QByteArray(),
        'user interface/main window state': QtCore.QByteArray()
    }
    __file_path__ = ''
    __obsolete_settings__ = [
        # ('general/recent files', 'core/recent files', [(recent_files_conv, None)]),
    ]

    @staticmethod
    def extend_default_settings(default_values):
        """
        Static method to merge the given ``default_values`` with the ``Settings.__default_settings__``.

        :param default_values: A dict with setting keys and their default values.
        """
        AppSettings.__default_settings__.update(default_values)

    @staticmethod
    def set_filename(ini_file):
        """
        Sets the complete path to an Ini file to be used by Settings objects.

        Does not affect existing Settings objects.
        """
        AppSettings.__file_path__ = ini_file

    @staticmethod
    def set_up_default_values():
        """
        This static method is called on start up. It is used to perform any operation on the __default_settings__ dict.
        """
        # Make sure the string is translated (when building the dict the string is not translated because the translate
        # function was not set up as this stage).
        AppSettings.__default_settings__['advanced/default service name'] = UiStrings().DefaultServiceName

    def __init__(self, *args):
        """
        Constructor which checks if this should be a native settings object, or an INI file.
        """
        if not args and AppSettings.__file_path__ and AppSettings.defaultFormat() == AppSettings.IniFormat:
            QtCore.QSettings.__init__(self, AppSettings.__file_path__, AppSettings.IniFormat)
        else:
            QtCore.QSettings.__init__(self, *args)
        # Add shortcuts here so QKeySequence has a QApplication instance to use.
        AppSettings.__default_settings__.update({
            'shortcuts/aboutItem': [QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_F1)],
            'shortcuts/addToService': [],
            'shortcuts/audioPauseItem': [],
            'shortcuts/displayTagItem': [],
            'shortcuts/blankScreen': [QtGui.QKeySequence(QtCore.Qt.Key_Period)],
            'shortcuts/collapse': [QtGui.QKeySequence(QtCore.Qt.Key_Minus)],
            'shortcuts/desktopScreen': [QtGui.QKeySequence(QtCore.Qt.Key_D)],
            'shortcuts/delete': [QtGui.QKeySequence(QtGui.QKeySequence.Delete)],
            'shortcuts/down': [QtGui.QKeySequence(QtCore.Qt.Key_Down)],
            'shortcuts/editSong': [],
            'shortcuts/escapeItem': [QtGui.QKeySequence(QtCore.Qt.Key_Escape)],
            'shortcuts/expand': [QtGui.QKeySequence(QtCore.Qt.Key_Plus)],
            'shortcuts/exportThemeItem': [],
            'shortcuts/fileNewItem': [QtGui.QKeySequence(QtGui.QKeySequence.New)],
            'shortcuts/fileSaveAsItem': [QtGui.QKeySequence(QtGui.QKeySequence.SaveAs)],
            'shortcuts/fileExitItem': [QtGui.QKeySequence(QtGui.QKeySequence.Quit)],
            'shortcuts/fileSaveItem': [QtGui.QKeySequence(QtGui.QKeySequence.Save)],
            'shortcuts/fileOpenItem': [QtGui.QKeySequence(QtGui.QKeySequence.Open)],
            'shortcuts/goLive': [],
            'shortcuts/importThemeItem': [],
            'shortcuts/importBibleItem': [],
            'shortcuts/listViewBiblesDeleteItem': [QtGui.QKeySequence(QtGui.QKeySequence.Delete)],
            'shortcuts/listViewBiblesPreviewItem': [QtGui.QKeySequence(QtCore.Qt.Key_Return),
                                                    QtGui.QKeySequence(QtCore.Qt.Key_Enter)],
            'shortcuts/listViewBiblesLiveItem': [QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Return),
                                                 QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Enter)],
            'shortcuts/listViewBiblesServiceItem': [QtGui.QKeySequence(QtCore.Qt.Key_Plus),
                                                    QtGui.QKeySequence(QtCore.Qt.Key_Equal)],
            'shortcuts/listViewCustomDeleteItem': [QtGui.QKeySequence(QtGui.QKeySequence.Delete)],
            'shortcuts/listViewCustomPreviewItem': [QtGui.QKeySequence(QtCore.Qt.Key_Return),
                                                    QtGui.QKeySequence(QtCore.Qt.Key_Enter)],
            'shortcuts/listViewCustomLiveItem': [QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Return),
                                                 QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Enter)],
            'shortcuts/listViewCustomServiceItem': [QtGui.QKeySequence(QtCore.Qt.Key_Plus),
                                                    QtGui.QKeySequence(QtCore.Qt.Key_Equal)],
            'shortcuts/listViewImagesDeleteItem': [QtGui.QKeySequence(QtGui.QKeySequence.Delete)],
            'shortcuts/listViewImagesPreviewItem': [QtGui.QKeySequence(QtCore.Qt.Key_Return),
                                                    QtGui.QKeySequence(QtCore.Qt.Key_Enter)],
            'shortcuts/listViewImagesLiveItem': [QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Return),
                                                 QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Enter)],
            'shortcuts/listViewImagesServiceItem': [QtGui.QKeySequence(QtCore.Qt.Key_Plus),
                                                    QtGui.QKeySequence(QtCore.Qt.Key_Equal)],
            'shortcuts/listViewMediaDeleteItem': [QtGui.QKeySequence(QtGui.QKeySequence.Delete)],
            'shortcuts/listViewMediaPreviewItem': [QtGui.QKeySequence(QtCore.Qt.Key_Return),
                                                   QtGui.QKeySequence(QtCore.Qt.Key_Enter)],
            'shortcuts/listViewMediaLiveItem': [QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Return),
                                                QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Enter)],
            'shortcuts/listViewMediaServiceItem': [QtGui.QKeySequence(QtCore.Qt.Key_Plus),
                                                   QtGui.QKeySequence(QtCore.Qt.Key_Equal)],
            'shortcuts/listViewPresentationsDeleteItem': [QtGui.QKeySequence(QtGui.QKeySequence.Delete)],
            'shortcuts/listViewPresentationsPreviewItem': [QtGui.QKeySequence(QtCore.Qt.Key_Return),
                                                           QtGui.QKeySequence(QtCore.Qt.Key_Enter)],
            'shortcuts/listViewPresentationsLiveItem': [QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Return),
                                                        QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Enter)],
            'shortcuts/listViewPresentationsServiceItem': [QtGui.QKeySequence(QtCore.Qt.Key_Plus),
                                                           QtGui.QKeySequence(QtCore.Qt.Key_Equal)],
            'shortcuts/listViewSongsDeleteItem': [QtGui.QKeySequence(QtGui.QKeySequence.Delete)],
            'shortcuts/listViewSongsPreviewItem': [QtGui.QKeySequence(QtCore.Qt.Key_Return),
                                                   QtGui.QKeySequence(QtCore.Qt.Key_Enter)],
            'shortcuts/listViewSongsLiveItem': [QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Return),
                                                QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Enter)],
            'shortcuts/listViewSongsServiceItem': [QtGui.QKeySequence(QtCore.Qt.Key_Plus),
                                                   QtGui.QKeySequence(QtCore.Qt.Key_Equal)],
            'shortcuts/lockPanel': [],
            'shortcuts/modeDefaultItem': [],
            'shortcuts/modeLiveItem': [],
            'shortcuts/make_live': [QtGui.QKeySequence(QtCore.Qt.Key_Return), QtGui.QKeySequence(QtCore.Qt.Key_Enter)],
            'shortcuts/moveUp': [QtGui.QKeySequence(QtCore.Qt.Key_PageUp)],
            'shortcuts/moveTop': [QtGui.QKeySequence(QtCore.Qt.Key_Home)],
            'shortcuts/modeSetupItem': [],
            'shortcuts/moveBottom': [QtGui.QKeySequence(QtCore.Qt.Key_End)],
            'shortcuts/moveDown': [QtGui.QKeySequence(QtCore.Qt.Key_PageDown)],
            'shortcuts/nextTrackItem': [],
            'shortcuts/nextItem_live': [QtGui.QKeySequence(QtCore.Qt.Key_Down),
                                        QtGui.QKeySequence(QtCore.Qt.Key_PageDown)],
            'shortcuts/nextItem_preview': [QtGui.QKeySequence(QtCore.Qt.Key_Down),
                                           QtGui.QKeySequence(QtCore.Qt.Key_PageDown)],
            'shortcuts/nextService': [QtGui.QKeySequence(QtCore.Qt.Key_Right)],
            'shortcuts/newService': [],
            'shortcuts/offlineHelpItem': [QtGui.QKeySequence(QtGui.QKeySequence.HelpContents)],
            'shortcuts/onlineHelpItem': [QtGui.QKeySequence(QtGui.QKeySequence.HelpContents)],
            'shortcuts/openService': [],
            'shortcuts/saveService': [],
            'shortcuts/previousItem_live': [QtGui.QKeySequence(QtCore.Qt.Key_Up),
                                            QtGui.QKeySequence(QtCore.Qt.Key_PageUp)],
            'shortcuts/playbackPause': [],
            'shortcuts/playbackPlay': [],
            'shortcuts/playbackStop': [],
            'shortcuts/playSlidesLoop': [],
            'shortcuts/playSlidesOnce': [],
            'shortcuts/previousService': [QtGui.QKeySequence(QtCore.Qt.Key_Left)],
            'shortcuts/previousItem_preview': [QtGui.QKeySequence(QtCore.Qt.Key_Up),
                                               QtGui.QKeySequence(QtCore.Qt.Key_PageUp)],
            'shortcuts/printServiceItem': [QtGui.QKeySequence(QtGui.QKeySequence.Print)],
            'shortcuts/songExportItem': [],
            'shortcuts/songUsageStatus': [QtGui.QKeySequence(QtCore.Qt.Key_F4)],
            'shortcuts/searchShortcut': [QtGui.QKeySequence(QtGui.QKeySequence.Find)],
            'shortcuts/settingsShortcutsItem': [],
            'shortcuts/settingsImportItem': [],
            'shortcuts/settingsPluginListItem': [QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_F7)],
            'shortcuts/songUsageDelete': [],
            'shortcuts/settingsConfigureItem': [QtGui.QKeySequence(QtGui.QKeySequence.Preferences)],
            'shortcuts/shortcutAction_B': [QtGui.QKeySequence(QtCore.Qt.Key_B)],
            'shortcuts/shortcutAction_C': [QtGui.QKeySequence(QtCore.Qt.Key_C)],
            'shortcuts/shortcutAction_E': [QtGui.QKeySequence(QtCore.Qt.Key_E)],
            'shortcuts/shortcutAction_I': [QtGui.QKeySequence(QtCore.Qt.Key_I)],
            'shortcuts/shortcutAction_O': [QtGui.QKeySequence(QtCore.Qt.Key_O)],
            'shortcuts/shortcutAction_P': [QtGui.QKeySequence(QtCore.Qt.Key_P)],
            'shortcuts/shortcutAction_V': [QtGui.QKeySequence(QtCore.Qt.Key_V)],
            'shortcuts/shortcutAction_0': [QtGui.QKeySequence(QtCore.Qt.Key_0)],
            'shortcuts/shortcutAction_1': [QtGui.QKeySequence(QtCore.Qt.Key_1)],
            'shortcuts/shortcutAction_2': [QtGui.QKeySequence(QtCore.Qt.Key_2)],
            'shortcuts/shortcutAction_3': [QtGui.QKeySequence(QtCore.Qt.Key_3)],
            'shortcuts/shortcutAction_4': [QtGui.QKeySequence(QtCore.Qt.Key_4)],
            'shortcuts/shortcutAction_5': [QtGui.QKeySequence(QtCore.Qt.Key_5)],
            'shortcuts/shortcutAction_6': [QtGui.QKeySequence(QtCore.Qt.Key_6)],
            'shortcuts/shortcutAction_7': [QtGui.QKeySequence(QtCore.Qt.Key_7)],
            'shortcuts/shortcutAction_8': [QtGui.QKeySequence(QtCore.Qt.Key_8)],
            'shortcuts/shortcutAction_9': [QtGui.QKeySequence(QtCore.Qt.Key_9)],
            'shortcuts/settingsExportItem': [],
            'shortcuts/songUsageReport': [],
            'shortcuts/songImportItem': [],
            'shortcuts/themeScreen': [QtGui.QKeySequence(QtCore.Qt.Key_T)],
            'shortcuts/toolsReindexItem': [],
            'shortcuts/toolsFindDuplicates': [],
            'shortcuts/toolsAlertItem': [QtGui.QKeySequence(QtCore.Qt.Key_F7)],
            'shortcuts/toolsFirstTimeWizard': [],
            'shortcuts/toolsOpenDataFolder': [],
            'shortcuts/toolsAddToolItem': [],
            'shortcuts/updateThemeImages': [],
            'shortcuts/up': [QtGui.QKeySequence(QtCore.Qt.Key_Up)],
            'shortcuts/viewProjectorManagerItem': [QtGui.QKeySequence(QtCore.Qt.Key_F6)],
            'shortcuts/viewThemeManagerItem': [QtGui.QKeySequence(QtCore.Qt.Key_F10)],
            'shortcuts/viewMediaManagerItem': [QtGui.QKeySequence(QtCore.Qt.Key_F8)],
            'shortcuts/viewPreviewPanel': [QtGui.QKeySequence(QtCore.Qt.Key_F11)],
            'shortcuts/viewLivePanel': [QtGui.QKeySequence(QtCore.Qt.Key_F12)],
            'shortcuts/viewServiceManagerItem': [QtGui.QKeySequence(QtCore.Qt.Key_F9)],
            'shortcuts/webSiteItem': []
        })

    def get_default_value(self, key):
        """
        Get the default value of the given key
        """
        if self.group():
            key = self.group() + '/' + key
        return AppSettings.__default_settings__[key]

    def remove_obsolete_settings(self):
        """
        This method is only called to clean up the config. It removes old settings and it renames settings. See
        ``__obsolete_settings__`` for more details.
        """
        for old_key, new_key, rules in AppSettings.__obsolete_settings__:
            # Once removed we don't have to do this again.
            if self.contains(old_key):
                if new_key:
                    # Get the value of the old_key.
                    old_value = super(AppSettings, self).value(old_key)
                    # When we want to convert the value, we have to figure out the default value (because we cannot get
                    # the default value from the central settings dict.
                    if rules:
                        default_value = rules[0][1]
                        old_value = self._convert_value(old_value, default_value)
                    # Iterate over our rules and check what the old_value should be "converted" to.
                    for new, old in rules:
                        # If the value matches with the condition (rule), then use the provided value. This is used to
                        # convert values. E. g. an old value 1 results in True, and 0 in False.
                        if callable(new):
                            old_value = new(old_value)
                        elif old == old_value:
                            old_value = new
                            break
                    self.setValue(new_key, old_value)
                self.remove(old_key)

    def value(self, key):
        """
        Returns the value for the given ``key``. The returned ``value`` is of the same type as the default value in the
        *Settings.__default_settings__* dict.

        :param key: The key to return the value from.
        """
        # if group() is not empty the group has not been specified together with the key.
        if self.group():
            default_value = AppSettings.__default_settings__[self.group() + '/' + key]
        else:
            default_value = AppSettings.__default_settings__[key]
        setting = super(AppSettings, self).value(key, default_value)
        return self._convert_value(setting, default_value)

    def _convert_value(self, setting, default_value):
        """
        This converts the given ``setting`` to the type of the given ``default_value``.

        :param setting: The setting to convert. This could be ``true`` for example.Settings()
        :param default_value: Indication the type the setting should be converted to. For example ``True``
        (type is boolean), meaning that we convert the string ``true`` to a python boolean.

        **Note**, this method only converts a few types and might need to be extended if a certain type is missing!
        """
        # Handle 'None' type (empty value) properly.
        if setting is None:
            # An empty string saved to the settings results in a None type being returned.
            # Convert it to empty unicode string.
            if isinstance(default_value, str):
                return ''
            # An empty list saved to the settings results in a None type being returned.
            else:
                return []
        # Convert the setting to the correct type.
        if isinstance(default_value, bool):
            if isinstance(setting, bool):
                return setting
            # Sometimes setting is string instead of a boolean.
            return setting == 'true'
        if isinstance(default_value, int):
            return int(setting)
        return setting

    def get_files_from_config(self, plugin):
        """
        This removes the settings needed for old way we saved files (e. g. the image paths for the image plugin). A list
        of file paths are returned.

         **Note**: Only a list of paths is returned; this does not convert anything!

         :param plugin: The Plugin object.The caller has to convert/save the list himself; o
        """
        files_list = []
        # We need QSettings instead of Settings here to bypass our central settings dict.
        # Do NOT do this anywhere else!
        settings = QtCore.QSettings(self.fileName(), AppSettings.IniFormat)
        settings.beginGroup(plugin.settings_section)
        if settings.contains('%s count' % plugin.name):
            # Get the count.
            list_count = int(settings.value('%s count' % plugin.name, 0))
            if list_count:
                for counter in range(list_count):
                    # The keys were named e. g.: "image 0"
                    item = settings.value('%s %d' % (plugin.name, counter), '')
                    if item:
                        files_list.append(item)
                    settings.remove('%s %d' % (plugin.name, counter))
            settings.remove('%s count' % plugin.name)
        settings.endGroup()
        return files_list
