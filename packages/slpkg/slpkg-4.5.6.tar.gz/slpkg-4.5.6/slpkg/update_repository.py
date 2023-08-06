#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
from pathlib import Path
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.install_data import CreateData
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.check_updates import CheckUpdates
from slpkg.models.models import session as Session
from slpkg.models.models import (Base, engine, SBoTable,
                                 PonceTable)


class UpdateRepository(Configs, Utilities):
    """ Deletes and install the data. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()

        self.flags: list = flags
        self.session = Session
        self.view = ViewMessage(self.flags)

        self.progress = ProgressBar()
        self.color = self.colour()

        self.endc: str = self.color['endc']
        self.flag_generate: list = ['-G', '--generate-only']

    def sbo(self) -> None:
        """ Updated the sbo repository. """
        self.view.question()

        if self.ponce_repo:

            if not self.is_option(self.flag_generate, self.flags):
                print('Updating the packages list.\n')
                print("Downloading the 'ponce' repository, please wait...\n")
                subprocess.call(f'lftp {self.lftp_mirror_options} {self.ponce_repo_url} {self.ponce_repo_path}',
                                shell=True)

            # Remove the SLACKBUILDS.TXT file before generating the new one.
            sbo_file_txt = Path(self.ponce_repo_path, self.ponce_txt)
            if sbo_file_txt.is_file():
                sbo_file_txt.unlink()

            # Generating the ponce SLACKBUILDS.TXT file.
            print(f'Generating the {self.ponce_txt} file... ', end='', flush=True)
            os.chdir(self.ponce_repo_path)
            subprocess.call(f'./gen_sbo_txt.sh > {self.ponce_txt}', shell=True)
            print()

        else:
            print('Updating the packages list.\n')
            self.delete_file(self.sbo_repo_path, self.sbo_txt)
            self.delete_file(self.sbo_repo_path, self.sbo_chglog_txt)

            slackbuilds_txt: str = f'{self.sbo_repo_url}{self.sbo_txt}'
            changelog_txt: str = f'{self.sbo_repo_url}{self.sbo_chglog_txt}'

            down_slackbuilds = Downloader(self.sbo_repo_path, slackbuilds_txt, self.flags)
            down_slackbuilds.download()

            down_sbo_changelog = Downloader(self.sbo_repo_path, changelog_txt, self.flags)
            down_sbo_changelog.download()

        self.delete_sbo_data()
        data = CreateData()
        data.install_sbo_table()

    def check(self) -> None:
        check_updates = CheckUpdates()
        if not check_updates.check():
            print(f'\n\n{self.endc}No changes in ChangeLog.txt between your last update and now.')
        else:
            print(f'\n\n{self.endc}There are new updates available!')

    def repository(self) -> None:
        """ Starting multiprocessing download process. """
        message = f'Checking for news in the Changelog.txt file...'

        # Starting multiprocessing
        p1 = Process(target=self.check)
        p2 = Process(target=self.progress.bar, args=(message, ''))

        p1.start()
        p2.start()

        # Wait until process 1 finish
        p1.join()

        # Terminate process 2 if process 1 finished
        if not p1.is_alive():
            p2.terminate()

        # Wait until process 2 finish
        p2.join()

        # Restore the terminal cursor
        print('\x1b[?25h', self.endc, end='')

        self.sbo()

    @staticmethod
    def delete_file(folder: str, txt_file: str) -> None:
        """ Delete the file. """
        file = Path(folder, txt_file)
        if file.exists():
            file.unlink()

    def delete_sbo_data(self) -> None:
        """ Delete all the data from a table of the database. """
        if self.ponce_repo:
            self.session.query(PonceTable).delete()
        else:
            self.session.query(SBoTable).delete()
        self.session.commit()

    def drop_the_tables(self):
        """ Drop all the tables from the database. """
        print('All the data from the database will be deleted.')
        self.view.question()

        tables: list = [PonceTable.__table__,
                        SBoTable.__table__]

        Base.metadata.drop_all(bind=engine, tables=tables)

        print("Successfully cleared!\n\nYou need to run 'slpkg update' now.")
