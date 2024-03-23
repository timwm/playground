#!/bin/python3

# @uthor: @timwm (timon w. mesulam)
# @licence: GNU GPLv3+

"""
simple script to serve atleast p7zip v17.03 archived files on-the-fly, with even directory indexing :-)
"""

import os, subprocess
from datetime import datetime
from urllib import parse as urlparse

ARCHIVE_DIR = "/archives"
MIME_FILE = "/data/data/com.termux/files/usr/etc/apache2/mime.types"
LOG_FILE = "/data/data/com.termux/files/home/.011/chroot/var/log/.011/"\
    "serve_archive_files.log"
INDEX_FILES = ["index.html", "default.html", "readme", "readme.md"]

def print_headers(mime="text/plain", **headers):
    mime_info = mime.partition(';')
    dispositions = ['application/octet-stream', 'application/x-011-']
    ret = "Content-Type: {0};{1}\r\n".format(mime_info[0],
            mime_info[2] or ' charset=utf-8')\
        + "X-Powered-By: 011/r"+ datetime.utcfromtimestamp(1627488345.1376514)\
            .strftime("%FT%TZ") + "\r\n"
    for i in dispositions:
        if mime_info[0].startswith(i):
            ret += "Content-Disposition: attachment; filename={0}\r\n"\
                .format(mime_info[2])
    for h in headers:
        ret += "{0}: {1}\r\n".format(h, headers[h])
    # capture written bytes
    _ = os.write(os.sys.stdout.fileno(), bytes(ret + "\r\n", encoding="utf8"))


def redirect(rloc):
    log(301, 0, suffix=" -> {0}\n".format(rloc))
    os.sys.exit(print_headers(**{
        "Status": "301 Moved Permanently",
        "Location":  os.environ["REQUEST_SCHEME"] + "://" + os.environ["HTTP_HOST"] +
            rloc
    }))


