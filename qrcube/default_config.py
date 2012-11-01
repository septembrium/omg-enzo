# /usr/bin/env python
# encoding: utf-8
# vim: tabstop 4 spaces

import sys
import os

VERSION = '0.1'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(os.path.dirname(ROOT_DIR), 'libs')

DEBUG = True

QR_URL_FQDN="http://localhost:8080/" # for the encoded value
QR_IMG_TYPES=['.jpg','.png','.eps'] # valid image types, by extension
QR_FS_ROOT=os.path.join(os.path.dirname(ROOT_DIR), 'qrs')
WEBSTYLE_ROOT=os.path.join(os.path.dirname(ROOT_DIR), 'libs')
DB_FILE_PATH=os.path.join(os.path.dirname(ROOT_DIR), 'database', 'qrcube.db')
URL_ROOT="http://localhost:8080/"
DEFAULT_QRTYPENUMBER=2

STATIC_FILES_ROOT = os.path.join(ROOT_DIR, 'static')

TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'views'),
)

HOST = '127.0.0.1'
PORT = 8080

def show_config():
    print("printing all configuration variables ...")
    configvars = sys.modules[__name__].__dict__.iteritems()
    for name, value in configvars:
        if name.isupper():
            print(name + "\t*:*\t" + str(value))

