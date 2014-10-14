"""watch-fs is a command line tool to run commands when files change"""

import datetime
import subprocess

import click
import pyinotify


@click.command()
@click.option(
    '--directory', '-d', 'directories', multiple=True, default=['.'],
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    help="A directory to watch for file changes - can be used multiple times, "
    "and defaults to the current directory.")
@click.option(
    '-c', '--clear/--no-clear', default=False,
    help="Clear the terminal before running the command")
@click.option(
    '-D', '--delay', type=click.FLOAT, default=0.5,
    help="Minium delay before running the command again, in seconds")
@click.option(
    '-v', '--verbose/--quiet', default=False,
    help="Echo commands and exit codes")
@click.argument('command')
def main(directories, clear, delay, verbose, command):
    WatchFS(directories, command, clear, delay, verbose=True).run()


class Timer(object):
    """Call a function if $delay has passed since the last successful call"""

    @staticmethod
    def now():
        return datetime.datetime.now()

    def __init__(self, delay):
        self.delay = datetime.timedelta(seconds=delay)
        self.finished_at = self.now() - self.delay

    def ready(self):
        """Returns True if .delay has passed since .finished_at"""
        return (self.now() - self.finished_at) > self.delay

    def finished(self):
        """Resets the finished_at attribute"""
        self.finished_at = self.now()


class WatchFS(pyinotify.ProcessEvent):
    def __init__(self, directories, command, clear, delay, verbose,
                 mask=pyinotify.IN_CREATE | pyinotify.IN_MODIFY):
        self.directories = directories
        self.command = command
        self.clear = clear
        self.verbose = verbose
        self.mask = mask
        self.timer = Timer(delay)

    def run(self):
        """Setup inotify to call run_command() on each event"""
        watch_manager = pyinotify.WatchManager()
        for d in self.directories:
            watch_manager.add_watch(d, self.mask, rec=True, auto_add=True)
        notifier = pyinotify.Notifier(
            watch_manager, default_proc_fun=self.maybe_run_command)
        self.run_command()
        notifier.loop()

    def maybe_run_command(self, event=None):
        """Run the command *if* the delay has passed"""
        if self.timer.ready():
            self.run_command()
            self.timer.finished()

    def run_command(self, event=None):
        if self.clear:
            subprocess.call('clear')

        if self.verbose:
            print('$', self.command)

        exit_code = subprocess.call(self.command, shell=True)
        if self.verbose and exit_code:
            print("! Command '{}' exited with code {}".format(
                self.command, exit_code))

if __name__ == '__main__':
    main()
