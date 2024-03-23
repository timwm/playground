#!/usr/bin/python

# @author @timw_mesulam (timon w. mesulam)
# @description: program to log HAproxy socket logs to disk, orignally created for
#               termux environment; It's really dirty
# @licence GNU GPLv3 or later
# @date: Fri, 05 Nov 2021 09:55:37 +0300

import socket, os, sys, signal, argparse

author = "timon w. mesulam"
root = "/data/data/com.termux/files/home/.011/chroot/"
LSOCK = root + "var/run/haplog.sock"
LPID = root + "var/run/haplog.pid"
LFILE = root + "var/log/haplog.log"

def main( ):

    global LSOCK, LFILE
    version = "0.0.1a"
    prog = sys.argv[0].split( '/' )[-1]

    argparser = argparse.ArgumentParser( prog=prog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="program to log HAproxy socket logs to disk, orignally created for termux environment.",
        epilog="NOTE: For options taking time-like arguments, if value is zero, run"
            " forever, and any value below zero stops program immediately\n\n"
            "%(prog)s Copyleft (c) 2021-present.\nLicense GPLv3+: GNU GPL version 3"
            " or later <http://gnu.org/licenses/gpl.html>\nThis is free software: you"
            " are free to change and redistribute it.\nThere is NO WARRANTY, to the"
            " extent permitted by law.\nFor bug reporting instructions, please see:"
            " https://resinst.cci.com/traker/bugs?kcw\nOriginally written by"
            " {0}, Cactus Communications, PLLC.".format( author )
    )
    argparser.add_argument( '-s', '--socket', default=LSOCK,
         help='filepath to create socket on, default: %(default)s'
    )
    argparser.add_argument( '-l', '--log', default=LFILE,
        help='log file, default: %(default)s'
    )
    argparser.add_argument( '-t', '--timeout', default=(60 * 60 * 3.0), type=float,
        help='set the socket idle timeout, default: %(default)ds'
    )
    argparser.add_argument( '-z', '--maxage', type=float,
        help="set the program's duration limit, default: timeout"
    )
    argparser.add_argument( '-d', '--deamonize', action='store_true',
        help='detach from tty and run in background; deamonize.'
    )
    argparser.add_argument( '-x', '--shutdown', nargs='?', const=0, type=int,
        help="send SIGALRM(14) signal to stop program, or specify PID"
    )
    argparser.add_argument( '-ro', '--stdout',
        help='redirect stdout, default: {} if deamonizing'.format( os.devnull )
    )
    argparser.add_argument( '-re', '--stderr',
        help='redirect stderr, default: {} if deamonizing'.format( os.devnull )
    )
    argparser.add_argument( '-p', '--pidlog', default=LPID,
        help='file to log in PID, default: %(default)s'
    )
    argparser.add_argument( '-V', '--verbose', action='store_true',
        help='make lots of noise; run in verbose mode'
    )
    argparser.add_argument( '-v', '--version', action='version',
        version='%(prog)s {}'.format( version ),
    )

    args = argparser.parse_args()
    verbose = args.verbose
    maxage = args.maxage
    code = os.EX_OK

    if args.shutdown or 0 == args.shutdown:
        pid = args.shutdown
        if 0 == pid:
            try:
                fd = open( args.pidlog, 'r' )
            except: pass
            else:
                pid = int( fd.read() )
                fd.close()
        verbose and sys.stderr.write( "Sending SIGALRM to process {}\n".format( pid )
            if pid else "Nothing to stop\n" )
        if pid:
            try:
                os.kill( pid, signal.SIGALRM )
            except OSError as e:
                sys.stderr.write( "{}: {}\n".format( prog, str(e) ))
            if code == os.EX_OK: code = e.errno
        sys.exit( code )

    sock = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
    streams = { 'log': args.log, sys.stdin: None, sys.stdout: args.stdout,
        sys.stderr: args.stderr
    }
    # get min( args.timeout, args.maxage )
    idle = duration = maxage if maxage and (maxage < args.timeout or not args.timeout) \
            else args.timeout
    track = ''

    for stream in streams:
        s = streams[ stream ]
        if not s: continue
        isstr = type(stream) is str
        sname = '<'+ stream +'>' if isstr else stream.name
        track += "redirecting {} to {} ..".format( sname, s )
        mode = 'ba'
        if os.path.exists( s ):
            # handle eg. /dev/stdout
            if os.st.S_ISCHR( os.stat( s ).st_mode ):
                mode = 'bw'
            elif not os.path.isfile( s ):
                import errno
                sys.stderr.write( "{}{}: {} stream must be a regular or character"
                    " special file\n".format( track + '\n' if verbose else '',
                        prog, sname ))
                if code == os.EX_OK: code = errno.EINVAL
                track = ''
                continue
        try:
            fd = open( s, mode )
            if isstr:
                streams[ stream ] = fd
                track += "OK\n"
                continue
            streams[ stream ] = stream
            os.dup2( fd.fileno(), stream.fileno() )
            fd.close()
        except OSError as e:
            sys.stderr.write( "{}{}: {}. can't redirect {} stream\n"
                .format( track + '\n' if verbose else '', str(e), prog, sname ))
            if code == os.EX_OK: code = e.errno
            track = ''
            continue
        if track: track += 'OK\n'

    track += 'binding to socket {} ..'.format( args.socket )
    retries = 5
    while True:
        try:
            sock.bind( args.socket )
            break
        except OSError as e:
            import errno, time
            msg = "{}{}: {}"
            if e.errno == errno.EADDRINUSE:
                try:
                    sock.connect( args.socket )
                except:
                    if os.st.S_ISSOCK( os.stat( args.socket ).st_mode ):
                        os.remove( args.socket )
                        time.sleep( 0.1 )
                        retries -= 1
                        if retries: continue
                    else:
                        msg = "{}{}: can't bind to non socket file"
                else:
                    sock.close()
            sys.stderr.write( (msg + '\n').format( track + '\n' if verbose else '',
                prog, str(e) ))
            if code == os.EX_OK: code = e.errno
            track = ''
            break

    if args.deamonize:
        track += ('OK' if track else '') + '\ndetaching from tty. deamonizing ..'
        try:
            if os.fork(): sys.exit()
            if os.fork(): sys.exit()
            os.setsid()
            os.umask(0)
            track += "OK\nprocess {}\nchanging cwd to {} ..".format( os.getpid(), root )
            os.chdir( root )
            for stream in streams:
                if streams[ stream ]: continue
                streams[ stream ] = stream
                track += "OK\nredirecting {} to {} ..".format( stream.name, os.devnull )
                fd = open( os.devnull, 'w' )
                os.dup2( fd.fileno(), stream.fileno() )
                fd.close()
        except OSError as e:
            sys.stderr.write( "{}{}: {}. can't deamonize\n".format(
                track + '\n' if verbose else '', prog, str(e) ))
            if code == os.EX_OK: code = errno.EINVAL
            track = ''
    bufsize = os.stat( args.socket ).st_blksize
    # stdin = streams[ sys.stdin ] or sys.stdin
    # stdout = streams[ sys.stdout ] or sys.stdout
    stderr = streams[ sys.stderr ] or sys.stderr
    log = streams[ 'log' ]

    if verbose:
        if track: track += 'OK\n'
        stderr.write( track + 'socket timeout: {}\nprocess max-age: {}\n'\
            'process ID: {}\n'.format( str(args.timeout) + 's' if args.timeout else\
            "+Inf", str(duration) + 's' if duration else "+Inf", os.getpid()
        ))
    try:
        fd = open( args.pidlog, 'w' )
    except OSError as e:
        sys.stderr.write( "{}: {}. can't log pid, continuing..\n".format(
            prog, str(e) ))
    else:
        fd.write( str(os.getpid()) )
        fd.close()
    
    if code != os.EX_OK:
        sys.stderr.write( '{}: exiting due to previous errors\n'.format( prog ))
        sys.exit( code )

    def kill( sig, stack ):
        if sig:
            duration = args.maxage if args.maxage and maxage < args.maxage else idle
            duration -= signal.getitimer( signal.ITIMER_REAL )[0]
            duration and ( args.deamonize and os.isatty( stderr.fileno() ) or \
                stderr.write( "Exhausted after {}s\n".format( duration )) )
        else:
            stderr.write( "Exiting immediately\n" )
        for s in streams:
            if not streams[ s ] or streams[ s ].closed: continue
            streams[ s ].close()
        sock.close()
        os.remove( args.socket )
        os.remove( args.pidlog )
        sys.exit()

    kill( None, None ) if duration < 0 else signal.signal( signal.SIGALRM, kill )
    while True:
        duration and signal.setitimer( signal.ITIMER_REAL, duration )
        log.write( sock.recv( bufsize ) )
        log.flush()
        if maxage:
            maxage -= duration - signal.getitimer( signal.ITIMER_REAL )[0]
            duration = duration if duration < maxage else maxage


if "__main__" == __name__:
    try:
        main()
    except KeyboardInterrupt:
        pass
