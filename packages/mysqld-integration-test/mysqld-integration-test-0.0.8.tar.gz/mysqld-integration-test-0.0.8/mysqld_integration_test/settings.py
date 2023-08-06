import os
import yaml
import sys
import tempfile
import functools

from mysqld_integration_test.version import __version__
from mysqld_integration_test.helpers import Utils

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


class Settings():
    def __init__(self, args):
        self.args = args

    @classmethod
    def parse_config(cls, config, config_args):
        args = {}
        args['database'] = [ 'username', 'password', 'host', 'port', 'mysql_install_db_binary', 'mysqld_binary' ]
        args['general'] = [ 'timeout_start', 'timeout_stop', 'log_level', 'config_file' ]

        # See if there is a config file
        if os.path.exists(config.general.config_file):
            with open(config.general.config_file, "r", encoding='utf-8') as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

            # Merge config together with args
            for section in args:
                for arg in args[section]:
                    if arg in cfg[section]:
                        # Set the value from the config file
                        rsetattr(config, f"{section}.{arg}", cfg[section][arg])

        # Merge in any class arguments
        for section in args:
            for arg in args[section]:
                if arg in config_args:
                    rsetattr(config, f"{section}.{arg}", config_args[arg])

        return config


class ConfigAttribute(object):
    pass


class ConfigFile():
    def __init__(self, base_dir):
        self.dirs = ConfigAttribute()
        self.dirs.base_dir = base_dir
        self.dirs.data_dir = os.path.join(self.dirs.base_dir, 'var')
        self.dirs.etc_dir = os.path.join(self.dirs.base_dir, 'etc')
        self.dirs.tmp_dir = os.path.join(self.dirs.base_dir, 'tmp')

        self.database = ConfigAttribute()
        self.database.host = "127.0.0.1"
        self.database.port = Utils.get_unused_port()
        self.database.username = 'root'
        self.database.password = 'root'
        self.database.socket_file = os.path.join(self.dirs.tmp_dir, 'mysql.sock')
        self.database.pid_file = os.path.join(self.dirs.tmp_dir, 'mysqld.pid')
        self.database.mysqld_binary = Utils.find_program('mysqld', ['bin', 'libexec', 'sbin'])
        self.database.mysql_install_db_binary = Utils.find_program('mysql_install_db', ['bin', 'scripts'])

        self.general = ConfigAttribute()
        self.general.timeout_start = 30
        self.general.timeout_stop = 30
        self.general.log_level = "INFO"
        self.general.config_file = 'mysqld-integration-test.cfg'


class ConfigInstance():
    def __init__(self):
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.socket_file = None

