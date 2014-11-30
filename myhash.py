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
        