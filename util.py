#!/usr/bin/env python

import json
import sys
import os
import shutil
import time
import argparse
import subprocess
import threading
import stat
import logging

#-------------------------------------------------------------------------------

class Platforms:
    """Enum class for easily checking agains what platform we are running on."""
    UNDEFINED   = 0
    WINDOWS     = 1
    CYGWIN      = 2
    LINUX       = 3
    OSX         = 4

#-------------------------------------------------------------------------------

def get_current_platform():
    """Return the current platform."""
    for k, v in {
                    Platforms.WINDOWS:  ['win32'],
                    Platforms.CYGWIN:   ['cygwin'],
                    Platforms.OSX:      ['darwin'],
                    Platforms.LINUX:    ['linux', 'linux2'],
                }.iteritems():
        if sys.platform in v:
            return k
    return Platforms.UNDEFINED

#-------------------------------------------------------------------------------

def is_executable(path):
    """Return True if the path points to an executable."""
    return os.path.isfile(path) and os.stat(path).st_mode & stat.S_IXOTH

#-------------------------------------------------------------------------------

DOTFILES_PATH = os.path.abspath(os.path.dirname(__file__))
HOME_PATH = os.path.expanduser('~')
PLATFORM = get_current_platform()

#-------------------------------------------------------------------------------

