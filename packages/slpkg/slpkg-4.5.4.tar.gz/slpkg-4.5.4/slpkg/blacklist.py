#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tomli
from pathlib import Path

from slpkg.configs import Configs
from slpkg.models.models import PonceTable
from slpkg.models.models import session as Session


class Blacklist(Configs):
    """ Reads and returns the blacklist. """

    def __init__(self):
        super(Configs, self).__init__()
        self.session = Session

    def packages(self) -> list:
        """ Reads the blacklist file. """
        toml_blacks, ponce_blacks = [], []
        file_toml = Path(self.etc_path, 'blacklist.toml')

        if self.ponce_repo:
            sbos: list = self.session.query(PonceTable.name).all()
            ponce_blacks: list = [sbo[0] for sbo in sbos]

        if file_toml.is_file():
            try:
                with open(file_toml, 'rb') as black:
                    toml_blacks = tomli.load(black)['blacklist']['packages']
            except tomli.TOMLDecodeError as error:
                raise SystemExit(f"\nValueError: {error}: in the configuration file "
                                 "'/etc/slpkg/blacklist.toml'\n")

        return toml_blacks + ponce_blacks
