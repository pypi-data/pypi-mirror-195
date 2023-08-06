#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess
from typing import NoReturn

from pathlib import Path
from collections import OrderedDict
from multiprocessing import Process, cpu_count

from slpkg.checksum import Md5sum
from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.dependencies import Requires
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class Slackbuilds(Configs):
    """ Download build and install the SlackBuilds. """

    def __init__(self, slackbuilds: list, flags: list, file_pattern, mode: str):
        super(Configs, self).__init__()
        self.slackbuilds: list = slackbuilds
        self.flags: list = flags
        self.file_pattern: str = file_pattern
        self.mode: str = mode

        self.session = Session
        self.utils = Utilities()
        self.progress = ProgressBar()
        self.dialogbox = DialogBox()
        self.view_message = ViewMessage(self.flags)
        self.color = self.colour()

        self.install_order: list = []
        self.dependencies: list = []
        self.sbos: dict = {}
        self.output: int = 0
        self.stderr = None
        self.stdout = None
        self.process_message = None
        self.bold: str = self.color['bold']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.yellow: str = self.color['yellow']
        self.endc: str = self.color['endc']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.bred: str = f'{self.bold}{self.red}'
        self.flag_reinstall: list = ['-r', '--reinstall']
        self.flag_skip_installed: list = ['-k', '--skip-installed']
        self.flag_resolve_off: list = ['-o', '--resolve-off']
        self.flag_jobs: list = ['-j', '--jobs']
        self.flag_no_silent: list = ['-n', '--no-silent']

    def execute(self) -> None:
        """ Starting build or install the slackbuilds. """
        self.creating_dictionary()

        if not self.utils.is_option(self.flag_resolve_off, self.flags):
            self.creating_dependencies_for_build()

        self.creating_main_for_build()

        self.view_before_build()

        start: float = time.time()
        self.download_slackbuilds()
        self.build_and_install()
        elapsed_time: float = time.time() - start

        self.utils.finished_time(elapsed_time)

    def creating_dictionary(self) -> None:
        """ Dictionary with the main slackbuilds and dependencies. """
        for sbo in self.slackbuilds:
            self.sbos[sbo] = Requires(sbo).resolve()

    def creating_dependencies_for_build(self) -> None:
        """ List with the dependencies. """
        for deps in self.sbos.values():
            for dep in deps:

                # Checks if the package was installed and skipped.
                if (self.utils.is_option(self.flag_skip_installed, self.flags) and
                        self.utils.is_installed(dep, self.file_pattern)):
                    continue

                self.dependencies.append(dep)

        # Remove duplicate packages and keeps the order.
        dependencies = list(OrderedDict.fromkeys(self.dependencies))

        if dependencies:
            self.dependencies = self.choose_dependencies(dependencies)

            # Clean up the main packages if they were selected for dependencies
            for dep in self.dependencies:
                if dep in self.slackbuilds:
                    self.slackbuilds.remove(dep)

        self.install_order.extend(self.dependencies)

    def creating_main_for_build(self) -> None:
        """ List with the main slackbuilds. """
        [self.install_order.append(main) for main in self.sbos.keys() if main not in self.install_order]

    def view_before_build(self) -> None:
        """ View slackbuilds before proceed. """
        if not self.mode == 'build':
            self.view_message.install_packages(self.slackbuilds, self.dependencies, self.mode)
        else:
            self.view_message.build_packages(self.slackbuilds, self.dependencies)

        del self.dependencies  # no more needed

        self.view_message.question()

    def is_for_skipped(self, sbo) -> None:
        """ Condition to check if slackbuild is for skipped. """
        return (not self.utils.is_installed(sbo, self.file_pattern) or
                self.utils.is_package_upgradeable(sbo, self.file_pattern) or
                self.mode == 'build' or self.utils.is_option(self.flag_reinstall, self.flags))

    def download_slackbuilds(self) -> None:
        """ Downloads files and sources. """
        for sbo in self.install_order:

            if self.is_for_skipped(sbo):

                file: str = f'{sbo}{self.sbo_tar_suffix}'

                self.utils.remove_file_if_exists(self.tmp_slpkg, file)
                self.utils.remove_folder_if_exists(self.build_path, sbo)

                location = SBoQueries(sbo).location()
                sbo_url: str = f'{self.sbo_repo_url}{location}/{file}'
                ponce_url: str = f'{self.ponce_url}{location}/{sbo}'

                if self.ponce_repo:
                    path = Path(self.build_path, sbo)
                    lftp = Downloader(path, ponce_url, self.flags)
                    lftp.download()
                else:
                    down_sbo = Downloader(self.tmp_slpkg, sbo_url, self.flags)
                    down_sbo.download()

                    self.utils.untar_archive(self.tmp_slpkg, file, self.build_path)

                self.patch_sbo_tag(sbo)

                sources = SBoQueries(sbo).sources()
                self.download_sources(sbo, sources)

    def build_and_install(self) -> None:
        """ Build the slackbuilds and install. """
        for sbo in self.install_order:

            if self.is_for_skipped(sbo):

                self.build_the_script(self.build_path, sbo)

                if not self.mode == 'build':

                    pkg: str = self.creating_package_for_install(sbo)
                    self.install_package(pkg)

                    if not self.utils.is_option(self.flag_resolve_off, self.flags):
                        self.logging_installed_dependencies(sbo)
            else:
                package: str = self.utils.is_installed(sbo, self.file_pattern)
                version: str = self.utils.split_installed_pkg(package)[1]
                self.view_message.view_skipping_packages(sbo, version)

    def patch_sbo_tag(self, sbo: str) -> None:
        """ Patching SBo TAG from the configuration file. """
        sbo_script = Path(self.build_path, sbo, f'{sbo}.SlackBuild')

        if sbo_script.is_file():
            with open(sbo_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(sbo_script, 'w') as script:
                for line in lines:
                    if line.startswith('TAG=$'):
                        line: str = f'TAG=${{TAG:-{self.sbo_repo_tag}}}\n'
                    script.write(line)

    def logging_installed_dependencies(self, name: str) -> None:
        """ Logging installed dependencies and used for remove. """
        exist = self.session.query(LogsDependencies.name).filter(
            LogsDependencies.name == name).first()

        requires: list = Requires(name).resolve()

        # Update the dependencies if exist else create it.
        if exist:
            self.session.query(
                LogsDependencies).filter(
                    LogsDependencies.name == name).update(
                        {LogsDependencies.requires: ' '.join(requires)})

        elif requires:
            deps: list = LogsDependencies(name=name, requires=' '.join(requires))
            self.session.add(deps)
        self.session.commit()

    def install_package(self, package: str) -> None:
        """ Install the packages that before created in the tmp directory. """
        pkg: str = self.utils.split_installed_pkg(package)[0]

        execute: str = self.installpkg
        if (self.utils.is_option(self.flag_reinstall, self.flags) and
                self.utils.is_installed(pkg, self.file_pattern)):
            execute: str = self.reinstall

        message: str = f'{self.cyan}Installing{self.endc}'
        self.process_message: str = f"'{pkg}' to install"

        if self.mode == 'upgrade':
            self.process_message: str = f"package '{pkg}' to upgrade"
            message: str = f'{self.cyan}Upgrade{self.endc}'

        command: str = f'{execute} {self.tmp_path}{package}'

        self.multi_process(command, package, message)

    def creating_package_for_install(self, name: str) -> str:
        """ Creating a list with all the finished packages for
            installation. """
        version: str = SBoQueries(name).version()

        pattern: str = f'{name}-{version}*{self.sbo_repo_tag}*'

        tmp = Path(self.tmp_path)
        packages: list = [file.name for file in tmp.glob(pattern)]

        return max(packages)

    def build_the_script(self, path: str, name: str) -> None:
        """ Run the .SlackBuild script. """
        folder: str = f'{Path(path, name)}/'
        execute: str = f'{folder}./{name}.SlackBuild'

        # Change to root privileges
        os.chown(folder, 0, 0)
        for file in os.listdir(folder):
            os.chown(f'{folder}{file}', 0, 0)

        if self.utils.is_option(self.flag_jobs, self.flags):
            self.set_makeflags()

        name = f'{name}.SlackBuild'
        message: str = f'{self.red}Build{self.endc}'
        self.process_message: str = f"package '{name}' to build"

        self.multi_process(execute, name, message)

    @staticmethod
    def set_makeflags() -> None:
        """ Set number of processors. """
        os.environ['MAKEFLAGS'] = f'-j {cpu_count()}'

    def download_sources(self, name: str, sources: list) -> None:
        """ Download the sources. """
        path = Path(self.build_path, name)
        checksums: list = SBoQueries(name).checksum()

        for source, checksum in zip(sources, checksums):
            down_source = Downloader(path, source, self.flags)
            down_source.download()

            md5sum = Md5sum(self.flags)
            md5sum.check(path, source, checksum, name)

    def multi_process(self, command: str, filename: str, message: str) -> None:
        """ Starting multiprocessing install/upgrade process. """
        if self.silent_mode and not self.utils.is_option(self.flag_no_silent, self.flags):

            done: str = f' {self.byellow} Done{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            # Starting multiprocessing
            p1 = Process(target=self.process, args=(command,))
            p2 = Process(target=self.progress.bar, args=(f'[{message}]', filename))

            p1.start()
            p2.start()

            # Wait until process 1 finish
            p1.join()

            # Terminate process 2 if process 1 finished
            if not p1.is_alive():

                if p1.exitcode != 0:
                    done: str = f' {self.bred} Failed{self.endc}'
                    self.output = p1.exitcode

                print(f'{self.endc}{done}', end='')
                p2.terminate()

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h', self.endc)
        else:
            self.process(command)

        self.print_error()

    def process(self, command: str) -> NoReturn:
        """ Processes execution. """
        self.output = subprocess.call(command, shell=True,
                                      stderr=self.stderr, stdout=self.stdout)
        if self.output != 0:
            raise SystemExit(self.output)

    def print_error(self) -> NoReturn:
        """ Stop the process and print the error message. """
        if self.output != 0:
            raise SystemExit(f"\n{self.red}FAILED {self.output}:{self.endc} {self.process_message}.\n")

    def choose_dependencies(self, dependencies: list) -> list:
        """ Choose packages for install. """
        height: int = 10
        width: int = 70
        list_height: int = 0
        choices: list = []
        title: str = ' Choose dependencies you want to install '

        for package in dependencies:
            status: bool = False
            repo_ver = SBoQueries(package).version()
            self.utils.is_package_upgradeable(package, self.file_pattern)

            if self.mode == 'upgrade' and self.utils.is_package_upgradeable(package, self.file_pattern):
                status: bool = True

            if self.mode == 'install' and not self.utils.is_installed(package, self.file_pattern):
                status: bool = True

            if self.mode == 'install' and self.utils.is_package_upgradeable(package, self.file_pattern):
                status: bool = True

            choices += [(package, repo_ver, status)]

        text: str = f'There are {len(choices)} dependencies:'

        code, tags = self.dialogbox.checklist(text, title, height, width,
                                              list_height, choices, dependencies)

        if not code:
            return dependencies

        os.system('clear')

        return tags
