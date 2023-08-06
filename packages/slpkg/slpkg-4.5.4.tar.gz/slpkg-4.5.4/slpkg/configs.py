#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tomli
import platform

from pathlib import Path
from dataclasses import dataclass


class LoadConfigs:
    @staticmethod
    def file(path: str, file: str) -> dict:
        try:
            """ Load the configs from the file. """
            config_path_file = Path(path, f'{file}.toml')
            if config_path_file.exists():
                with open(config_path_file, 'rb') as conf:
                    return tomli.load(conf)
        except tomli.TOMLDecodeError as error:
            raise SystemExit(f"\nValueError: {error}: in the configuration file "
                  "'/etc/slpkg/slpkg.toml'\n")


@dataclass
class Configs:
    """ Default configurations. """

    # Programme name.
    prog_name: str = 'slpkg'

    # OS architecture by default
    os_arch: str = platform.machine()

    # All necessary paths.
    tmp_path: str = '/tmp/'
    tmp_slpkg: str = Path(tmp_path, prog_name)
    build_path: str = Path('tmp', prog_name, 'build')
    download_only_path: str = Path(tmp_slpkg, '')
    lib_path: str = Path('/var/lib/', prog_name)
    etc_path: str = Path('/etc/', prog_name)
    db_path: str = Path(lib_path, 'database')
    sbo_repo_path: str = Path(lib_path, 'repository')
    log_packages: str = Path('/var', 'log', 'packages')

    # Database name.
    database_name: str = f'database.{prog_name}'

    # SBo repository configs.
    sbo_repo_url: str = 'https://slackbuilds.org/slackbuilds/15.0/'
    sbo_txt: str = 'SLACKBUILDS.TXT'
    sbo_chglog_txt: str = 'ChangeLog.txt'
    sbo_tar_suffix: str = '.tar.gz'
    sbo_repo_tag: str = '_SBo'

    # Ponce repo configs.
    ponce_repo: bool = False
    ponce_url: str = 'https://cgit.ponce.cc/slackbuilds/plain/'
    slack_current_mirror: str = 'https://mirrors.slackware.com/slackware/slackware64-current/'
    slack_chglog_txt: str = 'ChangeLog.txt'
    slack_chglog_path: str = Path('/var/lib/slpkg/repository/slack_current/')

    # Slackware commands.
    installpkg: str = 'upgradepkg --install-new'
    reinstall: str = 'upgradepkg --reinstall'
    removepkg: str = 'removepkg'

    # Cli menu colors configs.
    colors: bool = True

    # Dialog utility.
    dialog: bool = True

    # Downloader command. Wget and curl.
    downloader: str = 'wget'

    # Wget options.
    wget_options: str = '-c -N -q --show-progress'

    # Curl options.
    curl_options: str = ''

    # Lftp options'
    lftp_mirror_options: str = '-c mirror --delete-first --parallel=10'
    lftp_get_options: str = '-c get -e'

    # Choose the view mode.
    silent_mode: bool = True

    # Choose ascii characters.
    # If True use extended else basic.
    ascii_characters: bool = True

    # Load configurations from the file.
    load = LoadConfigs()
    configs = load.file(etc_path, prog_name)

    if configs:
        try:
            config = configs['CONFIGS']

            # OS architecture by default.
            os_arch: str = config['OS_ARCH']

            # All necessary paths.
            tmp_slpkg: str = config['TMP_SLPKG']
            build_path: str = config['BUILD_PATH']
            download_only_path: str = config['DOWNLOAD_ONLY_PATH']
            sbo_repo_path: str = config['SBO_REPO_PATH']

            # Database name.
            database_name: str = config['DATABASE_NAME']

            # SBo repository details.
            sbo_repo_url: str = config['SBO_REPO_URL']
            sbo_txt: str = config['SBO_TXT']
            sbo_chglog_txt: str = config['SBO_CHGLOG_TXT']
            sbo_tar_suffix: str = config['SBO_TAR_SUFFIX']
            sbo_repo_tag: str = config['SBO_REPO_TAG']

            # Ponce repo configs.
            ponce_repo: bool = config['PONCE_REPO']
            ponce_url: str = config['PONCE_URL']
            slack_current_mirror: str = config['SLACK_CURRENT_MIRROR']
            slack_chglog_txt: str = config['SLACK_CHGLOG_TXT']
            slack_chglog_path: str = config['SLACK_CHGLOG_PATH']

            # Slackware commands.
            installpkg: str = config['INSTALLPKG']
            reinstall: str = config['REINSTALL']
            removepkg: str = config['REMOVEPKG']

            # Cli menu colors configs.
            colors: bool = config['COLORS']

            # Dialog utility.
            dialog: str = config['DIALOG']

            # Downloader command.
            downloader: str = config['DOWNLOADER']

            # Wget options.
            wget_options: str = config['WGET_OPTIONS']

            # Curl options.
            curl_options: str = config['CURL_OPTIONS']

            # Lftp options.
            lftp_mirror_options: str = config['LFTP_MIRROR_OPTIONS']
            lftp_get_options: str = config['LFTP_GET_OPTIONS']

            # Choose the view mode.
            silent_mode: bool = config['SILENT_MODE']

            # Choose ascii characters. Extended or basic.
            ascii_characters: bool = config['ASCII_CHARACTERS']

        except KeyError as error:
            raise SystemExit(f"\nKeyError: {error}: in the configuration file '/etc/slpkg/slpkg.toml'.\n"
                             f"\nIf you have upgraded the '{prog_name}' probably you need to run:\n"
                             f"mv {etc_path}/{prog_name}.toml.new {etc_path}/{prog_name}.toml\n")

    # Creating the paths if not exists
    paths = [
        tmp_slpkg,
        build_path,
        download_only_path,
        sbo_repo_path,
        lib_path,
        etc_path,
        db_path,
        slack_chglog_path]

    for path in paths:
        if not os.path.isdir(path):
            os.makedirs(path)

    @classmethod
    def colour(cls) -> dict:
        color = {
            'bold': '',
            'red': '',
            'green': '',
            'yellow': '',
            'cyan': '',
            'blue': '',
            'grey': '',
            'violet': '',
            'endc': ''
        }

        if cls.colors:
            color = {
                'bold': '\033[1m',
                'red': '\x1b[91m',
                'green': '\x1b[32m',
                'yellow': '\x1b[93m',
                'cyan': '\x1b[96m',
                'blue': '\x1b[94m',
                'grey': '\x1b[38;5;247m',
                'violet': '\x1b[35m',
                'endc': '\x1b[0m'
            }

        return color
