from .profilemanager import ProfileManager
import argparse
import subprocess
import dmenu

parser = argparse.ArgumentParser(
        description = 'dlaunch: a terminal launcher for PrBoom+.'
        )

parser.add_argument(
        '-l', '--list', 
        help = 'List available profiles.',
        action = 'store_true'
        )

parser.add_argument(
        '-r', '--run',
        help = 'Run profile'
        )

parser.add_argument(
        '--run-last',
        help = 'Run the previously ran profile.',
        action = 'store_false'
        )

parser.add_argument(
        '--print-command',
        help = 'Print the console command used to run the profile.',
        action = 'store_true'
        )

def run_profile(mgr, profile_name, **kwargs):
    print('Running profile: ', profile_name)

    opts = {
            'print_command' : False
            }

    opts.update(kwargs)

    if profile_name not in mgr.profiles:
        raise ValueError(f'Profile {profile_name} not available. Run with the --list argument to see the available profiles.')
    
    mgr.options['last_profile'] = profile_name
    mgr.save()

    command = mgr.run_command(profile_name, print_commands = opts['print_command'])
    subprocess.run(command)


def list_profiles(mgr: ProfileManager):
    print('Profile list:')
    print('-------------')

    for profile in mgr.list_profiles():
        print(profile)

def run_dmenu():
    mgr = ProfileManager.load()

    profiles = mgr.list_profiles()
    profile_name = dmenu.show(profiles)

    run_profile(mgr, profile_name)

def main():
    args0 = parser.parse_args()
    print(args0)

    mgr = ProfileManager.load()

    if args0.list:
        list_profiles(mgr)

    elif args0.run is not None:
        profile_name = args0.run
        run_profile(mgr, profile_name)

    elif args0.run_last:
        if mgr.options['last_profile'] is None:
            print('No last profile.')
        else:
            run_profile(mgr, mgr.options['last_profile'])
