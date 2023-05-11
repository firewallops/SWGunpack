#/bin/python
import xml.etree.ElementTree as ET
import base64
import gzip
import tarfile
from io import BytesIO
import argparse

class SwgUnpack:
    def __init__(self, args) -> None:
        self.XMLdata = args.backupfile
        self.Verbose = args.v
        self.Outpath = args.outpath
        self.B64 = ""
        self.GZIP = ""
        self.TAR = ""
        self.unpack()

    def getB64(self):
        xmlFile = ET.parse(self.XMLdata)
        return xmlFile.find('.//co_backup_data').text

    def getGZIP(self):
        return base64.b64decode(self.B64)

    def getTAR(self):
        return BytesIO(gzip.decompress(self.GZIP))

    def getPlain(self, export):
        with tarfile.open(fileobj=self.TAR, mode='r') as tar:
            tar.extractall(path=export)
    
    def unpack(self):
        if self.Verbose == True:
            print(f'Backup File: {self.XMLdata}')
        self.B64 = self.getB64()
        self.GZIP = self.getGZIP()
        self.TAR = self.getTAR()
        self.getPlain(self.Outpath)
        if self.Verbose == True:
            print("Done!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract SWG configuration from XML backup file.')
    parser.add_argument('backupfile', default="xml.backup", type=str, help='Backup file from SWG.')
    parser.add_argument('-o', '--outpath', default='.', help='Optional. Provide a path where backup should be exported.')
    parser.add_argument('-v', help="Prints a status on the screen", action='store_true')
    args = parser.parse_args()
    SwgUnpack(args)

