from PyQRNative import *

def make_me_a_qrcode(length, version, eclevel, prepend=''):
    qr = QRCode(version, eclevel)
    cnt = 'adfasdfasdf adsf adsf asdf asd fas dfa sdf asdf asdf asdf sd fa sdf asdf asf asdf '
    qr.addData(cnt[0:length])
    qr.make()
    im = qr.makeImage()
    im.save('/home/bert/testqrcodefiles/' + prepend + 'qrcodetest.png')

if __name__ == "__main__":
    make_me_a_qrcode(17,1,QRErrorCorrectLevel.L)
