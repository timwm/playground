#!/bin/python

import locale, os, subprocess, shutil, re


def myexit( code, error=None, stack=None ):
    if None is error:
        error = "exiting due to precious errors. code: %d"% code 
    pformart("%s"% error, "\nError", colour='E')
    if stack:
        pformart("\33[2m\33[Kwhen running \33[1m\33[K%s\33[m\33[K"% stack,
            "Stack Trace\n...  ")
    os._exit( code )


def pformart( body, head=None, colour=None, file=os.sys.stderr ):
    c = {'E': "1;31", 'W': "1;2;33", 'I': "1;36", 'P': "1;3;32", 'S': '1;2',
        'D' : "1"}
    cb = "\33[;"+ ( colour and c.get(colour.upper(), colour) or
            c.get(head and head[0].upper(), c['D']) ) +"m\33[K"
    ce = "\33[m\33[K"
    cc = head and '\n'+ cb +"...  "+ ce or ''

    w = shutil.get_terminal_size()[0] - 3
    i = len(head and head or '')
    pat = re.compile('\33\[.+?\33\[K')
    prev_escs = ''
    lines = cb + (head and head + ce +' ' or ce +'')
    for word in body.split(' '):
        l = len( re.sub( pat, '', word ) )
        if l >= w or (i + l) > w:
            lines += cc + prev_escs + word
            i = len(cc) - len(cb + ce)
        else:
            lines += word +' '
        i += l + 1 # plus space
        escs = re.findall( pat, word )
        if escs:
            # FIXME many escape sequences, maybe remove everything upto the last
            # \33[m\33[K i.e ''.join(''.join(escs).rpartition('\33[m\33[k')[1:])
            # Due to performace, just let the shell do all escaping resolutions
            prev_escs += ''.join(escs)

    print( lines, file=file )


def parse_arguments():
    """Parse the program arguments"""
    from optparse import OptionParser  # pylint: disable=deprecated-module
    from datetime import datetime
    import errno

    uname = os.uname()
    MACHINE_ID = uname.machine +' '+ uname.sysname
    USAGE = '%prog [options] SRC'
    VERSION = '0.01.0'
    VERSION_MSG = [ '\033[;1m%prog {0} {1}\033[0m'.format(VERSION, MACHINE_ID),
        'Python version: {0}'.format(' '.join(line.strip() for line in os.sys.version.splitlines())),
    ]
    EPILOG="011's Kotlin Compiler Wrapper, copyleft (C) {0}-present Cactus"\
        " Communications, PLC. License GPLv3+: GNU GPL version 3 or later "\
        "<http://gnu.org/licenses/gpl.html> This is free software: you are free to "\
        "change and redistribute it. There is NO WARRANTY, to the extent permitted "\
        "by law. For bug reporting instructions, please see: "\
        "https://resinst.cci.org/kcw/bugs".format( datetime.now().year )

    parser = OptionParser( usage=USAGE, version=('\n'.join(VERSION_MSG)),
            epilog=EPILOG )
    parser.add_option('-d', '--dest', dest='dest', metavar="DEST",
            help="Destination for generated class|jar files, [<SRC>.jar]")
    parser.add_option('-k', '--keep', action="store_true", dest="keep",
            help="Don't delete generated DEST files")
    parser.add_option("-x", "--nocached", action="store_true", dest="recompile",
            help="Don't use --keep'ed file of previous run; Compile if non existent")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="Make lots of noise")
    
    options, positional = parser.parse_args()

    if not positional[:]:
        parser.print_usage( file = os.sys.stderr )
        pformart( "Missing \33[;1m\33[Krequired\33[m\33[K argument, SRC" )
        os.sys.exit( SystemExit(os.EX_USAGE) )
    elif positional[1:]:
        pformart("\33[;1m\33[Kunused options\33[m\33[K %s, support for "\
            "parsing other [\33[1m\33[Kkotlinc, kotlin\33[m\33[K] options is "\
            "\33[1m\33[KNOT\33[m\33[K available, type --help for known options. "\
            "\33[4m\33[KWill pass options as is to kotlinc\33[m\33[K\n"%
            positional[1:], "Warnning"
        )
    if not options.dest:
        options.dest = positional[0] +".jar"
    if not os.path.exists( positional[0] ):
        pformart(errno.errorcode[errno.ENOENT] +': '+ os.strerror(errno.ENOENT)+
            " \33[;1m\33[K"+ positional[0] +"\33[m\33[K", "Error" )
        os.sys.exit( errno.ENOENT )
    return ( options, positional )


def purge( top ):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    if os.path.isdir( top ): os.rmdir( top )
    else: os.remove( top )


class Compile:
    def __init__( self ):
        opts = parse_arguments() 
        self.src = opts[1][0]
        self.dest = opts[0].dest
        self.keep = opts[0].keep
        self.verbose = opts[0].verbose
        self.recompile = opts[0].recompile
        self.orig_dest = os.path.join( os.getcwd(), self.dest )
        self.kotlin = [ "kotlin", self.dest ]
        self.kotlinc = [ "kotlinc", "-include-runtime", self.src, "-d",
            self.dest ] + opts[1][1:]
        #os.sys.exit(opts)
        self.go()

    def go( self ):
        b, _, e = self.src.rpartition('.')
        if e == "kts":
            self.keep = True
            self.kotlin = [ "kotlin", self.src ]
        else:
            if self.recompile or not os.path.exists( self.dest ):
                self.run( self.kotlinc )
            if not self.dest.endswith(".jar"):
                if self.verbose:
                    pformart( "\33[1m\33[K%s\33[m\33[K"% self.dest,
                            "changing to directory", 'I' )
                    os.chdir( self.dest )
                self.kotlin = [ "kotlin", (
                    b[0].capitalize() + b[1:] + e[0].capitalize() + e[1:]
                )]
        self.run( self.kotlin )
        if not self.keep: purge( self.orig_dest )

    def run( self, cmd ):
        if self.verbose:
            pformart("\33[;1m%s\033[0m"% ' '.join( cmd ), "running... ", 'P')
        proc = subprocess.run( cmd )
        if proc.returncode:
            if os.path.exists( self.dest ) and not self.keep:
                purge( self.orig_dest )
            myexit( proc.returncode, stack=' '.join( cmd ) )


try:
    Compile()
except BaseException as E:
    os.sys.exit( os.sys.exc_info()[1] )
