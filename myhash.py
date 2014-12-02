import hashlib
import sys, os

def get_md5(filepath):
    with open(filepath, 'rb') as f:
        obj = hashlib.md5()
        obj.update(f.read())
        ret = obj.hexdigest()
    return ret

def get_sha1(filepath):
    with open(filepath, 'rb') as f:
        obj = hashlib.sha1()
        obj.update(f.read())
        ret = obj.hexdigest()
    return ret

def calc_md5(text):
    obj = hashlib.md5()
    obj.update(text)
    ret = obj.hexdigest()
    return ret

def calc_sha1(text):
    obj = hashlib.sha1()
    obj.update(text)
    ret = obj.hexdigest()
    return ret


username_charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
password_charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-.:;<=>?@[]^_{|}~ "
def check_text(username, password):
    for it in username:
        if it not in username_charset:
            return False
    for it in password:
        if it not in password_charset:
            return False
    return True

ALLOWED_EXT = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'ogg', 'mp4', 'bmp', 'ico'])
def check_filename(filename): #---------- upload [check] ----------
    return ('.' in filename) and (filename.rsplit('.', 1)[1] in ALLOWED_EXT)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # >>python myhash.py [filepath]
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print("[ERROR] cannot find file.")
        else:
            print get_md5(filepath)
            print get_sha1(filepath)
    else:
        print("[ERROR] no filename.")
        
