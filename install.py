#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import re
import subprocess
from pathlib import Path as pathlib_Path
import urllib.request
import zipfile
import argparse


class Distro:

    def __init__(self):
        self.distro = None
        self.version = None
        self.version_name = None

    def __str__(self):
        return f'{self.distro} {self.version} {self.version_name}'

def get_distro():
    ret = Distro()
    rel_file = '/etc/os-release'
    if not os.path.exists(rel_file):
        return ret
    with open(rel_file, 'r') as f:
        for l in f.readlines():
            if re.search('^VERSION_ID=', l):
                ret.version = l[len('VERSION_ID='):].replace('"','').strip()
            elif re.search('^VERSION_CODENAME=', l):
                ret.version_name = l[len('VERSION_CODENAME='):].replace('"','').strip()
            elif re.search('^NAME=', l):
                ret.distro = l[len('NAME='):].replace('"','').strip()

        return ret


REPO_PATH = os.path.realpath(os.path.dirname(__file__))
HOME_PATH = pathlib_Path.home()
VERBOSE = False
DISTRO = get_distro()


def find_existing_base_dir(path):
    '''Finds the parth of a given path that exists
    '''
    if not os.path.isdir(path):
        return find_existing_base_dir(os.path.dirname(path))
    if os.path.exists(path):
        return path
    return find_existing_base_dir(os.path.dirname(path))


def can_write(path):
    '''Checks if the user can write to the given path
    '''
    return os.access(
        path
        if os.path.exists(path)
        else find_existing_base_dir(path),
        os.W_OK
    )

def unable_to_write(path):
    '''Negation of can_write
    '''
    return not can_write(path)


def run_command(cmd, needs_elevation):
    '''Runs the given command through subprocess
    '''
    if VERBOSE:
        cmd_str = ' '.join(cmd)
        msg = (
            'Running command as root' if needs_elevation
            else 'Running command'
        )
        print(f'{msg}: {cmd_str}')
    with subprocess.Popen(cmd if not needs_elevation else ['sudo'] + cmd):
        pass


class Target:
    '''Container for file operations that require a source and destination
    '''

    def __init__(self, src, dst, absolute):
        self.src = os.path.join(REPO_PATH, src)
        self.dst = dst if absolute else os.path.join(HOME_PATH, dst)

    def __str__(self):
        return f'{self.src} -> {self.dst}'


class Recipe:
    '''Container for installation process
    '''

    def __init__(self):
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
        p = path if absolute else os.path.join(HOME_PATH, path)
        self.new_dirs.append(p)

    def create_link(self, src, target, absolute=False):
        '''Add instruction to create a symbolic link
        '''
        self.links.append(Target(src, target, absolute))

    def create_copy(self, src, target):
        '''Add instruction to copy a file
        '''
        self.copies.append(Target(src, target, False))

    def create_file(self, path, absolute=False):
        '''Add instruction to create an empty file
        '''
        p = path if absolute else os.path.join(HOME_PATH, path)
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
                needs_elevation=True
            )

        for target in self.copies:
            run_command(
                cmd=['cp', target.src, target.dst],
                needs_elevation=unable_to_write(target.dst)
            )

        for file in self.files:
            run_command(
                cmd=['touch', file],
                needs_elevation=unable_to_write(file)
            )


        for link in self.links:
            dst_path = os.path.dirname(link.dst)
            if not os.path.exists(dst_path):
                run_command(
                        cmd=['mkdir', '-p', dst_path],
                        needs_elevation=unable_to_write(dst_path)
                )

            if os.path.islink(link.dst):
                print(f'{link.dst} already exists, skipping')
                continue

            run_command(
                cmd=['ln', '-s', link.src, link.dst],
                needs_elevation=unable_to_write(link.dst)
            )

        for directory in self.new_dirs:
            run_command(
                cmd=['mkdir', '-p', directory],
                needs_elevation=unable_to_write(directory)
            )

        for command in self.custom_commands:
            run_command(cmd=command, needs_elevation=False)

        for callback in self.callbacks:
            callback()


r = Recipe()


