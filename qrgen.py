# my first "real" BottlePy project
# goal: light web front-end for a QR Code generator
# Wed Jul 25
import bottle
from bottle import post, get, template, request, static_file
import sys
import toolbox
from PyQRNative import QRCode, QRErrorCorrectLevel

# config
QR_URL_FQDN="http://localhost:8080/" # for the encoded value
QR_IMG_TYPES=['.jpg','.png','.eps'] # valid image types, by extension
QR_FS_ROOT="/home/bert/Documents/omg-enzo/qrs/"

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
        raise ImageTypeException("can't generte QR Code, not a valid type")
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
        # serve page with qrcode and download links
        return template('yourqr', qrcode_filename=qrcode_filename, text=text)
    except ValueError:
        # [TODO] handle filesystem permission and filewrite errors
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

@get('/qrs/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=QR_FS_ROOT)
