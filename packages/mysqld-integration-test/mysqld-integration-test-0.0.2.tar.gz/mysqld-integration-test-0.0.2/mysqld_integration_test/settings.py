import os
import argparse
import yaml
import sys
import tempfile

from mysqld_integration_test.version import __version__
from mysqld_integration_test.helpers import Utils

class Settings():

    def __init__(self, args):
        self.args = args

    def parse_arguments(self):
        _base_dir = default=tempfile.mkdtemp()

        parser = argparse.ArgumentParser()
        parser.add_argument("--base-dir", help="Base directory", default=_base_dir)
        parser.add_argument("--data-dir", help="Data directory", default=os.path.join(_base_dir, 'var'))
        parser.add_argument("--etc-dir", help="Temp directory", default=os.path.join(_base_dir, 'etc'))
        parser.add_argument("--tmp-dir", help="Temp directory", default=os.path.join(_base_dir, 'tmp'))
        parser.add_argument("--socket-file", help="Socket File", default=os.path.join(_base_dir, 'tmp', 'mysql.sock'))
        parser.add_argument("--pid-file", help="PID File", default=os.path.join(_base_dir, 'tmp', 'mysqld.pid'))
        parser.add_argument("--mysql-install-db", help="mysql_install_db binary", default=Utils.find_program('mysql_install_db', ['bin', 'scripts']))
        parser.add_argument("--mysqld", help="mysqld binary", default=Utils.find_program('mysqld', ['bin', 'libexec', 'sbin']))
        parser.add_argument("--bind-address", help="MySQL Address to bind", default='127.0.0.1')
        parser.add_argument("--port", help="MySQL Port", default=Utils.get_unused_port())
        parser.add_argument("--username", help="MySQL Username", default='root')
        parser.add_argument("--password", help="MySQL Password", default='root')
        parser.add_argument("--timeout", help="Timeout in seconds to start up the database", default=30)

        parser.add_argument("-c", "--config", help="Config file", default=os.environ.get('PYWAY_CONFIG_FILE', '.pyway.conf'))
        parser.add_argument("-v", "--version", help="Version", action='store_true')

        args = parser.parse_args()

        # Display version if it exists
        if args.version:
            print(f"Version: {__version__}")
            sys.exit(1)

        return args
