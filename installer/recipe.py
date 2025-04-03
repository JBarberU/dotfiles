import os.path as os_path
from installer.util import (
    run_command, unable_to_write
)


class Target:
    '''Container for file operations that require a source and destination
    '''

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __str__(self):
        return f'{self.src} -> {self.dst}'


class Recipe:
    '''Container for installation process
    '''

    def __init__(self, dotfile_dir, home_dir, verbose=False):
        self.dotfile_dir = dotfile_dir
        self.home_dir = home_dir
        self.verbose = verbose

        self.binaries = []
        self.callbacks = []
        self.copies = []
        self.custom_commands = []
        self.files = []
        self.links = []
        self.new_dirs = []

    def create_dir(self, path, absolute=False):
        '''Add instruction to create a directory
        '''
        p = path if absolute else os_path.join(self.home_dir, path)
        self.new_dirs.append(p)

    def create_link(self, src, target, absolute=False):
        '''Add instruction to create a symbolic link
        '''
        src = os_path.join(self.dotfile_dir, src)
        dst = target if absolute else os_path.join(self.home_dir, target)
        self.links.append(Target(src, dst))

    def create_copy(self, src, target):
        '''Add instruction to copy a file
        '''
        src = os_path.join(self.dotfile_dir, src)
        dst = os_path.join(self.home_dir, target)
        self.copies.append(Target(src, dst))

    def create_file(self, path, absolute=False):
        '''Add instruction to create an empty file
        '''
        p = path if absolute else os_path.join(self.home_dir, path)
        self.files.append(p)

    def install_binaries(self, binaries):
        '''Add instruction to install a binary or list of binaries
        '''
        if isinstance(binaries, str):
            self.binaries.append(binaries)
        elif isinstance(binaries, list):
            self.binaries = self.binaries + binaries
        else:
            raise Exception('Expected list or string')

    def clone(self, repo, path):
        self.create_custom_commands([
            'sh', '-c', f'git clone {repo} {path}'
        ])

    def create_custom_commands(self, command):
        self.custom_commands.append(command)

    def run_code(self, callback):
        self.callbacks.append(callback)

    def dryrun(self):
        '''Print what would be done
        '''
        print('Installing binaries:\n'  + ''.join('- ' + str(v) + '\n' for v in self.binaries))
        print('Copying:\n'              + ''.join('- ' + str(v) + '\n' for v in self.copies))
        print(f'Running {len(self.callbacks)} callbacks')
        print('Running commands:\n'              + ''.join('- ' + str(v) + '\n' for v in self.custom_commands))
        print('Creating files:\n'       + ''.join('- ' + str(v) + '\n' for v in self.files))
        print('Linking:\n'              + ''.join('- ' + str(v) + '\n' for v in self.links))
        print('Creating directories:\n' + ''.join('- ' + str(v) + '\n' for v in self.new_dirs))

    def run(self):
        '''Run installation
        '''

        if self.binaries:
            run_command(
                cmd=['apt-get', 'install'] + self.binaries,
                needs_elevation=True,
                verbose=self.verbose
            )

        for target in self.copies:
            run_command(
                cmd=['cp', target.src, target.dst],
                needs_elevation=unable_to_write(target.dst),
                verbose=self.verbose
            )

        for file in self.files:
            run_command(
                cmd=['touch', file],
                needs_elevation=unable_to_write(file),
                verbose=self.verbose
            )


        for link in self.links:
            dst_path = os_path.dirname(link.dst)
            if not os_path.exists(dst_path):
                run_command(
                        cmd=['mkdir', '-p', dst_path],
                        needs_elevation=unable_to_write(dst_path),
                        verbose=self.verbose
                )

            if os_path.islink(link.dst):
                print(f'{link.dst} already exists, skipping')
                continue

            run_command(
                cmd=['ln', '-s', link.src, link.dst],
                needs_elevation=unable_to_write(link.dst),
                verbose=self.verbose
            )

        for directory in self.new_dirs:
            run_command(
                cmd=['mkdir', '-p', directory],
                needs_elevation=unable_to_write(directory),
                verbose=self.verbose
            )

        for command in self.custom_commands:
            run_command(
                cmd=command, needs_elevation=False, verbose=self.verbose
            )

        for callback in self.callbacks:
            callback()

    def do_if(self, condition):
        '''Returns self if condition evaluates to True, or an empty Dummy
        recipe otherwise
        '''
        return self if condition else Recipe('dummy_dotfiles', 'dummy_home')
