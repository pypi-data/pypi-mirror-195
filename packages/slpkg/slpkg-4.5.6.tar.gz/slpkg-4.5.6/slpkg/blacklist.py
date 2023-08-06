#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tomli
from pathlib import Path

from slpkg.configs import Configs
from slpkg.models.models import session as Session


class Blacklist(Configs):
    """ Reads and returns the blacklist. """

    def __init__(self):
        super(Configs, self).__init__()
        self.session = Session

    def packages(self) -> list:
        """ Reads the blacklist file. """
        file_toml = Path(self.etc_path, 'blacklist.toml')

        if file_toml.is_file():
            try:
                with open(file_toml, 'rb') as black:
                    return tomli.load(black)['blacklist']['packages']
            except tomli.TOMLDecodeError as error:
                raise SystemExit(f"\nValueError: {error}: in the configuration file "
                                 "'/etc/slpkg/blacklist.toml'\n")
