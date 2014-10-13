"""watch-fs is a command line tool to run commands when files change"""

import datetime
import subprocess

import click
import pyinotify


@click.command()
@click.option(
    '--directory', '-d', 'directories',
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    help="A directory to watch for file changes - can be used multiple times, "
    "and defaults to the current directory.")
@click.option(
    '-f', '--first/--no-first', default=True,
    help="Run the command once before waiting for changes")
@click.option(
    '-c', '--clear/--no-clear', default=False,
    help="Clear the terminal before running the command")
@click.option(
    '-D', '--delay', type=click.FLOAT, default=1,
    help="Minium delay before running the command again, in seconds")
@click.option(
    '-v', '--verbose/--quiet', default=False,
    help="Echo commands and exit codes")
@click.argument('command')
def main(directories, clear, delay, first, verbose, command):
    WatchFS(directories, command, clear, delay, first, verbose=True).run()


class WatchFS(pyinotify.ProcessEvent):
    def __init__(self, directories, command,
                 clear=False, delay=0.5, first=True, verbose=True,
                 mask=pyinotify.IN_CREATE | pyinotify.IN_MODIFY):
        self.directories = directories or ['.']
        self.command = command
        self.first = first
        self.clear = clear
        # self.delay = delay
        self.verbose = verbose
        self.mask = mask

        self.timer = Timer(delay)

    def run(self):
        watch_manager = pyinotify.WatchManager()
        for d in self.directories:
            watch_manager.add_watch(d, self.mask, rec=True, auto_add=True)
        notifier = pyinotify.Notifier(watch_manager, self)

        if self.first:
            self.run_command()

        notifier.loop()

    def run_command(self):
        if self.clear:
            subprocess.call('clear')

        if self.verbose:
            print('$', self.command)

        exit_code = subprocess.call(self.command, shell=True)
        if self.verbose and exit_code:
            print("Command '{}' exited with code {}".format(
                self.command, exit_code))

    def process_default(self, event):
        if self.timer():
            self.run_command()


class Timer(object):
    """Call a function if $delay has passed since the last successful call"""

    @staticmethod
    def now():
        return datetime.datetime.now()

    def __init__(self, delay=1):
        self.delay = datetime.timedelta(seconds=delay)
        self.last_call = self.now() - self.delay

    def __call__(self):
        if (self.now() - self.last_call) > self.delay:
            self.last_call = self.now()
            return True
        return False

if __name__ == '__main__':
    main()
