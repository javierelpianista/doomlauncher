'''
A Profile object contains all the information required to run a Doom mod with
all the required options.

It does not hold information about itself, i.e., where it should be saved and
read from. This will be handled by the ProfileManager.
'''

class Profile(dict):

    def __init__(self, *args):
        super().__init__(*args)

        if not 'files' in self:
            self['files'] = []

        for what in ('skill', 'warp'):
            if not what in self:
                self[what] = None

        self.check()

    def check(self):
        '''
        Check if all the required entries are filled.
        '''

        for what in ['name', 'iwad', 'port']:
            if what not in self:
                raise ValueError(f'{what} should be in the profile file.')

    def get_command_args(self, additional_args, print_commands=False):
        '''
        Get a list of the arguments required to run this profile.
        '''

        command = [self['port'], '-iwad', self['iwad']]
        for arg in additional_args:
            command.append(arg)

        if len(self['files']) > 0:
            for file in self['files']:
                command.append('-file')
                command.append(file)

        if self['warp'] is not None:
            command.append('-warp')
            command.append(str(self['warp']))

        if self['skill'] is not None:
            print(self['skill'])
            command.append('-skill')
            command.append(str(self['skill']))

        if print_commands:
            print('profile: ', self)
            print('Commands: ', command)

        return command
