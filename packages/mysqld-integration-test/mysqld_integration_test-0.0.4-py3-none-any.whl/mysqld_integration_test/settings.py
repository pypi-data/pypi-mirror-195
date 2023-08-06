import os
import yaml
import sys
import tempfile

from mysqld_integration_test.version import __version__
from mysqld_integration_test.helpers import Utils

class Settings():

    def __init__(self, args):
        self.args = args

    def parse_config_file(configfile):
        config = ConfigFile()

        # See if there is a config file
        if os.path.exists(configfile):
            with open(configfile, "r", encoding='utf-8') as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

            # Merge config together with args
            if 'database' in cfg:
                if 'username' in cfg['database']:
                    config.database.username = cfg['database']['username']
                if 'password' in cfg['database']:
                    config.database.password = cfg['database']['password']
                if 'host' in cfg['database']:
                    config.database.host = cfg['database']['host']
                if 'port' in cfg['database']:
                    config.database.port = cfg['database']['port']
                if 'mysql_install_db_binary' in cfg['database']:
                    config.database.mysql_install_db_binary = cfg['database']['mysql_install_db_binary']
                if 'mysqld_binary' in cfg['database']:
                    config.database.mysqld_binary = cfg['database']['mysqld_binary']

            if 'general' in cfg:
                if 'timeout_start' in cfg['general']:
                    config.general.timeout_start = cfg['general']['timeout_start']
                if 'timeout_stop' in cfg['general']:
                    config.general.timeout_stop = cfg['general']['timeout_stop']
                if 'log_level' in cfg['general']:
                    config.general.log_level = cfg['general']['log_level']

        return config


class ConfigAttribute(object):
    pass

class ConfigFile():
    def __init__(self):
        _base_dir = default=tempfile.mkdtemp()

        self.dirs = ConfigAttribute()
        self.dirs.base_dir = _base_dir
        self.dirs.data_dir = os.path.join(_base_dir, 'var')
        self.dirs.etc_dir = os.path.join(_base_dir, 'etc')
        self.dirs.tmp_dir = os.path.join(_base_dir, 'tmp')

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

class ConfigInstance():
    def __init__(self):
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.socket_file = None

