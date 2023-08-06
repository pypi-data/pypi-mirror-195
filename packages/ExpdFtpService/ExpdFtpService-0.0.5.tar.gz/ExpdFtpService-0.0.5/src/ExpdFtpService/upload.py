from os import path, sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from loguru import logger
from .connServer import ConnFtpServer


class ExpdUploadFtpServerFile(ConnFtpServer):
    """Class is used for connecting to a FTP Server and upload files.
        The constructor accepts the following parameters with the indicated types:
            destfolder (str): The full path on the FTP server to upload the file from, create it automatically when the folder does not exists,.
            local_file (str): The local file on the computer to upload to server.
    """    
    def __init__(self, hostname, username, password, destfolder=None):
        super().__init__(hostname, username, password)
        self.destfolder = destfolder
        self.create_directory(self.destfolder)

    @logger.catch(reraise=True)
    def create_directory(self, folder):
        if not self.directory_exists(folder):
            self.ftp.mkd(folder)

    def directory_exists(self, directory):
        parent = path.dirname(directory)
        pathes = self.ftp.nlst(parent)
        return True if directory in pathes else False
    
    @logger.catch(reraise=True)
    def upload_file_to_server(self, local_file):
        try:
            with open(local_file,'rb') as f:  
                self.ftp.cwd(self.destfolder)          
                self.ftp.storbinary(f'STOR {path.basename(local_file)}', f)
                logger.debug(f"{local_file} uploaded successfully")
        finally:
            self.ftp.quit()
    

if __name__ == '__main__':
    pass
    # ExpdUploadFtpServerFile(
    #     hostname=hostname,
    #     username=username,
    #     password=password,
    #     destfolder=destfolder,
    # ).upload_file_to_server(r"D:\Solutions\edoc_upload_sourth_korea\server\data\GENRES\E13I0095652\2431295471_PIE_E433593539.pdf")