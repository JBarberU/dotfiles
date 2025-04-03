from shutil import which as shutil_which
from os import (
    path as os_path,
    access as os_access,
    W_OK as os_W_OK,
)
from subprocess import Popen as subprocess_Popen


def has_binary(binary):
    '''Checks if the given binary is an existing executable
    '''
    return shutil_which(binary) is not None


def hasnt_binary(binary):
    '''Checks if the given binary is not an existing executable
    '''
    return not has_binary(binary)


def find_existing_base_dir(path):
    '''Finds the parth of a given path that exists
    '''
    if not os_path.isdir(path):
        return find_existing_base_dir(os_path.dirname(path))
    if os_path.exists(path):
        return path
    return find_existing_base_dir(os_path.dirname(path))


def can_write(path):
    '''Checks if the user can write to the given path
    '''
    return os_access(
        path
        if os_path.exists(path)
        else find_existing_base_dir(path),
        os_W_OK
    )


def unable_to_write(path):
    '''Negation of can_write
    '''
    return not can_write(path)


def run_command(cmd, needs_elevation, verbose=False):
    '''Runs the given command through subprocess
    '''
    if verbose:
        cmd_str = ' '.join(cmd)
        msg = (
            'Running command as root' if needs_elevation
            else 'Running command'
        )
        print(f'{msg}: {cmd_str}')
    with subprocess_Popen(cmd if not needs_elevation else ['sudo'] + cmd):
        pass


def select_option(message, options):
    '''
    Takes the given options, sorts them, shows a number and asks the user to
    pick one of them.
    '''
    opts = sorted(options)
    print(message + ''.join(
        f'\n{i}: {str(v)}' for i, v in enumerate(opts))
    )
    try:
        ans = input('Selection: ')
        selected = int(ans)
        if selected < 0 or selected >= len(opts):
            raise Exception('Index out of range!')
        return opts[selected]
    except ValueError as exc:
        raise Exception(f'{ans} is not a number') from exc
