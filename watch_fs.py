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
    'command', help="The command to run when files change")
parser.add_argument(
    '-d', action='append', metavar='DIR', dest='paths',
    help="A directory to watch. Can be used more than once.")


class Timer(object):
    """Call a function if $delay has passed since the last call"""

    @staticmethod
    def now():
        return datetime.datetime.now()

    def __init__(self, delay, function):
        self.delay = datetime.timedelta(seconds=delay)
        self.function = function
        self.set_last_call_time()

    def set_last_call_time(self):
        self.last_call = self.now()

    def time_since_last_call(self):
        return self.now() - self.last_call

    def __call__(self, *args, **kwargs):
        if self.time_since_last_call() > self.delay:
            self.function(*args, **kwargs)
            self.set_last_call_time()


class Command(pyinotify.ProcessEvent):
    def __init__(self, command, delay=0.5):
        self.command = command
        self.timer = Timer(delay, self.run_command)

    def run_command(self, event):
        command = self.command.format(name=event.name, path=event.pathname)
        proccess = subprocess.Popen(command, shell=True)
        proccess.wait()

    def process_default(self, event):
        if not event.dir:
            self.timer(event)


def main(mask=DEFAULT_INOTIFY_MASK):
    args = parser.parse_args()

    watch_manager = pyinotify.WatchManager()
    event_handler = Command(args.command)
    notifier = pyinotify.Notifier(watch_manager, event_handler)

    for path in (args.paths or ['.']):
        watch_manager.add_watch(path, mask, rec=True, auto_add=True)

    notifier.loop()

if __name__ == '__main__':
    main()
