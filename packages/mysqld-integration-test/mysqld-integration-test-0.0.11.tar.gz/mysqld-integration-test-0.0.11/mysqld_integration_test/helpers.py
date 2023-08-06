import os
import re
import socket

from mysqld_integration_test.log import logger

BASEDIRS = ['/', '/usr', '/usr/local']

class Utils():

    @staticmethod
    def find_program(name, subdirs):
        for basedir in BASEDIRS:
            for subdir in subdirs:
                path = os.path.join(basedir, subdir, name)
                logger.debug(f"Searching for {name} in {path}")
                if os.path.exists(path):
                    return path

        raise RuntimeError(f"Command not found: {name}")


    @staticmethod
    def get_unused_port():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        _, port = sock.getsockname()
        sock.close()

        return port

    @staticmethod
    def parse_version(version_str):
        version_info = (re.findall(r"Ver (\d+)\.([0-9.]+)\-(\w+)", version_str))
        version_major = int(version_info[0][0])
        version_minor = version_info[0][1]
        version_variant = version_info[0][2].lower()

        if version_major == 8:
            version_variant = "mysql"

        return (version_variant, version_major, version_minor)
