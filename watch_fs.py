"""
watch-fs is a command line tool to run commands when files change
"""

import argparse
import subprocess

import pyinotify

DEFAULT_INOTIFY_MASK = pyinotify.IN_CREATE | pyinotify.IN_MODIFY

parser = argparse.ArgumentParser(prog='watch-fs')
parser.add_argument(
    'command', help="The command to run when files change")
parser.add_argument(
    '-d', action='append', metavar='DIR',
    help="A directory to watch. Can be used more than once.")

class Command(object):
    def __init__(self, command):
        self.command = command

    def __call__(self, event):
        if event.dir:
            return
        command = self.command.format(name=event.name, path=event.pathname)
        proccess = subprocess.Popen(command, shell=True)
        proccess.wait()

def main(mask=DEFAULT_INOTIFY_MASK):
    args = parser.parse_args()

    watch_manager = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(watch_manager, Command(args.command))

    for path in (args.path or ['.']):
        watch_manager.add_watch(path, mask, rec=True, auto_add=True)

    notifier.loop()

if __name__ == '__main__':
    main()
