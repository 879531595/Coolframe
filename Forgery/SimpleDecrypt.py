import hashlib

def get_md5(_str):
    m1 = hashlib.md5()
    m1.update(_str)
    return m1.hexdigest()

def get_sha1(_str):
    m1 = hashlib.sha1()
    m1.update(_str)
    return m1.hexdigest()


