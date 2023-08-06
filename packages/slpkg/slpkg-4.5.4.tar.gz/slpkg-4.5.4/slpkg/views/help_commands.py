#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs


class Help(Configs):

    def __init__(self, command: str, flags: list):
        super(Configs, self).__init__()
        self.command: str = command
        self.flags: list = flags

        color = self.colour()

        self.bold: str = color['bold']
        self.green: str = color['green']
        self.cyan: str = color['cyan']
        self.yellow: str = color['yellow']
        self.endc: str = color['endc']

    def view(self) -> None:
        self.flags.reverse()  # Put first the short options.

        help_commands: dict = {
            'update': "Updates the package list and the database.",
            'upgrade': "Upgrade all the installed packages if the newer version exists in the repository.",
            'check-updates': "Check if there is any news on the SlackBuild's ChangeLog.txt file.",
            'configs': "Edit the configuration /etc/slpkg/slpkg.toml file.",
            'clean-logs': "Cleans dependencies log tracking. After that procedure you should remove dependencies "
                          "by hand.",
            'clean-tmp': "Deletes all the downloaded SlackBuilds scripts and sources.",
            'build': "Builds the Slackbuilds scripts and adds them to the /tmp directory.",
            'install': "Builds and installs the packages in the correct order, and also logs the packages with the "
                       "dependencies for removal.",
            'download': "Download the SlackBuilds scripts and the sources without building or installing it.",
            'remove': "Removes packages with dependencies if the packages was installed with 'slpkg install' method. "
                      "Slpkg looks at the 'sbo_repo_tag' configuration to find packages for removal by default, except "
                      "if you are using '--file-pattern=' option.",
            'find': "Find your installed packages on your system.",
            'view': "View information packages from the repository and get everything in your terminal.",
            'search': "Search and match packages from the repository.",
            'dependees': "Show which SlackBuilds depend on.",
            'tracking': "Tracking the packages dependencies."
        }

        help_commands['-u']: dict = help_commands['update']
        help_commands['-U']: dict = help_commands['upgrade']
        help_commands['-c']: dict = help_commands['check-updates']
        help_commands['-g']: dict = help_commands['configs']
        help_commands['-L']: dict = help_commands['clean-logs']
        help_commands['-D']: dict = help_commands['clean-tmp']
        help_commands['-b']: dict = help_commands['build']
        help_commands['-i']: dict = help_commands['install']
        help_commands['-d']: dict = help_commands['download']
        help_commands['-r']: dict = help_commands['remove']
        help_commands['-f']: dict = help_commands['find']
        help_commands['-w']: dict = help_commands['view']
        help_commands['-s']: dict = help_commands['search']
        help_commands['-e']: dict = help_commands['dependees']
        help_commands['-t']: dict = help_commands['tracking']

        print(f'\n{self.bold}{self.green}Help: {self.endc}{help_commands[self.command]}\n')
        print(f"{self.bold}COMMAND{self.endc}: {self.cyan}{self.command}{self.endc}")
        print(f"{self.bold}OPTIONS:{self.endc} {self.yellow}{', '.join(self.flags)}{self.endc}\n")
        print('If you need more information try to use slpkg manpage.\n')
