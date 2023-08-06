#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
from typing import Union

from slpkg.queries import SBoQueries

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.models.models import SBoTable, PonceTable
from slpkg.models.models import session as Session


class CreateData(Configs):
    """ Reads the SLACKBUILDS.TXT file and inserts them into the database. """

    def __init__(self):
        super(Configs, self).__init__()

        self.session = Session
        self.utils = Utilities()
        self.query = SBoQueries('')

    def insert_sbo_table(self) -> None:
        """ Install the data for SBo repository. """
        sbo_tags = [
            'SLACKBUILD NAME:',
            'SLACKBUILD LOCATION:',
            'SLACKBUILD FILES:',
            'SLACKBUILD VERSION:',
            'SLACKBUILD DOWNLOAD:',
            'SLACKBUILD DOWNLOAD_x86_64:',
            'SLACKBUILD MD5SUM:',
            'SLACKBUILD MD5SUM_x86_64:',
            'SLACKBUILD REQUIRES:',
            'SLACKBUILD SHORT DESCRIPTION:'
        ]
        path = Path(self.sbo_repo_path, self.sbo_txt)
        sbo_file: list = self.read_file(path)

        cache: list = []  # init cache

        print('\nCreating the database... ', end='', flush=True)

        for i, line in enumerate(sbo_file, 1):

            for tag in sbo_tags:
                if line.startswith(tag):
                    line = line.replace(tag, '').strip()
                    cache.append(line)

            if (i % 11) == 0:
                data: str = SBoTable(name=cache[0], location=cache[1].split('/')[1],
                                     files=cache[2], version=cache[3],
                                     download=cache[4], download64=cache[5],
                                     md5sum=cache[6], md5sum64=cache[7],
                                     requires=cache[8], short_description=cache[9])
                self.session.add(data)

                cache: list = []  # reset cache after 11 lines

        print('Done')

        self.session.commit()

    def insert_ponce_blacklist_packages(self) -> None:
        """ Install data for ponce repository. """
        sbos: list = self.query.sbos()

        path = Path(self.slack_chglog_path, self.slack_chglog_txt)
        slack_chglog: list = self.read_file(path)

        for line in slack_chglog:

            # Clean the line from white spaces.
            line: str = line.strip()

            if re.findall('Added[.]', line):

                # Clean the line.
                line = re.sub(r'Added.|.txz:', '', line)
                pkg: str = line.split('/')[-1]

                # Split and get the name only.
                name = self.utils.split_installed_pkg(pkg)[0]

                if name in sbos:
                    data = PonceTable(name=name)
                    self.session.add(data)

            # Stop the date when the Slackware 15.0 released.
            if line == 'Wed Feb  2 22:22:22 UTC 2022':
                break

        self.session.commit()

    @staticmethod
    def read_file(file: Union[str, Path]) -> list:
        """ Reads the text file. """
        with open(file, 'r', encoding='utf-8') as f:
            return f.readlines()
