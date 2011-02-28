from cStringIO import StringIO
import re

int_filter = re.compile('(0|-?[1-9][0-9]*)e')

def decode_int(x, f):
    m = int_filter.match(x, f)
    if m is None:
        raise ValueError
    return (long(m.group(1)), m.end())

string_filter = re.compile('(0|[1-9][0-9]*):')

def decode_string(x, f):
    m = string_filter.match(x, f)
    if m is None:
        raise ValueError
    l = int(m.group(1))
    s = m.end()
    return (x[s:s+l], s + l)

def decode_list(x, f):
    r = []
    while x[f] != 'e':
        v, f = bdecode_rec(x, f)
        r.append(v)
    return (r, f + 1)

def decode_dict(x, f):
    r = {}
    lastkey = None
    while x[f] != 'e':
        k, f = decode_string(x, f)
        if lastkey is not None and lastkey >= k:
            raise ValueError
        lastkey = k
        v, f = bdecode_rec(x, f)
        r[k] = v
    return (r, f + 1)

def bdecode_rec(x, f):
    t = x[f]
    if t == 'i':
        return decode_int(x, f + 1)
    elif t == 'l':
        return decode_list(x, f + 1)
    elif t == 'd':
        return decode_dict(x, f + 1)
    else:
        return decode_string(x, f)

def bdecode(x):
    try:
        r, l = bdecode_rec(x, 0)
    except IndexError:
        raise ValueError
    if l != len(x):
        raise ValueError
    return r


def bencode_rec(x, b):
    t = type(x)
    if t in (int, long, bool):
        b.write('i%de' % x)
    elif t is str:
        b.write('%d:%s' % (len(x), x))
    elif t in (list, tuple):
        b.write('l')
        for e in x:
            bencode_rec(e, b)
        b.write('e')
    elif t is dict:
        b.write('d')
        keylist = x.keys()
        keylist.sort()
        for k in keylist:
            assert type(k) is str
            bencode_rec(k, b)
            bencode_rec(x[k], b)
        b.write('e')
    else:
        assert 0

def bencode(x):
    b = StringIO()
    bencode_rec(x, b)
    return b.getvalue()