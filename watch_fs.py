"""watch-fs is a command line tool to run commands when files change"""

from __future__ import print_function

import datetime
import subprocess

import click
import pyinotify


@click.command()
@click.option(
    '--directory', '-d', 'directories', multiple=True, default=['.'],
    type=click.Path(dir_okay=True, file_okay=True, exists=True),
    help="A directory to watch for file changes - can be used multiple times, "
    "and defaults to the current directory.")
@click.option(
    '-c', '--clear', is_flag=True,
    help="Clear the terminal before running the command")
@click.option(
    '-w', '--wait', type=click.FLOAT, default=1,
    help="A minium wait before running the command again, in seconds")
@click.option(
    '-v', '--verbose', 'verbosity', count=True,
    help="-v prints commands before running, and -vv shows debug information")
@click.argument('command')
def main(directories, clear, wait, verbosity, command):
    WatchFS(directories, command, clear, wait, verbosity).run()


class Timer(object):
    """Calls a function if a delay has passed since the last successful call"""

    @staticmethod
    def now():
        return datetime.datetime.now()

    def __init__(self, wait):
        self.wait = datetime.timedelta(seconds=wait)
        self.finished_at = self.now() - self.wait

    def ready(self):
        """Returns True if .wait has passed since .finished_at"""
        return (self.now() - self.finished_at) > self.wait

    def finished(self):
        """Resets the finished_at attribute"""
        self.finished_at = self.now()


class WatchFS(pyinotify.ProcessEvent):
    def __init__(self, directories, command, clear, wait, verbosity,
                 mask=pyinotify.IN_CREATE | pyinotify.IN_MODIFY):
        self.directories = directories
        self.command = command
        self.clear = clear
        self.verbosity = verbosity
        self.mask = mask
        self.timer = Timer(wait)

    def run(self):
        """Setup inotify to call run_command() on each event"""
        watch_manager = pyinotify.WatchManager()
        for d in self.directories:
            watch_manager.add_watch(d, self.mask, rec=True, auto_add=True)
        notifier = pyinotify.Notifier(
            watch_manager, default_proc_fun=self.maybe_run_command)
        self.run_command()
        notifier.loop()

    def maybe_run_command(self, event):
        """Run the command *if* the delay has passed"""
        if self.timer.ready():
            self.say(2, '!', 'Ready, running command')
            self.run_command()
            self.timer.finished()
        else:
            self.say(2, '!', 'Not ready, skipping event')

    def run_command(self):
        if self.clear:
            subprocess.call('clear')
        self.say(1, '$', self.command)
        exit_code = subprocess.call(self.command, shell=True)
        self.say(2, "!", "Command '{}' exited with code {}".format(
                self.command, exit_code))

    def say(self, verbosity, *args, **kwargs):
        if self.verbosity >= verbosity:
            print(*args, **kwargs)

if __name__ == '__main__':
    main()
