"""
watch-fs is a command line tool to run commands when files change
"""

import argparse
import datetime
import subprocess

import pyinotify

DEFAULT_INOTIFY_MASK = pyinotify.IN_CREATE | pyinotify.IN_MODIFY

parser = argparse.ArgumentParser(prog='watch-fs')
parser.add_argument(
    'command', help="the command to run when files change")
parser.add_argument(
    '-d', '--directory', action='append', metavar='DIR', dest='paths',
    help="a directory to watch")
parser.add_argument(
    '-D', '--delay', type=int, default=1,
    help="minimum seconds to wait before running the command again")
parser.add_argument(
    '-V', '--verbose', action='store_true',
    help="be more verbose")


class Timer(object):
    """Call a function if $delay has passed since the last call"""

    @staticmethod
    def now():
        return datetime.datetime.now()

    def __init__(self, delay, function):
        self.delay = datetime.timedelta(seconds=delay)
        self.function = function
        self.last_call = self.now() - self.delay

    def __call__(self, *args, **kwargs):
        if (self.now() - self.last_call) > self.delay:
            self.function(*args, **kwargs)
            self.last_call = self.now()


class Command(pyinotify.ProcessEvent):
    def __init__(self, command, verbose=False, delay=0.5):
        self.command = command
        self.verbose = verbose
        self.timer = Timer(delay, self.run_command)

    def run_command(self, event):
        if self.verbose:
            print("$ {}".format(self.command))
        command = self.command.format(name=event.name, path=event.pathname)
        exit_code = subprocess.call(command, shell=True)
        if self.verbose and exit_code:
            print("Command {} exited with code {}".format(
                self.command, exit_code))

    def process_default(self, event):
        if not event.dir:
            self.timer(event)


def main(mask=DEFAULT_INOTIFY_MASK):
    args = parser.parse_args()

    watch_manager = pyinotify.WatchManager()
    event_handler = Command(
        command=args.command, delay=args.delay, verbose=args.verbose)
    notifier = pyinotify.Notifier(watch_manager, event_handler)

    for path in (args.paths or ['.']):
        watch_manager.add_watch(path, mask, rec=True, auto_add=True)

    notifier.loop()

if __name__ == '__main__':
    main()
