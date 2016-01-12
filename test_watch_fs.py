"""Test the watch_fs module using click.testing"""

import watch_fs

import click.testing
import mock
import pytest


@pytest.fixture
def run():
    return lambda *args: click.testing.CliRunner().invoke(watch_fs.main, args)


@mock.patch('pyinotify.Notifier.loop')
class TestWatchFS(object):
    def test_debug_output(self, loop_mock, run):
        """Check the debug output"""
        result = run('-v', '--no-smile', 'echo', 'hello', 'world')
        assert result.output == (
            '$ echo hello world\n'
            '! Command \'echo hello world\' exited [0]\n'
        )

    def test_loop_called(self, loop_mock, run):
        run('echo')

        assert isinstance(loop_mock, mock.Mock)
        loop_mock.assert_called_once_with()

    def test_run_command(self, loop_mock, run, capfd):
        """Check that the echo command was run"""
        run('echo', 'hello', 'world')
        out, err = capfd.readouterr()
        assert out.strip() == 'hello world'
