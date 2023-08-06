#!/usr/bin/python3
# -*- coding: utf-8 -*-

import locale
from dialog import Dialog
from pathlib import Path
from typing import Union

from slpkg.configs import Configs
from slpkg.views.version import Version

locale.setlocale(locale.LC_ALL, '')


class DialogBox(Configs):
    """ Class for dialog box"""

    def __init__(self):
        super(Configs).__init__()

        self.d = Dialog(dialog="dialog")
        self.d.set_background_title(f'{self.prog_name} {Version().version} - Software Package Manager')

    def checklist(self, text: str, title: str, height: int, width: int,
                  list_height: int, choices: list, packages: list):
        """ Display a checklist box. """
        if self.dialog:
            code, tags = self.d.checklist(text, title=title, height=height,  width=width,
                                          list_height=list_height, choices=choices)
        else:
            code: bool = False
            tags: list = packages

        return code, tags

    def mixedform(self, text: str, title: str, elements: list, height: int, width: int):
        """ Display a mixedform box. """
        if self.dialog:
            code, tags = self.d.mixedform(text=text, title=title, elements=elements,
                                          height=height, width=width, help_button=True)
        else:
            code: bool = False
            tags: list = elements

        return code, tags

    def msgbox(self, text: str, height: int, width: int):
        """ Display a message box. """
        if self.dialog:
            self.d.msgbox(text, height, width)

    def textbox(self, text: Union[str, Path], height: int, width: int):
        """ Display a text box. """
        if self.dialog:
            self.d.textbox(text, height, width)
