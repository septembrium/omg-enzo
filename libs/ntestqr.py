import qrcode
import csv

cnt_file = open('testcontent.txt', 'rb')
print('test file encoding: %s' % cnt_file.encoding)
cnt = ''
for line in cnt_file:
    cnt += line
print('test file character count %s' % str(len(cnt)))

def make_me_a_qrcode(length, version, eclevel, prepend=''):
    qr = qrcode.QRCode(
        version=version,
        error_correction=eclevel,
        box_size=5,
    )
    # don't do versions above min_version
    min_version = 0
    if min_version > version:
        return
    qr.add_data(cnt[0:length])
    qr.make()
    im = qr.make_image()
    im.save('/home/bert/testqrcodefiles/' + prepend + 'qrcodetest.png')

class QRErrorCorrectLevel:
    L = 1
    M = 0
    Q = 3
    H = 2

def pretty_ecl(ecl): # these ecl functions could have been more elegant, but wth it works
    if ecl == QRErrorCorrectLevel.L: return 'L'
    if ecl == QRErrorCorrectLevel.M: return 'M'
    if ecl == QRErrorCorrectLevel.Q: return 'Q'
    if ecl == QRErrorCorrectLevel.H: return 'H'

def det_ecl(ecl):
    if ecl == 'L': return QRErrorCorrectLevel.L
    if ecl == 'M': return QRErrorCorrectLevel.M
    if ecl == 'Q': return QRErrorCorrectLevel.Q
    if ecl == 'H': return QRErrorCorrectLevel.H

def show_and_do(n, v, ecl):
    print('len' + str(n) + ' version:' + str(v) + ' ecl:' + str(pretty_ecl(ecl)))
    make_me_a_qrcode(n,v,ecl,prepend=str(n)+'_'+str(v)+'_'+str(pretty_ecl(ecl))+'_')

def run_full_spectrum_test():
    print('running a full a spectrum test')
    csv_reader = csv.reader(open("qr_code_capacity.csv","rb"), delimiter=",", quotechar='"')
    v=1
    ecl=QRErrorCorrectLevel.L
    for row in csv_reader:
        print row
        if row[0] == 'Version':
            print('skipping header row')
            continue # skip header row
        new_v=row[0]
        if new_v <> '' and str(v) <> new_v:
            new_v = ''.join(new_v.split('.'))
            v = int(new_v)
        n=int(''.join(row[6].split('.')))
        ecl=det_ecl(row[2])
        show_and_do(n, v, ecl)

if __name__=="__main__":
    run_full_spectrum_test()
    # show_and_do(129, 15, det_ecl('H')) # for v15, H the max is 129 instead of 220 which was specified, might be a bug in the library I'm using, I replaced it in the limits csv, after that version 26 seems to crash on L or M ecl but we'll skip all that (for now) and continue with the project
