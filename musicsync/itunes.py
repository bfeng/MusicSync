import binascii


class iTunesLibrary(object):
    def __init__(self, itl_path):
        f_i = open(itl_path, 'rb')
        f_itl_bin = f_i.read()
        f_i.close()
        f_itl_hex = str(binascii.hexlify(f_itl_bin)).upper()
        print(f_itl_hex[104:120])


iTunesLibrary(u'/Users/bfeng/Music/iTunes/iTunes Library.itl')
