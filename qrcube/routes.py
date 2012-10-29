# A batch QRCode generator with a twist
# goal: a multiple QRCode generator
# Wed 26 September
import os
import sys
import datetime
import toolbox
import sqlite3 as sqlite

# add project and libs to path
from toolbox import settings # <-- default_config gets loaded here
import bottle
from bottle import (Bottle, run, post, get, template, request, static_file)
from PyQRNative import QRCode, QRErrorCorrectLevel

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
    def __init__(self, path=settings.QR_FS_ROOT, author_id=0, eclevel=QRErrorCorrectLevel.L, qrtypenumber=settings.DEFAULT_QRTYPENUMBER):
        self.path = path
        self.eclevel = int(eclevel)
        self.author_id = author_id
        self.qrtypenumber = qrtypenumber

    def create_qrcode_file(self, text, img_type, name):
        # write qr code to filesystem
        if img_type not in settings.QR_IMG_TYPES:
            raise ImageTypeException("can't generate QR Code, not a valid image type (determined by extension) " + settings.QR_IMG_TYPES)
        if not toolbox.string_has_content(text):
            raise ValueError("can't generate QR Code without proper string content")
        qr = QRCode(self.qrtypenumber, self.eclevel)
        qr.addData(text)
        qr.make()
        im = qr.makeImage()
        qrcode_filename = name+img_type
        full_file_path = os.path.join(settings.QR_FS_ROOT, qrcode_filename)
        im.save(full_file_path)
        return qrcode_filename, full_file_path

    def create_qrcode_record(self, author_id, content, eclevel, qrtypenumber,\
filename, alttag, titletag, creation_date):
        # write a record to the QRCode table, returns record id
        con = sqlite.connect(settings.DB_FILE_PATH)
        c = con.cursor()
        c.execute("INSERT INTO QRCode VALUES (NULL,?,?,?,?,?,?,?,?)",(author_id, content, eclevel, qrtypenumber, filename, alttag, titletag,creation_date))
        new_id = c.lastrowid
        con.commit()
        c.close()
        return new_id

    def create_qrcode(self, content, alttag, titletag, img_types=settings.QR_IMG_TYPES):
        # determine the name of the QRCode file
        # HACK, just calling it something random [TODO] refactor
        print("in create_qrcode: " + content)
        name = toolbox.random_identifier()
        # first make the file(s)
        def qrcode_files(qr_img_types):
            for t in qr_img_types:
                qrcode_filename, full_file_path = self.create_qrcode_file(content, t, name)
                yield qrcode_filename, full_file_path
        qrcode_fullpaths = [y for x,y in qrcode_files(settings.QR_IMG_TYPES)]
        # then make the qrcode record
        qr_id = self.create_qrcode_record(self.author_id, content, self.eclevel, self.qrtypenumber, qrcode_fullpaths[0], alttag, titletag, datetime.datetime.now())
        return qr_id, name

@post('/generate')
def handle_generate_form():
    # check the text
    content = request.forms.get('content')
    alttag = request.forms.get('alttag')
    titletag = request.forms.get('titletag')
    eclevel = request.forms.get('eclevel')
    author_id = request.forms.get('author_id')
    try:
        print(content)
        # make QRCode
        maker = QRCodeMaker(author_id=author_id, eclevel=eclevel)
        qr_id, qrcode_filename = maker.create_qrcode(content, alttag, titletag)
        # serve page with qrcode and download link(s)
        return template('yourqr', qrcode_filename=qrcode_filename, titletag=titletag, alttag=alttag)
    except ValueError:
        # show error messages
        return template('qrcube_test', error_msg="probably didn't get value from the form for the qrcode content")
    except IOError:
        # show message saying the qrcode can't be written to the system
        return template('qrcube_test', error_msg='technical error, probably a\
filesystem issue, check config and permissions')

@get('/')
@get('/generate')
def generate():
    return template('qrcube_test', error_msg='')

@get('/show_records/<table>')
def show_records(table):
    # for DEBUG purposes only!! [TODO] remove this route once somewhere public
    con = sqlite.connect(settings.DB_FILE_PATH)
    c = con.cursor()
    c.execute("SELECT * FROM %s" % table)
    return [str(i)+'<br \>\n' for i in c.fetchall()]

@get('/r/<qrname>')
def qrlanding(qrname):
    # get corresponding record
    con = sqlite.connect('qrcube.db')
    c = con.cursor()
    # [TODO] this will cause problems when 2 comps have the same name, refactor
    # or ensure that no 2 'comps' have the same name
    c.execute("SELECT * FROM qrbattle WHERE comp1 = ? OR comp2 = ?",
(qrname,qrname))
    row = c.fetchone() # we need fields 3 and 4
    if row:
        # if found show the template with the points
        comp1 = row[3]
        print comp1
        comp2 = row[4]
        print comp2
        return template('battlefield',
                        qrimg1=comp1,
                        qrimg2=comp2,
                        error_msg=''
                        )
    else:
        # if not found, direct to homepage
        return battle()

@get('/qrs/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=settings.QR_FS_ROOT)

@get('/<filepath:path>')
def serve_style(filepath):
    return static_file(filepath, root=settings.WEBSTYLE_ROOT)

