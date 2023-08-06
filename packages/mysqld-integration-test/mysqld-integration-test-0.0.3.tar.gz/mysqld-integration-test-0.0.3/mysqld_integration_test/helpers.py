import os
import socket

from mysqld_integration_test.log import logger

class Utils():

    @staticmethod
    def find_program(name, subdirs):
        for basedir in ['/', '/usr', '/usr/local']:
            for subdir in subdirs:
                path = os.path.join(basedir, subdir, name)
                logger.debug(f"Searching for {name} in {path}")
                if os.path.exists(path):
                    return path

        raise RuntimeError("command not found: %s" % name)

    @staticmethod
    def get_unused_port():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        _, port = sock.getsockname()
        sock.close()

        return port


