# -*- coding: utf8 -*-
"""watch-fs is a command line tool to run commands when files change."""

from __future__ import print_function, unicode_literals

import datetime
import subprocess

import click
import pyinotify


class Timer(object):
    """Call a function if a delay has passed since the last successful call."""

    @staticmethod
    def now():
        return datetime.datetime.now()

    def __init__(self, wait):
        self.wait = datetime.timedelta(seconds=wait)
        self.finished_at = self.now() - self.wait

    def ready(self):
        """Return True if ``wait`` has passed since ``finished_at``."""
        return (self.now() - self.finished_at) > self.wait

    def finished(self):
        """Reset ``finished_at``."""
        self.finished_at = self.now()


class WatchFS(object):
    """A timer and pyinotify setup to run a command when files change."""

    def __init__(self, directories, command, clear, show, verbose, wait,
                 mask=pyinotify.IN_CREATE | pyinotify.IN_MODIFY):
        self.directories = directories
        self.command = command
        self.clear = clear
        self.show = show
        self.verbose = verbose
        self.mask = mask
        self.timer = Timer(wait)

    def run(self):
        """Setup inotify to call run_command() on each event."""
        watch_manager = pyinotify.WatchManager()
        for d in self.directories:
            watch_manager.add_watch(d, self.mask, rec=True, auto_add=True)
        notifier = pyinotify.Notifier(
            watch_manager, default_proc_fun=self.maybe_run_command)
        self.run_command()
        notifier.loop()

    def maybe_run_command(self, event):
        """Run the command if the delay has passed."""
        if self.timer.ready():
            self.run_command()
            self.timer.finished()

    def run_command(self):
        if self.clear:
            click.clear()
        if self.show:
            click.secho('$ {0}'.format(self.command), fg='cyan')
        exit_code = subprocess.call(self.command, shell=True)
        if self.verbose:
            click.echo("! Command '{0}' exited [{1}]".format(
                self.command, exit_code))


@click.command()
@click.option(
    '--directory', '-d', 'directories', multiple=True, default=['.'],
    type=click.Path(dir_okay=True, file_okay=True, exists=True),
    help="A directory to watch for file changes - can be used multiple times, "
    "and defaults to the current directory.")
@click.option(
    '-c', '--clear/--no-clear', is_flag=True, default=True,
    help="Clear the terminal before running the command.")
@click.option(
    '-s', '--show/--no-show', is_flag=True, default=True,
    help="Show commands before runnning them.")
@click.option(
    '-v', '--verbose/--no-verbose', is_flag=True, default=False,
    help="Show exit codes.")
@click.option(
    '-w', '--wait', type=click.FLOAT, default=1,
    help="A minium wait between commands, in seconds.")
@click.argument('command', nargs=-1)
def main(command, **kwargs):
    """Click entry point for watch-fs."""
    WatchFS(command=' '.join(command), **kwargs).run()

if __name__ == '__main__':
    main()
