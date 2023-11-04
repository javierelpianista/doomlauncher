'''
A ProfileManager contains all the information about all the Profile objects
and manages them.
It is basically a dict of Profiles with some functionallity.
'''

from .profile import Profile

import os
import json
import subprocess

class RepeatedProfileError(ValueError):
    pass

class ProfileManager:
    def __init__(self):
        self.profiles = {}
        self.options = {}

        self.dir = os.path.join(
                os.path.expanduser('~'), '.config', 'doomlauncher')

        self.filename = os.path.join(self.dir, 'config.json')
        self.savedir = os.path.join(self.dir, 'saves')

        os.makedirs(self.savedir, exist_ok=True)
        os.makedirs(self.dir, exist_ok=True)

    def __getitem__(self, key):
        return self.profiles[key]

    def __setitem__(self, key, val):
        self.profiles[key] = val

    def __contains__(self, key):
        return key in self.profiles

    @classmethod
    def load(cls):
        '''
        Read the configuration file to load the profiles.
        '''

        mgr = ProfileManager()

        with open(mgr.filename, 'r') as read_file:
            data = json.load(read_file)

        for key, val in data.items():
            if key == 'Profiles':
                for name, profile in val.items():
                    mgr[name] = Profile(profile)

            else:
                mgr.options[key] = val

        return mgr

    def save(self):
        '''
        Save the configuration file.
        It is always saved in ~/.config/doomlauncher/config.json
        '''

        data = self.options
        data['Profiles'] = self.profiles

        with open(self.filename, 'w') as write_file:
            json.dump(data, write_file, indent=4)

    def list_profiles(self):
        return list(self.profiles)

    def add_profile(self, profile):

        if profile['name'] in self:
            raise RepeatedProfileError(
                    f'Profile {profile["name"]} is already in the database')

        self[profile['name']] = profile

    def run_command(self, profile_name, **kwargs):
        savedir = os.path.join(self.savedir, profile_name.replace(' ','_'))
        os.makedirs(savedir, exist_ok=True)

        additional_args = ['-save', savedir]

        command = self[profile_name].get_command_args(
                additional_args = additional_args, **kwargs)

        return command

