import os
import re
import socket

BASEDIRS = ['/', '/usr', '/usr/local', '/opt/homebrew']


class Utils():
    @staticmethod
    def find_program(name):
        for basedir in ['usr', 'usr/local']:
            for subdir in ['bin', 'libexec', 'sbin', 'scripts']:
                path = os.path.join("/", basedir, subdir, name)
                if os.path.exists(path):
                    return path
        return None

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
