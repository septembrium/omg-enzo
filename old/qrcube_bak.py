# A minimalist website that let's you generate QRCode "toys"
# goal: a multiple QRCode generator
# Wed 26 September
import bottle
from bottle import post, get, template, request, static_file
from bottle.ext import sqlite
import sys
import toolbox
import sqlite3
from PyQRNative import QRCode, QRErrorCorrectLevel

# prep app
app = bottle.Bottle()
plugin = bottle.ext.sqlite.Plugin(dbfile='qrcube')
app.install(plugin)

# config
QR_URL_FQDN="http://localhost:8080/" # for the encoded value
QR_IMG_TYPES=['.jpg','.png','.eps'] # valid image types, by extension
QR_FS_ROOT="/home/bert/Documents/omg-enzo/qrs/"
WEBSTYLE_ROOT="/home/bert/Documents/omg-enzo/style/"
DB_NAME="qrcube.db"
URL_ROOT="http://localhost:8080/"

class ImageTypeError(Exception):
    def __init__(self, msg):
        self.value=msg

    def __str__(self):
        errormsg = str(self.value) + '\n'
        for i in QR_IMG_TYPES: errormsg += ', '+str(i)
        return repr(errormsg)

# QR Code generation
def save_qrcode(text, img_type, path, name, qr_type_number, error_correct_level):
    # write qr code to filesystem
    if img_type not in QR_IMG_TYPES:
        raise ImageTypeException("can't generate QR Code, not a valid type")
    if not toolbox.string_has_content(text):
        raise ValueError("can't generate QR Code without proper string content")
    qr = QRCode(qr_type_number, error_correct_level)
    qr.addData(text)
    qr.make()
    im = qr.makeImage()
    qrcode_filename = name+img_type
    im.save(QR_FS_ROOT+qrcode_filename)
    return qrcode_filename

@post('/generate')
def handle_form():
    # check the text
    text = request.forms.get('qrtext')
    try:
        # write qr code to filesystem
        qrcode_filename = save_qrcode(text, QR_IMG_TYPES[1], QR_FS_ROOT,
toolbox.random_identifier(), 2, QRErrorCorrectLevel.L)
        # serve page with qrcode and download link(s)
        return template('yourqr', qrcode_filename=qrcode_filename, text=text)
    except ValueError:
        # show error messages
        return template('index', error_msg='please enter some text')
    except IOError:
        # show message saying the qrcode can't be written to the system
        return template('index', error_msg='technical error, probably a\
filesystem issue, check config and permissions')

@get('/')
@get('/generate')
def generate():
    return template('index', error_msg='')

@post('/battle')
def handle_battle_form():
    comp1 = request.forms.get('comp1')
    comp2 = request.forms.get('comp2')
    question = request.forms.get('question')
    # [TODO] make slug safe, no dupes possible, safe to be used in a URL
    slug = comp1 + '-vs-' + comp2
    # [TODO] create the 2 QRCodes contents (what's encoded)
    qr_content1 = comp1
    qr_content2 = comp2
    # starting points
    points1 = 0
    points2 = 0
    # dummy content for "question" field
    question = "nog niks" 
    try:
        # connect to database
        con = sqlite3.connect('qrbattle.db')
        # write QR Codes to the filesystem, [TODO] off course these names
        # should be added to the database record, otherwise we can not couple
        # them afterwards
        qrcode_file1 = save_qrcode(qr_content2, QR_IMG_TYPES[1], QR_FS_ROOT,
toolbox.random_identifier(), 2, QRErrorCorrectLevel.L)
        qrcode_file2 = save_qrcode(qr_content1, QR_IMG_TYPES[1], QR_FS_ROOT,
toolbox.random_identifier(), 2, QRErrorCorrectLevel.L)
        # write to db
        # [TODO] check database availability of "slug" name in db
        c = con.cursor()
        c.execute("INSERT INTO qrbattle VALUES (NULL,?,?,?,?,?,?,?,?)", (slug, question, comp1, comp2, qr_content1, qr_content2, points1, points2))
        new_id = c.lastrowid
        print "new_id is " + str(new_id)
        con.commit()
        c.close()
        # serve page with QR Codes
        return template('battlefield',
                        qrimg1=qrcode_file1,
                        qrimg2=qrcode_file2,
                        error_msg=''
                        )
    except ValueError:
        # show error messages
        return template('index', error_msg='fill in both competitors')
    except IOError:
        # show message saying the qrcode can't be written to the system
        return template('index', error_msg='technical error, probably a\
filesystem issue, check config and permissions')

@get('/showslugs')
def showslugs():
    con = sqlite3.connect('qrbattle.db')
    c = con.cursor()
    c.execute("SELECT * FROM qrbattle")
    return [str(i)+'<br \>\n' for i in c.fetchall()]

@get('/r/<qrname>')
def qrlanding(qrname):
    # get corresponding record
    con = sqlite3.connect('qrbattle.db')
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

@get('/testdbplugin')
def plugintest(db):
    db.execute('INSERT (null, 0, "foobar", 0, 0, "dzefile", "dzealttag",\
"dzetitletag", "25-09-2012")')
    row =  b.execute('SELECT * FROM QRCode').fetchone()
    if row:
        return str(row)
    return HTTPError(404, "Page lost in space.")

@get('/battle')
def battle():
    return template('qrbattle', error_msg='')

@get('/qrs/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=QR_FS_ROOT)

@get('/<filepath:path>')
def serve_style(filepath):
    return static_file(filepath, root=WEBSTYLE_ROOT)

