# my first "real" BottlePy project
# goal: light web front-end for a QR Code generator
# Wed Jul 25
import bottle
from bottle import post, get, template, request, static_file
import sys, random, time
import toolbox
from PyQRNative import QRCode, QRErrorCorrectLevel

# config 
QR_URL_FQDN="http://localhost:8080/" # for the encoded value
QR_IMG_TYPES=['.jpg','.png','.eps']
QR_FS_ROOT="/home/bert/Desktop/project/qrs/"

# utility functions
def random_identifier():
    ''' time ceasarcypher and random, no guarantee that it's unique!! '''
    timepart = str(time.time())[-5:].replace('.','')
    rndpart = str(random.random())[-5:].replace('.','')
    return ''.join([timepart, rndpart])

@post('/generate')
def handle_form():
    # check the text
    text = request.forms.get('qrtext')
    if not toolbox.string_has_content(text):
        # show error messages
        return template('index', error_msg='please enter some text') # [TODO] update
    else:
        # write qr code to filesystem
        qr = QRCode(2, QRErrorCorrectLevel.L)
        qr.addData(text)
        qr.make()
        im = qr.makeImage()
        qrcode_filename = random_identifier()+QR_IMG_TYPES[1]
        im.save(QR_FS_ROOT+qrcode_filename)
        # serve page with qrcode and download links
        return template('yourqr', qrcode_filename=qrcode_filename, text=text) # [TODO] # make template

@get('/generate')
def generate():
    return template('index', error_msg='')

@get('/')
def index():
    return generate()

@get('/qrs/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=QR_FS_ROOT)
