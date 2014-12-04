# -*- coding: utf-8 -*-
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

def sex_repr(sex):
    if not sex:
        return "Not available"
    sex = int(sex)
    if sex < 0: return "Not available"
    if sex == 0: return "Male (男性)"
    if sex == 1: return "Female (女性)"
    if sex == 2: return "Gay (男性同性愛者)"
    if sex == 3: return "Lesbian (女性同性愛者)"
    if sex == 4: return "Bisexual (両性愛者)"
    if sex == 5: return "Transgender (性転換者・異性装同性愛者など)"
    if sex == 6: return "Transsexual (性転換者)"
    if sex == 7: return "Transvestite/Crossdresser (異性装者)"
    if sex == 8: return "Two-spirit (二つの精神を持った者)"
    if sex == 9: return "Asexual (無性愛)"
    if sex == 10: return "Queer"
    if sex == 11: return "FagHag"
    if sex == 12: return "Homophobia"
    if sex == 13: return "MoneyBoy"
    if sex == 14: return "Queen"
    if sex == 15: return "King"
    if sex == 16: return "Butch"
    if sex == 17: return "Intersex"
    if sex == 18: return "Otaku (御宅)"
    if sex == 19: return "BoysLoveComplex (腐女子/腐男子)"
    if sex == 20: return "GirlsLoveComplex (百合好き)"
    if sex == 21: return "SisterComplex (シスコン)"
    if sex == 22: return "BrotherComplex (ブラコン)"
    if sex == 23: return "ElectraComplex (父親に対して愛情を抱く女児)"
    if sex == 24: return "OedipusComplex (母親に対して愛情を抱く男児)"
    if sex == 25: return "Hentai (変態)"
    if sex == 26: return "Other"
    return "Unknown/Private"

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
        
