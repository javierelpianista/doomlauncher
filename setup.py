# doomlauncher: a launcher for Doom games and mods
#
# Copyright (c) 2023-2023, Javier Garcia.
#
# This file is part of doomlauncher.
#
# doomlauncher is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# doomlauncher is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with
# doomlauncher. If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

packages = find_packages()

for pack in packages:
    print(pack)
setup(
        name = 'doomlauncher',
        version = '0.2',
        author = 'Javier Garcia', 
        long_description = 'No description for now',
        packages = packages,
        entry_points = {
            'gui_scripts' : [
                'doomlauncher = doomlauncher.main:main'
                ],
            'console_scripts' : [
                'dlaunch = doomlauncher.tui:main'
                ]
            },
        package_data = {'': 
            [
                'main.ui',
                'edit_profile.ui',
                ]
            },
        include_package_data=True,
        install_requires = [
            'PyQt5',
            'chardet'
        #    'importlib_resources',
        #    'fuzzywuzzy',
        #    'python-Levenshtein',
        #    'scidownl',
        #    'arxiv'
            ]
        )
