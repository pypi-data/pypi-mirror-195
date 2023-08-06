from mysql_integration_test.log import logger

SEARCH_PATHS = ['/usr/local/mysql']

class Mysqld():

   def initialize(self):
        self.my_cnf = self.settings.get('my_cnf', {})
        self.my_cnf.setdefault('socket', os.path.join(self.base_dir, 'tmp', 'mysql.sock'))
        self.my_cnf.setdefault('datadir', os.path.join(self.base_dir, 'var'))
        self.my_cnf.setdefault('pid-file', os.path.join(self.base_dir, 'tmp', 'mysqld.pid'))
        self.my_cnf.setdefault('tmpdir', os.path.join(self.base_dir, 'tmp'))

        self.mysql_install_db = self.settings.get('mysql_install_db')
        if self.mysql_install_db is None:
            self.mysql_install_db = find_program('mysql_install_db', ['bin', 'scripts'])

        self.mysqld = self.settings.get('mysqld')
        if self.mysqld is None:
            self.mysqld = find_program('mysqld', ['bin', 'libexec', 'sbin'])


def find_program(name, subdirs):
    path = get_path_of(name)
    if path:
        return path

    mysql_paths = [os.path.join(dir, 'bin', 'mysql') for dir in SEARCH_PATHS] + \
                  [get_path_of('mysql')]
    for mysql_path in mysql_paths:
        if mysql_path and os.path.exists(mysql_path):
            for subdir in subdirs:
                replace = '/%s/%s' % (subdir, name)
                path = re.sub('/bin/mysql$', replace, mysql_path)
                if os.path.exists(path):
                    return path

    raise RuntimeError("command not found: %s" % name)