def select_option(message, options):
    '''
    Do things
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


def install_cmus():
    r.create_dir('.config/cmus')
    r.create_link('cmus/rc', '.config/cmus/rc')

    r.install_binaries(['cmus'])


def install_git():
    r.create_link('git/gitignore', '.gitignore')
    r.create_link('git/gitconfig', '.gitconfig')

    r.install_binaries(['git'])


def install_irssi():
    r.create_link('irssi', '.irssi')
    r.create_copy('irssi/config.example', '.irssi/config')
    r.install_binaries(['irssi'])


def install_tmux():
    r.create_link('tmux/tmux.conf', '.tmux.conf')
    r.create_link('tmux/tmux_powerline.snap', '.tmux_powerline.snap')

    r.install_binaries(['tmux'])

    return
    r.create_custom_commands([
        'sh', '-c','''
        cd /tmp &&
        git clone "https://github.com/thewtex/tmux-mem-cpu-load.git" &&
        cd /tmp/tmux-mem-cpu-load &&
        mkdir build &&
        cd build &&
        cmake .. &&
        make -j &&
        sudo make install
        '''
    ])
    # # Build and install tmux-mem-cpy
    # if [[ -v $DRY_RUN ]]
    # then
        # echo "Downloading, building and installing tmux-mem-cpu-load"
    # else
        # echo not dry run
        # CURRENT_PATH="$(pwd)"

        # cd /tmp
        # git clone "https://github.com/thewtex/tmux-mem-cpu-load.git"
        # cd /tmp/tmux-mem-cpu-load
        # mkdir build
        # cd build
        # cmake ..
        # make -j
        # sudo make install

        # cd "$CURRENT_PATH"
    # fi
# }


def install_urxvt():
    r.create_link('xorg/Xresources', '.Xresources')
    if DISTRO.distro == 'Ubuntu':
        r.install_binaries(['rxvt-unicode'])
    elif DISTRO.distro == 'Debian':
        r.install_binaries(['rxvt-unicode-256color'])


def install_vim():
    r.create_link('vimfiles', '.vim')
    r.create_link('vimfiles/vimrc', '.vimrc')
    r.create_link('vimfiles/nvim', '.config/nvim/init.vim')

    r.install_binaries(['vim', 'exuberant-ctags', 'ack-grep'])


def install_zsh():
    r.create_dir('.bin')
    r.create_dir('.config/boop')
    r.create_file('.aliases')
    r.create_file('.paths')

    r.create_link('zsh/zshrc', '.zshrc')
    r.create_link('zsh/zsh_custom', '.zsh_custom')
    r.create_link('zsh/zsh_env', '.zsh_env')
    r.create_link('zsh/cheat_sheet', '.cheat_sheet')
    r.create_link('zsh/sh_functions''', '.sh_functions')
    r.create_link('zsh/oh-my-zsh', '.oh-my-zsh')
    r.create_link('zsh/zsh_paths', '.zsh_paths')
    r.create_link('bin', '.bin/dotbin')

    r.install_binaries(['zsh'])

    # echo "Add files/symlinks {good,bad}.wav to .config/boop in order for the boop command to work properly!"
    # echo "Run \"chsh -s $(which zsh)\" to set zsh as our default shell"


def install_xmonad():
    r.create_dir('shots')

    r.create_link('haskell/ghci', '.ghci')
    r.create_link('xmonad/xmonad.hs', '.xmonad/xmonad.hs')
    r.create_link('xmonad/xmobarrc', '.xmobarrc')
    r.create_link('conky/conkyrc', '.conkyrc')
    r.create_link('xorg/xinitrc', '.xinitrc')
    r.create_link('xorg/start-xmonad', '.xmonad/start-xmonad')
    r.create_link('rofi/config.rasi', '.config/rofi/config.rasi')
    r.create_link('rofi/gruvbox-purple.rasi', '.config/rofi/gruvbox-purple.rasi')
    r.create_link('xmonad/dunstrc', '.config/dunst/dunstrc')

    r.create_link('xorg/start-xmonad', '/usr/bin/stxmonad', absolute=True)
    r.create_link('xorg/keyboard.conf', '/etc/X11/xorg.conf.d/keyboard.conf', absolute=True)
    monitor_option = select_option(
        'Select monitor configuration file to use:',
        [f'xorg/{f}' for f in os.listdir(f'{REPO_PATH}/xorg') if 'monitor' in f]
    )
    r.create_link(monitor_option, '/etc/X11/xorg.conf.d/monitors.conf', absolute=True)

    r.create_dir('/usr/share/dotfiles/backgrounds', absolute=True)

    r.install_binaries(['xmonad', 'xmobar', 'rofi', 'conky-all', 'xclip', 'feh', 'dunst', 'xcompmgr', 'numlockx', 'xinput', 'scrot'])


def patch_kbd_layout():
    dst = '/usr/share/X11/xkb/symbols/us'
    patch_file = f'"{REPO_PATH}/kbdlayout/dvorak-intl.patch"'
    paths = f'{dst} {patch_file}'
    base_cmd = 'sudo patch --silent -p0'
    r.create_custom_commands([
        'sh', '-c',
        (
            # Test if the patch can be reversed, and if so skip the patch (by
            # using or between the operations
            f'{base_cmd} --reverse --force --dry-run {paths} || '
            f'{base_cmd} {paths}'
         )
    ])


