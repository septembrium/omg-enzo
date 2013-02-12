# QRCube data handling (qrcode generation, database and filesystem stuff)
# Tue Feb 12
import os
import datetime
import toolbox
import qrcode
import sqlite3 as sqlite

# add project and libs to path
from toolbox import (lid, settings) # <-- default_config gets loaded here
import bottle
from bottle import (Bottle, run, post, get, template, request, static_file)

class ImageTypeError(Exception):
    def __init__(self, msg):
        self.value=msg

    def __str__(self):
        errormsg = str(self.value) + '\n'
        for i in settings.QR_IMG_TYPES: errormsg += ', '+str(i)
        return repr(errormsg)

class QRCodeMaker:
    '''
    makes QRCodes on the filesystem and creates matching database records
    external data: path, author_id, eclevel, qrtypenumber, content, alttag, titletag,
    '''
    def __init__(self, path=settings.QR_FS_ROOT, author_id=0, eclevel=qrcode.ERROR_CORRECT_L, qrtypenumber=settings.DEFAULT_QRTYPENUMBER):
        self.path = path
        self.eclevel = int(eclevel)
        self.author_id = author_id
        self.qrtypenumber = qrtypenumber # [TODO] factor this member out, type or version are determined by the length of the content
        lid("QRCodeMaker object created")

    def create_qrcode_file(self, text, img_type, name):
        # write qr code to filesystem
        lid("create_qrcode_file start")
        if img_type not in settings.QR_IMG_TYPES:
            raise ImageTypeException("can't generate QR Code, not a valid image type (determined by extension) " + settings.QR_IMG_TYPES)
        if not toolbox.string_has_content(text):
            raise ValueError("can't generate QR Code without proper string content")
        # determine the qrcode type based on amount of content to load
        lid("looks like the image type check out ...")
        content_length = len(text)
        # [TODO] optimize best version determination, the best_fit method (called by default) of the QRCode lib is based on cathing DataOverflowErrors, determining version should be declarative lookup based
        qr = qrcode.QRCode(self.qrtypenumber, self.eclevel)
        qr.add_data(text)
        qr.make()
        im = qr.make_image()
        qrcode_filename = name+img_type
        full_file_path = os.path.join(settings.QR_FS_ROOT, qrcode_filename)
        im.save(full_file_path)
        lid("wrote file to filesystem: %s" % full_file_path)
        return qrcode_filename, full_file_path

    def create_qrcode_record(self, author_id, content, eclevel, qrtypenumber,\
filename, alttag, titletag, creation_date):
        # write a record to the QRCode table, returns record id
        lid("start of create_qrcode_record")
        con = sqlite.connect(settings.DB_FILE_PATH)
        c = con.cursor()
        c.execute("INSERT INTO QRCode VALUES (NULL,?,?,?,?,?,?,?,?)",(author_id, content, eclevel, qrtypenumber, filename, alttag, titletag,creation_date))
        new_id = c.lastrowid
        con.commit()
        c.close()
        return new_id

    def create_qrcode(self, content, alttag, titletag, img_types=settings.QR_IMG_TYPES):
        # determine the name of the QRCode file
        lid("creating qrcode ...")
        # HACK, just calling it something random [TODO] refactor
        name = toolbox.random_identifier()
        # first make the file(s)
        def qrcode_files(qr_img_types):
            for t in qr_img_types:
                qrcode_filename, full_file_path = self.create_qrcode_file(content, t, name)
                yield qrcode_filename, full_file_path
        lid("before making qrcode_fullpaths")
        qrcode_fullpaths = [y for x,y in qrcode_files(settings.QR_IMG_TYPES)]
        lid("de qrcode full_paths:", qrcode_fullpaths)
        # then make the qrcode record
        qr_id = self.create_qrcode_record(self.author_id, content, self.eclevel, self.qrtypenumber, qrcode_fullpaths[0], alttag, titletag, datetime.datetime.now())
        return qr_id, name


