import atexit
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
from mysqld_integration_test.settings import ConfigInstance
from mysqld_integration_test.version import __version__

class Mysqld:
    def __init__(self, config='mysqld-integration-test.cfg'):
        logger.debug(f"mysqd-integration-test {__version__}")

        self.child_process = None
        self.config = Settings.parse_config_file(config)
        logger.setlevel(self.config.general.log_level)

        atexit.register(self.stop)


    def __del__(self):
        if self.config:
            logger.debug(f"Cleaning up temp dir {self.config.dirs.base_dir}")
            # Sleep for a 1/2 sec to allow mysql to shut down
            time.sleep(0.5)
            shutil.rmtree(self.config.dirs.base_dir)


    def run(self):
        if self.child_process:
            logger.error("Error, database already running!")
            return  # already started

        # Get the mysql variant and version
        (variant, version, version_minor) = self.parse_version(subprocess.check_output([self.config.database.mysqld_binary, '--version']).decode("utf-8"))
        logger.debug(f"VERSION: {variant} {version} {version_minor}")

        # Set the owner pid
        self.owner_pid = os.getpid()

        # Build the mysql base fileset
        # Make base directories
        logger.debug("Creating application directories")
        os.mkdir(self.config.dirs.tmp_dir)
        os.mkdir(self.config.dirs.etc_dir)
        os.mkdir(self.config.dirs.data_dir)

        # Write my.cnf
        logger.debug("Writing my.cnf")
        self.write_mycnf()

        # Initialize database files
        logger.debug("Initializing databases with mysql_install_db")
        subprocess.Popen([self.config.database.mysql_install_db_binary, f"--defaults-file={os.path.join(self.config.dirs.etc_dir, 'my.cnf')}", f"--datadir={self.config.dirs.data_dir}"] , stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()

        # Start up the database
        try:
            logger.debug("Starting mysql")
            self.mysql_command_line = [self.config.database.mysqld_binary, f"--defaults-file={os.path.join(self.config.dirs.etc_dir, 'my.cnf')}"]
            self.child_process = subprocess.Popen(self.mysql_command_line, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        if variant == "mariadb" and version >= 10:
            logger.debug("Detected MariaDB >= 10: Resetting password")
            current_user = os.getlogin()
            cnx = mysql.connector.connect(user=current_user, unix_socket=self.config.database.socket_file,
                                  host=self.config.database.host, port=self.config.database.port)
            cursor = cnx.cursor()
            cursor.execute(f"ALTER USER '{self.config.database.username}'@'localhost' IDENTIFIED BY '{self.config.database.password}';")
            cursor.execute("FLUSH PRIVILEGES;")
            cnx.commit()
            cursor.close()
            cnx.close()

        # create test database
        cnx = mysql.connector.connect(user=current_user, unix_socket=self.config.database.socket_file,
                              host=self.config.database.host, port=self.config.database.port)
        cursor = cnx.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS test')
        cnx.commit()
        cursor.close()
        cnx.close()

        # Return specifics the user can use to connect to the test instance
        instance_config = ConfigInstance()
        instance_config.host = self.config.database.host
        instance_config.port = self.config.database.port
        instance_config.username = self.config.database.username
        instance_config.password = self.config.database.password
        return(instance_config)


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
            logger.debug("Stopping server")
            self.child_process.send_signal(_signal)
            killed_at = datetime.now()
            while self.child_process.poll() is None:
                if (datetime.now() - killed_at).seconds > self.config.general.timeout_stop:
                    self.child_process.kill()
                    raise RuntimeError("Failed to shutdown mysql (timeout)" )

                time.sleep(0.5)
        except OSError:
            pass

        self.child_process = None


    def write_mycnf(self):
        with open(os.path.join(self.config.dirs.etc_dir, 'my.cnf'), 'wt') as my_cnf:
            my_cnf.write("[mysqld]" + "\n")
            my_cnf.write(f"bind-address={self.config.database.host}" + "\n")
            my_cnf.write(f"port={self.config.database.port}" + "\n")
            my_cnf.write(f"datadir={self.config.dirs.data_dir}" + "\n")
            my_cnf.write(f"tmpdir={self.config.dirs.tmp_dir}" + "\n")
            my_cnf.write(f"socket={self.config.database.socket_file}" + "\n")
            my_cnf.write(f"pid-file={self.config.database.pid_file}" + "\n")


    def wait_booting(self):
        exec_at = datetime.now()
        while True:
            if self.child_process.poll() is not None:
                raise RuntimeError("Failed to launch mysql binary")

            if self.is_server_available():
                break

            if (datetime.now() - exec_at).seconds > self.config.general.timeout_start:
                raise RuntimeError("Failed to launch mysql binary (timeout)")

            time.sleep(0.5)

    def is_server_available(self):
        return os.path.exists(self.config.database.pid_file)


    def parse_version(self, version):
        return ('mariadb', 10, '5.16')


