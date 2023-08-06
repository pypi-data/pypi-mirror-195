from os import path, sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from loguru import logger
from ftplib import FTP


class ConnFtpServer:
    """
    The ConnFtpServer class is used for connecting to a FTP Server. The constructor accepts the following parameters with the indicated types:
        hostname (str): The hostname of the FTP server.
        username (str): The username to login to the FTP server.
        password (str): The password to login to the FTP server.
    """    
    def __init__(self, hostname, username, password):
        self.ftp = FTP()
        self.ftp.connect(host=hostname, port=21)
        self.ftp.set_pasv(True)
        self.ftp.login(user=username, passwd=password)
        logger.debug(self.ftp.getwelcome())


if __name__ == "__main__":
    pass
    # ConnFtpServer(hostname=hostname, username=username, password=password)