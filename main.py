#/bin/python
import xml.etree.ElementTree as ET
import base64
import gzip
import tarfile
from io import BytesIO
import argparse

class SwgUnpack:
    def __init__(self, XMLdata) -> None:
        self.XMLdata = XMLdata
        self.B64 = self.getB64()
        self.GZIP = self.getGZIP()
        self.TAR = self.getTAR()
        self.getPlain()
        pass

    def getB64(self):
        xmlFile = ET.parse(self.XMLdata)
        return xmlFile.find('.//co_backup_data').text

    def getGZIP(self):
        return base64.b64decode(self.B64)

    def getTAR(self):
        return BytesIO(gzip.decompress(self.GZIP))

    def getPlain(self):
        with tarfile.open(fileobj=self.TAR, mode='r') as tar:
            tar.extractall(path=".")

parser = argparse.ArgumentParser(description='Extract SWG configuration from XML backup file.')
parser.add_argument('backupfile', type=str, help='Backup file from SWG.')
args = parser.parse_args()

print(f'Backup File: {args.backupfile}')
SwgUnpack(args.backupfile)
print("Done!")