def get_contents(resource, code=None):
    """
    get contents of resource if code is None else execute code 
    """
    from re import compile as re_compile
    scripts_dir = os.path.dirname(os.environ['SCRIPT_FILENAME']) + '/scripts'
    prog_map = {
        '.*\.ph(p[3457]?|t|tml?)$': ['php', '-q', '-d', 'display_errors=2', '-f', '@@@'],
        '.*\.py[23]?$': ['python', '-B', '@@@'],
        '.*\.md$': ['php', '-q', '-d', 'html_errors=1', '-r',
            "include('" + scripts_dir + "/Parsedown.php');"
            "echo (new Parsedown())->text(file_get_contents('@@@'));"
        ]
    }
    filename = resource
    mime = get_mime(filename)
    headers = {}
    ret = None

    for p in prog_map:
        if re_compile(p).match(resource.lower()):
            mime = 'text/html'
            if code is not None:
                from tempfile import mkstemp
                fd, filename = mkstemp()
                os.write(fd, code)
                os.close(fd)
            os.chdir(os.path.dirname(filename))
            try:
                ret = subprocess.run([a.replace('@@@', filename) for a in prog_map[p]],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except:
                return error_doc(500, os.environ['REQUEST_URI'], 'Server encountered' +
                    ' an internal error while proccessing requested resource')
            else:
                if ret.stderr:
                    return error_doc(500, os.environ['REQUEST_URI'], 'Server encountered' +
                        ' an internal error while proccessing requested resource<br><br>' +
                        '<p style="color:red;">' + str(ret.stderr)[2:-1]+'</p>')
                h, _, ret = ret.stdout.partition(b'\r\n\r\n')
                headers = {k: v for k, _, v in [l.partition(':')
                    for l in (str(h)[2:-1] if ret else '').split('\r\n')] if v}
                ret = ret or h
            if code is not None: os.remove(filename)
    if ret is None:
        if code is None:
            with open(resource, 'rb') as fh: ret = fh.read()
        else:
            ret = code
    return (200, ret, headers, mime)


def get_mime(filename):
    top, _, ext = os.path.basename(filename).lower().rpartition('.')
    mime = None
    if top:
        m = get_conf(MIME_FILE, ext, [1,999,0,1])
        mime = m and m[0]
    if not mime:
        try:
            mime = str(subprocess.run(['file', '-bi', filename],
                stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).stdout)[2:-3]
        except: 
            mime = None
    return mime or "application/x-011-" + ext


def get_conf(filename, needle, indices=[0,0,0,0]):
    """
    indices = [<haystack start>, <haystack end>, <return start>, <return end>]
    """
    with open(filename, 'r') as fh:
        for line in fh:
            haystack = line.strip('\n').split()
            if not haystack or haystack[0][0] == '#': continue
            for h in haystack[indices[0]:indices[1]]:
                if needle == h:
                    return haystack[indices[2] : indices[3]]
    return []


def extract(archive, entry, url, attempt=True):
    args = ["-mmt8", "-so", "-bd", "-spd", "-bsp2", "-bse2", "-bb0", archive, entry]
    if attempt:
        # We are not using stderr at the moment cause we're using it for other staff
        # And also VERY dependent on .7z listing
        entries = subprocess.run(["7z", "l"] + args, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL).stdout.split(b'\n') 
        index = entries[-3].rfind(b' ')
        # get number of files and directories
        summary = entries[-2][index:].split()
        length = int(summary[0]) + (int(summary[2]) if summary[2:] else 0) if summary[1:] else -1

        entries = entries[-(length + 3):-3]
        #os.sys.exit([length,index,entries])
        if length > 1 or length == 1 and entries[0].split()[2].lower().find(b'd') > -1: 
            return dirlist(archive, url, [entries, entry, index + (len(entry) or -1) + 2])
        elif length < 1:
            if length and not entry: # it's not an archive entry but just a file
                return get_contents(archive + '/' + entry if entry else archive)
            return error_doc(404, url, "Can't extract, file NOT FOUND")
    # We are not using stderr at the moment
    return get_contents(entry, subprocess.run(["7z", "e"] + args,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout)


def serve_files():
    # just put here to help with some other tests was doing with HAproxy and
    # varnishcache, it's absolutely stupid code; non realistic. You MAY delete it.
    if os.environ['REQUEST_METHOD'] == "HEAD":
        return print_headers(**{"Status": "302 Found", "Content-Length": '0'})

    archive_dir = ARCHIVE_DIR.rstrip('/') + '/'
    url = urlparse.unquote(os.environ["REQUEST_URI"])
    # path = [<server root>, <archive name>, </>, <file path>]
    path = [os.path.normpath(os.environ["DOCUMENT_ROOT"])] + list(os.path.normpath(
        urlparse.urlparse(url).path).removeprefix(archive_dir).partition('/'))
    resource = path[0] + (archive_dir if path[1] else '') + ''.join(path[1:])
    ret = tuple() # [<response>, {<headers>}, <mime type>]

    if os.path.isdir(resource): ret = dirlist(resource, url)
    elif path[1]:
        # URI prefix is ARCHIVE_DIR and have requested for an entry in ARCHIVE_DIR
        archive = path[0] + archive_dir + path[1]
        while os.path.isdir(archive):
            top, _, path[3] = path[3].partition('/')
            archive += '/' + top
        if os.path.exists(archive):
            ret = extract(archive, path[3], url)
        else:
            ret = error_doc(404, url, "No such file or archive")
    elif os.path.exists(resource):
        # if not path[3]: redirect request for / to ARCHIVE_DIR
        ret = get_contents(resource)
    else:
        ret = error_doc(404, url, "File NOT FOUND")

    ret_len = len(ret[1])
    ret[2].update({"Content-Length": str(ret_len)})

    log(ret[0], ret_len)
    print_headers(ret[3], **ret[2])
    # capture written bytes
    _ = os.write(os.sys.stdout.fileno(), ret[1])


def dirlist(path, url, archive_entries=None):
    if url[-1] != '/':
        return redirect(url + '/')
    wp = os.path.normpath(url)
    ret = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html><head>'\
        '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>'\
        "<title>Index of " + wp + "</title></head><body><h1>Index of " + wp +\
        "</h1><hr><ul>"
    if wp != '/':
        ret += '<li><a href="' + urlparse.quote(wp.rpartition('/')[0]) + '/"> ..</a>'
    if archive_entries is None: # give me the listing of {path}
        for entry in os.listdir(path):
            # handle broken symlinks and hidden files
            if not os.path.exists(path + '/' + entry) or entry[0] == '.':
                continue
            ret += '<li><a href="' + urlparse.quote(entry)
            if os.path.isdir(path + '/' + entry):
                # directory entry URL end in '/' to quicken processing
                ret += '/"><b> ' + entry + '/</b></a>'
            else:
                if entry.lower() in INDEX_FILES:
                    return get_contents(path + '/' + entry)
                ret += '"> ' + entry + '</a>'
    else:
        # list archive entries
        # we use the first line. +2 or +1: cater for b' ' and b'/'
        reg = {}
        index = archive_entries[2]
        for archive_entry in archive_entries[0]:
            entry, sep, _ = archive_entry[index:].partition(b'/')
            if reg.get(entry) or sep and reg or not entry:
                continue
            reg[entry] = True
            entry = str(entry)[2:-1]

            ret += '<li><a href="' + urlparse.quote(entry)
            if archive_entry.split()[2].lower().find(b'd') > -1: 
                # directory entry URL end in '/' to quicken processing
                ret += '/"><b> ' + entry + '/</b></a>'
            else:
                if entry.lower() in INDEX_FILES:
                    return extract(path, archive_entries[1] + '/' + entry, url, attempt=False)
                ret += '"> ' + entry + '</a>'

    return (200, bytes(ret + "</ul></body></html>", encoding="utf8"), {
        "Pragma": "no-cache", "Expires": '0',
        "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0"
        }, "text/html"
    )


def error_doc(code, url, info=''):
    db = {404: "Not Found", 500: "Internal Server Error"}
    ret = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html><head>'\
        '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>'\
        "<title>" + str(code) + " " + db[code] + "</title></head><body>"\
        "<center><br><h1>"+ str(code) + " " + db[code] + "</h1><hr><p>"\
        "Could NOT process requested resource: <b>" + url + "</b><br><br>" + info +\
        "</p><p>... and that's all I know, sorry :(</p><br><br><p>Maybe you'd like"\
        ' going to the <a href="/">homepage</a>.</p></center></body></html>'

    return (code, bytes(ret, encoding="utf8"), {
        "Status": str(code) + ' ' + db[code], "Pragma": "no-cache",
        "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
        "Expires": "0"
        }, "text/html"
    )


def log(code, length, prefix='', suffix='\n'):
    with open(LOG_FILE, "ab") as fh:
        msg = '[' + datetime.utcnow().strftime('%FT%T.%f') + ']' + prefix
        for k in ["HTTP_HOST", "REQUEST_METHOD", "REQUEST_URI"]:
            msg += ' ' + os.environ.get(k, '-')
        msg += ' ' + str(code) + ' ' + str(length) + suffix
        fh.write(bytes(msg, encoding='utf8'))


if __name__ == "__main__":
    serve_files()
