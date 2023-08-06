from os import path, sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from loguru import logger
from .connServer import ConnFtpServer


class ExpdDownloadFtpServerFile(ConnFtpServer):
    """Class is used for connecting to a FTP Server and downloading files.
        The constructor accepts the following parameters with the indicated types:
            destfolder (str): The full path on the FTP server to download the file from.
            savefolder (str): The local folder on the computer to save the downloaded file to.
            fstartwith (str): A string that all filenames will begin with in order to be considered valid for download.
        @method download(number): automatic download/arachived from the server
            number (integer): number of files downloaded
            
    """    
    def __init__(self, hostname, username, password, destfolder, savefolder, fstartwith):
        super().__init__(hostname, username, password)
        self.destfolder = destfolder
        self.savefolder = savefolder
        self.fstartwith = fstartwith
        
    @property
    def files(self):
        self.ftp.cwd(self.destfolder)
        files = [x for x in self.ftp.nlst() if x.startswith(self.fstartwith)]
        if len(files) == 0:
            logger.warning("No files to download, scripting will be exiting")
            sys.exit()
        else:
            logger.debug(f"server total files: [{len(files)}]")
        return files
    
    def archive(self, from_file, to_path, to_file):
        history = self.ftp.nlst(to_path)
        if to_file not in history:
            self.ftp.rename(f"{from_file}", f"{to_path}\{to_file}")
            logger.debug(f"server file [ {from_file} ] archived to history folder successfully.")
        else:
            logger.warning(f"file exist in history folder, delete: {from_file}")
            self.ftp.delete(from_file)

    @logger.catch(reraise=True)
    def download(self, numbers):
        try:
            for count, file in enumerate(self.files, 1):
                with open(path.join(self.savefolder, f"{file}.edi"), 'wb') as rd:
                    self.ftp.retrbinary('RETR %s' % file, rd.write)
                self.archive(file, "History", file)
                logger.debug(f"NO.{count}: file {file} download & archived successfully")
                if count == numbers:
                    break
        finally:
            self.ftp.quit()
    

if __name__ == '__main__':
    pass
    # ExpdDownloadFtpServerFile(
    #     hostname=hostname,
    #     username=username,
    #     password=password,
    #     destfolder=destfolder,
    #     savefolder=savefolder,
    #     fstartwith=fstartwith,
    # ).download(numbers=1)