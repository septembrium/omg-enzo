from PyQRNative import *
import csv

class TestFile(object):
    """
    singleton holding test file content
    only want to read it once
    """
    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(TestFil, self).__new__(self, *args, **kwargs)
        self._instance.update_with_module(default_config)
        return self._instance



def make_me_a_qrcode(length, version, eclevel, prepend=''):
    qr = QRCode(version, eclevel)
    cnt_file = open('testcontent.txt', 'rb')
    print('test file encoding: %s' % cnt_file.encoding)
    cnt = ''
    for line in cnt_file:
        cnt += line
    print('test file character count %s' % str(len(cnt)))
    qr.addData(cnt[0:length])
    qr.make()
    im = qr.makeImage()
    im.save('/home/bert/testqrcodefiles/' + prepend + 'qrcodetest.png')

def run_full_spectrum_test():
    print('running a full a spectrum test')
    def show_and_do(n, v, ecl):
        print('len' + str(n) + ' version:' + str(v) + ' ecl:' + str(ecl))
        make_me_a_qrcode(n,v,ecl,prepend=str(n)+'_'+str(v)+'_'+str(ecl)+'_')
    def det_ecl(ecl):
        if ecl == 'L': return QRErrorCorrectLevel.L
        if ecl == 'M': return QRErrorCorrectLevel.M
        if ecl == 'Q': return QRErrorCorrectLevel.Q
        if ecl == 'H': return QRErrorCorrectLevel.H
    csv_reader = csv.reader(open("qr_code_capacity.csv","rb"), delimiter=",", quotechar='"')
    for row in csv_reader:
        print row
        if row[0] == 'Version':
            print('skipping header row')
            continue # skip header row
        v=1
        ecl=QRErrorCorrectLevel.L
        if row[0] <> '' and int(row[0]) <> v: # only change version when in row, take along for next rows
            v = int(row[0])
        n=int(row[6])
        ecl=det_ecl(row[2])
        show_and_do(n, v, ecl)

def run_a_jolly_test():
    print('running a jolly test')
    def show_and_do(l, v, ecl):
        print('len' + str(l) + ' version:' + str(v) + ' ecl:' + str(ecl))
        make_me_a_qrcode(l,v,ecl,prepend=str(l)+'_'+str(v)+'_'+str(ecl)+'_')
    l = 17 # <- 17 is the limit for v1 ecl L
    v = 1
    ecl = QRErrorCorrectLevel.L
    show_and_do(l,v,ecl) # The quick brown f
    l = 14
    ecl = QRErrorCorrectLevel.M
    show_and_do(l,v,ecl) # The quick brown f
    l = 11
    ecl = QRErrorCorrectLevel.Q
    show_and_do(l,v,ecl) # The quick brown f
    l = 7
    ecl = QRErrorCorrectLevel.H
    show_and_do(l,v,ecl) # The quick brown f
    l = 64
    v = 7
    ecl = QRErrorCorrectLevel.H
    show_and_do(l,v,ecl) # ... Dat hem lazy is den d

if __name__=="__main__":
    run_full_spectrum_test()
