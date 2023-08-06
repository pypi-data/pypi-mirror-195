#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.downloader import Downloader
from slpkg.create_data import CreateData
from slpkg.models.models import SBoTable, PonceTable
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.check_updates import CheckUpdates
from slpkg.models.models import session as Session


class UpdateRepository(Configs):
    """ Deletes and install the data. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.session = Session

        self.progress = ProgressBar()
        self.color = self.colour()

        self.endc: str = self.color['endc']

    def sbo(self) -> None:
        """ Updated the sbo repository. """
        view = ViewMessage(self.flags)

        view.question()

        print('Updating the package list.\n')
        print('Downloading some necessary files, please wait...\n')
        self.delete_file(self.sbo_repo_path, self.sbo_txt)
        self.delete_file(self.sbo_repo_path, self.sbo_chglog_txt)
        self.delete_file(self.slack_chglog_path, self.slack_chglog_txt)

        self.delete_sbo_data()
        self.delete_ponce_data()

        slackbuilds_txt: str = f'{self.sbo_repo_url}{self.sbo_txt}'
        changelog_txt: str = f'{self.sbo_repo_url}{self.sbo_chglog_txt}'
        slack_changelog_txt: str = f'{self.slack_current_mirror}{self.slack_chglog_txt}'

        down_slackbuilds = Downloader(self.sbo_repo_path, slackbuilds_txt, self.flags)
        down_slackbuilds.download()

        down_sbo_changelog = Downloader(self.sbo_repo_path, changelog_txt, self.flags)
        down_sbo_changelog.download()

        if self.ponce_repo:
            down_slack_current_changelog = Downloader(self.slack_chglog_path, slack_changelog_txt, self.flags)
            down_slack_current_changelog.download()

        data = CreateData()
        data.insert_sbo_table()

        if self.ponce_repo:
            data.insert_ponce_blacklist_packages()

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
        """ Delete the table from the database. """
        self.session.query(SBoTable).delete()
        self.session.commit()

    def delete_ponce_data(self) -> None:
        """ Delete the table from the database. """
        if self.ponce_repo:
            self.session.query(PonceTable).delete()
        self.session.commit()