def install_rando_tools():
    r.install_binaries([
        'curl',
        'python3-pip',
        'cmake',
        'valgrind',     # C/C++ profiler
        'gnome-clocks',
        'simple-scan',  # scanner application
        'oathtool',     # oath stuff
        'pavucontrol',  # audio mixer
        'fuse',         # needed for running AppImages
    ])

def download_file(url, path):
    request = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(request) as req:
        with open(path, 'wb') as file:
            file.write(req.read())


def install_fonts():
    print('installing fonts')

    def inst_fonts():
        # # Font Awesome
        zip_file = '/tmp/fontawesome5.zip'
        folder = '/tmp/fontawesome5'
        font_viewer = 'gnome-font-viewer'
        download_file(
            url='https://use.fontawesome.com/releases/v5.15.4/fontawesome-free-5.15.4-desktop.zip',
            path=zip_file
        )

        with zipfile.ZipFile(zip_file, 'r') as f:
            f.extractall(folder)

        os.remove(zip_file)

        awesome_out = f'{folder}_fonts'
        os.makedirs(awesome_out)

        c = 0
        for root, dirs, files in os.walk(folder):
            for f in files:
                if 'otf' in f:
                    shutil.copyfile(f'{root}/{f}', f'{awesome_out}/{c}.otf')
                    c = c + 1

        for file in os.listdir(awesome_out):
            full_path = f'{awesome_out}/{file}'
            run_command(
                cmd=[font_viewer, full_path],
                needs_elevation=False
            )

        run_command(['rm', '-r', folder], False)
        run_command(['rm', '-r', awesome_out], False)

        folder = '/tmp/dejavu_sans'
        os.makedirs(folder)

        download_file(url='https://github.com/powerline/fonts/blob/master/DejaVuSansMono/DejaVu%20Sans%20Mono%20Bold%20Oblique%20for%20Powerline.ttf?raw=true', path=f'{folder}/1.ttf')
        download_file(url='https://github.com/powerline/fonts/blob/master/DejaVuSansMono/DejaVu%20Sans%20Mono%20Bold%20for%20Powerline.ttf?raw=true', path=f'{folder}/2.ttf')
        download_file(url='https://github.com/powerline/fonts/blob/master/DejaVuSansMono/DejaVu%20Sans%20Mono%20Oblique%20for%20Powerline.ttf?raw=true', path=f'{folder}/3.ttf')
        download_file(url='https://github.com/powerline/fonts/blob/master/DejaVuSansMono/DejaVu%20Sans%20Mono%20for%20Powerline.ttf?raw=true', path=f'{folder}/4.ttf')

        for file in os.listdir(folder):
            full_path = f'{folder}/{file}'
            run_command(cmd=[
                font_viewer, full_path
            ], needs_elevation=False)

        run_command(['rm', '-r', folder], False)

    r.run_code(inst_fonts)


def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true', help='Installs everything')
    parser.add_argument('--cmus', action='store_true', help='Installs cmus')
    parser.add_argument('--fonts', action='store_true', help='Installs fonts')
    parser.add_argument('--git', action='store_true', help='Installs git')
    parser.add_argument('--irssi', action='store_true', help='Installs irssi')
    parser.add_argument('--kbd', action='store_true', help='Installs kbd')
    parser.add_argument('--tmux', action='store_true', help='Installs tmux')
    parser.add_argument('--tools', action='store_true', help='Installs tools')
    parser.add_argument('--urxvt', action='store_true', help='Installs urxvt')
    parser.add_argument('--vim', action='store_true', help='Installs vim')
    parser.add_argument('--xmonad', action='store_true', help='Installs xmonad')
    parser.add_argument('--zsh', action='store_true', help='Installs zsh')
    parser.add_argument('--dryrun', action='store_true', help='Prints all that will be done without making any changes')
    parser.add_argument('--verbose', action='store_true', help='Prints more stuff')
    args = parser.parse_args()

    if args.all:
        print('All')

    if args.cmus or args.all:
        install_cmus()

    if args.fonts or args.all:
        install_fonts()

    if args.git or args.all:
        install_git()

#    if args.irssi or args.all:
#        install_irssi()

    if args.kbd or args.all:
        patch_kbd_layout()

    if args.tmux or args.all:
        install_tmux()

    if args.tools or args.all:
        install_rando_tools()

    if args.urxvt or args.all:
        install_urxvt()

    if args.vim or args.all:
        install_vim()

    if args.xmonad or args.all:
        install_xmonad()

    if args.zsh or args.all:
        install_zsh()

    global VERBOSE
    VERBOSE = args.verbose

    if args.dryrun:
        r.dryrun()
    else:
        r.run()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
