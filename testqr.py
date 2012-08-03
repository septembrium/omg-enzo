from PyQRNative import *

qr = QRCode(2, QRErrorCorrectLevel.L)
qr.addData("http://www.baconsalt.com")
qr.make()

im = qr.makeImage()

im.save('/home/bert/Desktop/de_qrcode.png')
im.show()
