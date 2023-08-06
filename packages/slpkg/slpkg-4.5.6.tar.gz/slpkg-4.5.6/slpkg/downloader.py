#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
from pathlib import Path
from urllib.parse import unquote
from typing import Union
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.progress_bar import ProgressBar


class Downloader(Configs, Utilities):
    """ Wget downloader. """

    def __init__(self, path: Union[str, Path], url: str, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.path = path
        self.url: str = url
        self.flags: list = flags

        self.color = self.colour()
        self.progress = ProgressBar()

        self.output: int = 0
        self.stderr = None
        self.stdout = None

        self.filename: str = url.split('/')[-1]
        self.bold: str = self.color['bold']
        self.green: str = self.color['green']
        self.yellow = self.color['yellow']
        self.red: str = self.color['red']
        self.blue: str = self.color['blue']
        self.endc: str = self.color['endc']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.bred: str = f'{self.bold}{self.red}'
        self.flag_no_silent: list = ['-n', '--no-silent']

    def transfer_tools(self) -> None:
        """ Downloader tools wget and curl. """
        if self.downloader == 'wget':
            self.output = subprocess.call(f'{self.downloader} {self.wget_options} --directory-prefix={self.path} '
                                          f'"{self.url}"', shell=True, stderr=self.stderr, stdout=self.stdout)
        elif self.downloader == 'curl':
            self.output = subprocess.call(f'{self.downloader} {self.curl_options} "{self.url}" --output '
                                          f'{self.path}/{self.filename}', shell=True, stderr=self.stderr,
                                          stdout=self.stdout)
        else:
            raise SystemExit(f"{self.red}Error:{self.endc} Downloader '{self.downloader}' not supported.\n")

        if self.output != 0:
            raise SystemExit(self.output)

    def check_if_downloaded(self) -> None:
        """ Checks if the file downloaded. """
        url: str = unquote(self.url)
        file: str = url.split('/')[-1]
        path_file = Path(self.path, file)

        if not path_file.exists():
            raise SystemExit(f"\n{self.red}FAILED {self.output}:{self.endc} '{self.blue}{self.url}{self.endc}' "
                             f"to download.\n")

    def download(self) -> None:
        """ Starting multiprocessing download process. """
        if self.silent_mode and not self.is_option(self.flag_no_silent, self.flags):

            done: str = f' {self.byellow} Done{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            message: str = f'[{self.green}Downloading{self.endc}]'

            # Starting multiprocessing
            p1 = Process(target=self.transfer_tools)
            p2 = Process(target=self.progress.bar, args=(message, self.filename))

            p1.start()
            p2.start()

            # Wait until process 1 finish
            p1.join()

            # Terminate process 2 if process 1 finished
            if not p1.is_alive():

                if p1.exitcode != 0:
                    done: str = f' {self.bred} Failed{self.endc}'
                    self.output: int = p1.exitcode

                print(f'{self.endc}{done}', end='')
                p2.terminate()

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h', self.endc)
        else:
            self.transfer_tools()

        self.check_if_downloaded()
