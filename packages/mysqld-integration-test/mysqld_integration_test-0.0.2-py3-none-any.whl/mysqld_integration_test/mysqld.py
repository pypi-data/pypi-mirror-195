import inspect
import tempfile
import shutil
import time
import os
import signal
import subprocess
import mysql.connector
from datetime import datetime

from mysqld_integration_test.log import logger
from mysqld_integration_test.settings import Settings
from mysqld_integration_test.version import __version__

SEARCH_PATHS = ['/usr/local/mysql']

class Mysqld:
    def __init__(self):
        logger.info(f"mysqd-integration-test {__version__}")

        self.args = Settings.parse_arguments(self)
        self.child_process = None


    def __del__(self):
        if self.args:
            logger.debug(f"Cleaning up temp dir {self.args.base_dir}")
            shutil.rmtree(self.args.base_dir)

    def run(self):
        if self.child_process:
            logger.error("Error, database already running!")
            return  # already started

        # Get the mysql brand and version
        (brand, version) = self.parse_version(subprocess.check_output([self.args.mysqld, '--version']).decode("utf-8"))

        # Set the owner pid
        self.owner_pid = os.getpid()


        # Build the mysql base fileset
        # Make base directories
        logger.debug("Creating application directories")
        os.mkdir(self.args.tmp_dir)
        os.mkdir(self.args.etc_dir)
        os.mkdir(self.args.data_dir)

        # Write my.cnf
        logger.debug("Writing my.cnf")
        self.write_mycnf()

        # Initialize database files
        logger.debug("Initializing databases with mysql_install_db")
        subprocess.Popen([self.args.mysql_install_db, f"--defaults-file={os.path.join(self.args.etc_dir, 'my.cnf')}", f"--datadir={self.args.data_dir}"] , stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()

        # Start up the database
        try:
            logger.debug("Starting mysql")
            self.mysql_command_line = [self.args.mysqld, f"--defaults-file={os.path.join(self.args.etc_dir, 'my.cnf')}"]
            self.child_process = subprocess.Popen(self.mysql_command_line) #, stdout=subprocess.STDOUT, stderr=subprocess.STDERR)
        except Exception as e:
            raise RuntimeError('failed to start %s: %r' % (self.name, e))
        else:
            try:
                self.wait_booting()
            except Exception:
                self.stop()
                raise

        # MariaDB 10 requires that you log in as the user that is running the mysql instance and reset the root pw
        # Set password
        # Get the current user
        current_user = os.getlogin()

        cnx = mysql.connector.connect(user=current_user, unix_socket=self.args.socket_file,
                              host=self.args.bind_address, port=self.args.port)
        cursor = cnx.cursor()
        cursor.execute(f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{self.args.password}';")
        cursor.execute("FLUSH PRIVILEGES;")
        cnx.commit()
        cursor.close()
        cnx.close()

        # create test database
        cnx = mysql.connector.connect(user=current_user, unix_socket=self.args.socket_file,
                              host=self.args.bind_address, port=self.args.port)
        cursor = cnx.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS test')
        cnx.commit()
        cursor.close()
        cnx.close()

    def stop(self, _signal=signal.SIGTERM):
        self.terminate(_signal)


    def terminate(self, _signal=None):
        if self.child_process is None:
            return  # not started

        if self.owner_pid != os.getpid():
            return  # could not stop in child process

        if _signal is None:
            _signal = self.terminate_signal

        try:
            self.child_process.send_signal(_signal)
            killed_at = datetime.now()
            while self.child_process.poll() is None:
                if (datetime.now() - killed_at).seconds > self.args.timeout:
                    self.child_process.kill()
                    raise RuntimeError("*** failed to shutdown mysql (timeout) ***\n" )

                time.sleep(0.5)
        except OSError:
            pass

        self.child_process = None


    def write_mycnf(self):
        with open(os.path.join(self.args.etc_dir, 'my.cnf'), 'wt') as my_cnf:
            my_cnf.write("[mysqld]" + "\n")
            my_cnf.write(f"bind-address={self.args.bind_address}" + "\n")
            my_cnf.write(f"port={self.args.port}" + "\n")
            my_cnf.write(f"datadir={self.args.data_dir}" + "\n")
            my_cnf.write(f"tmpdir={self.args.tmp_dir}" + "\n")
            my_cnf.write(f"socket={self.args.socket_file}" + "\n")
            my_cnf.write(f"pid-file={self.args.pid_file}" + "\n")


    def wait_booting(self):
        exec_at = datetime.now()
        while True:
            if self.child_process.poll() is not None:
                raise RuntimeError("*** failed to launch ***")

            if self.is_server_available():
                break

            if (datetime.now() - exec_at).seconds > self.args.timeout:
                raise RuntimeError("*** failed to launch (timeout) ***")

            time.sleep(0.5)

    def is_server_available(self):
        return os.path.exists(self.args.pid_file)


    def read_bootlog(self):
        try:
            with open(os.path.join(self.args.base_dir, '%s.log' % self.name)) as log:
                return log.read()
        except Exception as exc:
            raise RuntimeError("failed to open file:%s.log: %r" % (self.name, exc))


    def parse_version(self, version):
        return (version, version)

