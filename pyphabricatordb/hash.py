import hashlib

# python port of PhabricatorHash.digestForIndex
def digestForIndex(s):
    hash = hashlib.sha1(s).digest();
    map = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._"
    result = ""
    for i in xrange(12):
        result = result + map[ord(hash[i]) & 0x3F]
    return result