def install():
    """Install the dotfiles."""
    recipes = None
    with open('{0}/recipes.json'.format(os.path.dirname(__file__)), 'r') as f:
        recipes = json.load(f)

    if not recipes:
        print 'Unable to read recipes'
        exit(1)

    platform = {
        Platforms.LINUX:     'linux',
        Platforms.OSX:       'osx',
        Platforms.WINDOWS:   'windows',
        Platforms.CYGWIN:    'windows',
        Platforms.UNDEFINED: None,
    }[PLATFORM]

    if not platform:
        print 'Attemting to run on unsupported platform, do you still want to continue?'
        ans = sys.stdin.readline()
        if 'yes' in ans.lower():
            print 'If anything catches fire, you\'re on your own 8]'
            print 'Cancel now if you changed your mind'
            for _ in range(0, 6):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(1)
        else:
            print 'Aborting'
            exit(1)

    def handle_binaries(recipe):
        if 'binaries' in recipe:
            bin_l = []
            man_bin_l = []
            b_bin_l = []
            for binary in recipe['binaries']:
                if type(binary) == dict:
                    is_exec = is_executable(binary['name'])
                    if not is_exec:
                        split_char = ';' if PLATFORM == Platforms.WINDOWS else ':'
                        for p in os.environ['PATH'].split(split_char):
                            if is_executable('{0}/{1}'.format(p, binary['name'])):
                                is_exec = True
                                break
                    if not is_exec:
                        t = binary['type']
                        if t == 'manual':
                            man_bin_l.append(binary)
                        elif 'ignore_platforms' in binary and platform not in binary['ignore_platforms']:
                            b_bin_l.append(binary)
                else:
                    bin_l.append(binary)
            return (bin_l, man_bin_l, b_bin_l)
    
    def handle_mkdirs(recipe):
        if 'mkdirs' in recipe:
            for dir_ in recipe['mkdirs']:
                d = '{0}/{1}'.format(HOME_PATH, dir_)
                if os.path.exists(d):
                    if not os.path.isdir(d):
                        sys.stderr.write('Unable to create folder {0}, a file with the same name already exists\n'.format(d))
                        exit(1)
                else:
                    os.makedirs(d)
    def handle_touch(recipe):
        if 'touch' in recipe:
            for file_ in recipe['touch']:
                f = '{0}/{1}'.format(HOME_PATH, file_)
                if not os.path.exists(f):
                    with open(f, 'w'):
                        pass

    def handle_links(recipe):
        if 'links' in recipe:
            for src_n, dst_n in recipe['links'].iteritems():
                src = '{0}/{1}'.format(DOTFILES_PATH, src_n)
                dst = '{0}/{1}'.format(HOME_PATH, dst_n)
                if os.path.exists(dst):
                    if not os.path.islink(dst):
                        sys.stderr.write('Unable to create symlink to {0}, a file/directory already exists at that location'.format(dst))
                    elif os.readlink(dst) != src:
                        sys.stderr.write('Conflicting symlink on $HOME\n')
                        exit(1)
                else:
                    os.symlink(src, dst)

    def handle_copy(recipe):
        if 'copy' in recipe:
            for src_n, dst_n in recipe['copy'].iteritems():
                src = '{0}/{1}'.format(DOTFILES_PATH, src_n)
                dst = '{0}/{1}'.format(HOME_PATH, dst_n)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                elif os.path.isfile(src):
                    shutil.copyfile(src, dst)
                else:
                    sys.stderr.write('Asked to copy unsupported filetype')

    binaries = []
    manual_binaries = []
    build_binaries = []
    messages = []
    for key, recipe in recipes.iteritems():
        if 'platforms' not in recipe or platform in recipe['platforms']:
            bin_, man_bin, b_bin = handle_binaries(recipe)
            if bin_:
                binaries = binaries + bin_
            if man_bin:
                manual_binaries = manual_binaries + man_bin
            if b_bin:
                build_binaries = build_binaries + b_bin


            handle_mkdirs(recipe)
            handle_touch(recipe)
            handle_links(recipe)
            handle_copy(recipe)
            if 'message' in recipe:
                messages.append(recipe['message'])
        else:
            print 'Ignoring {0} for platform {1}'.format(key, platform)

    def kill_sudo():
        subprocess.Popen(args=['sudo', '-k'], stdout=open(os.devnull, 'wb')).wait()

    class NopProcess:
        returncode = 0
        def wait(self):
            pass

    cleanup = lambda: None
    if binaries:
        p = NopProcess()

        if PLATFORM == Platforms.LINUX:
            cleanup = kill_sudo
            p = subprocess.Popen(args=['sudo', 'apt-get', 'install'] + binaries, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif PLATFORM == Platforms.OSX:
            p = subprocess.Popen(args=['brew', 'install'] + binaries, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif PLATFORM == Platforms.WINDOWS:
            manual_binaries = [{'name': b, 'message': '{0} has to be installed manually'.format(b)} for b in binaries]

        p.wait()
        if p.returncode:
            print 'Failed to install some packages, aborting'
            while True:
                line = p.stderr.readline()
                if not line:
                    break
                print line

            cleanup()
            exit(1)

        cleanup()

        for bb in build_binaries:
            with open(os.devnull, 'wb') as dnull:
                cwd = '/tmp'
                url = bb['url']
                repo_name = url.split('/')[-1]
                repo = '{0}/{1}'.format(cwd, repo_name)
                if not os.path.exists(repo):
                    p = subprocess.Popen(['git', 'clone', url, repo_name], stdout=dnull, stderr=subprocess.PIPE, cwd=cwd)
                    print 'Fetching code'
                    while True:
                        l = p.stderr.readline()
                        if not l:
                            break
                        sys.stdout.write('.')
                        sys.stdout.flush()
                    sys.stdout.write('\n')

                    p.wait()
                    logger = logging.getLogger()
                    if p.returncode:
                        logger.error('Failed to clone repo {}'.format(url))
                        exit(1)


                build_cwd = '{0}/{1}'.format(repo, bb['cwd'])
                if not os.path.exists(build_cwd):
                    os.makedirs(build_cwd)
                for cmd in bb['commands']:
                    p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, cwd=build_cwd)
                    print 'Running command: {0}'.format(cmd)
                    while True:
                        l = p.stdout.readline()
                        if not l:
                            break
                        sys.stdout.write('.')
                        sys.stdout.flush()
                    sys.stdout.write('\n')

                    p.wait()
                    if p.returncode:
                        logger.error('Failed to run command {0}'.format(cmd))
                        exit(1)

    if manual_binaries:
        binaries_msg = '\n'.join(['>\t{0}: {1}'.format(mb['name'], mb['message']) for mb in manual_binaries])
        print "You'll have to install the following binaries manually:\n{0}".format(binaries_msg)
    if messages:
        print 'Messages: \n{0}'.format('\n'.join(messages))

#-------------------------------------------------------------------------------

def update_vim_plugins():
    """Update the vim plugins by recursively running:
            $ git checkout master
            $ git pull --rebase origin master
            $ git submodule update --init --recursive
    """

    class PluginUpdater(threading.Thread):
        """Runner for the update of a plugin"""
        plugin_dir = ''

        def __init__(self, plugin_dir):
            self.plugin_dir = plugin_dir
            threading.Thread.__init__(self)

        def run(self):
            commands = [
                ['git', 'checkout', 'master'],
                ['git', 'pull', '--rebase', 'origin', 'master'],
                ['git', 'submodule', 'update', '--init', '--recursive'],
            ]
            with open(os.devnull, 'wb') as dnull:
                for cmd in commands:
                    subprocess.Popen(args=cmd,
                                     stdout=dnull,
                                     stderr=dnull,
                                     cwd=self.plugin_dir
                                    ).wait()
            sys.stdout.write('.')
            sys.stdout.flush()

    bundle_dir = '{0}/vim/vim/bundle'.format(DOTFILES_PATH)
    workers = []
    for d_iter in os.listdir(bundle_dir):
        plugin_dir = '{0}/{1}'.format(bundle_dir, d_iter)
        if not os.path.isdir(plugin_dir):
            continue

        t = PluginUpdater(plugin_dir)
        t.start()
        workers.append(t)
    
    for w in workers:
        w.join()

    print ' Done!'

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    if PLATFORM == Platforms.WINDOWS:
        sys.stderr.write('Win32 is currently explicitly unsupported, try using cygwin instead')
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('--install', '-i', action='store_true', help='Installs the dotfiles')
    parser.add_argument('--update-vim-plugins', '--uvp', action='store_true', help='Updates all vim plugins')
    args = parser.parse_args()
    if args.install:
        install()
    elif args.update_vim_plugins:
        update_vim_plugins()
    else:
        print 'Nothing to do, see --help for options'
        exit(1)
