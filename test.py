import getopt, sys
import glob
import time
import string
import subprocess

def usage():
    s = "Options: \n"
    s += "-d : compile in Debug mode"
    s += "-p : test python"
    print(s)

def colorCode(q):
    return [ "\\033[1;41m%s\\033[0m", "\\033[1;31m%s\\033[0m", "%s", "\\033[1;32m%s\\033[0m" ][q+2] 
 
def colorTestResult(r):
    q = {'+': 1, '?':0 }
    return colorCode( q[r] if r in q else -1 ) % r
 
def prettyStr(x):
    if type(x) == str:
        return '"%s"' % x
    elif type(x) == tuple:
        return '(%s)' % string.join( (prettyStr(y) for y in x), ',' )
    else:
        return str(x)
 
def tc_equal(expected, received):
    try:
        _t = type(expected)
        print(_t, type(received))
        received = _t(received)
        print(_t)
        if _t == list or _t == tuple:
            print("checking list or tuple")
            if len(expected) != len(received): return False
            return all(tc_equal(e, r) for (e, r) in zip(expected, received))
        elif _t == float:
            eps = 1e-9
            if abs(expected - received) < eps: return True
            if abs(received) > abs(expected) * (1.0 - eps) and abs(received) < abs(expected) * (1.0 + eps): return True
        elif isinstance(expected, basestring):
            exp_lines = expected.splitlines()
            rec_lines = received.splitlines()
            if len(exp_lines) == 1:
                return expected == received
            else:
                return tc_equal(exp_lines, rec_lines)
        else:
            print("check equality")
            return expected == received
    except:
        return False
 

def do_test():
    in_files = glob.glob("input*")
    out_files = glob.glob("output*")
    print(in_files, out_files)
    
    for inf, outf in zip(in_files, out_files):
        print(inf, outf)
        with open(inf) as f:
            p = subprocess.Popen("python myprog.py", stdout=subprocess.PIPE, stdin=f)
            recv =  p.stdout.read()

        with open(outf) as of:
            s = of.read()
            print(s)
            print(recv)
            print(s == recv)
            print tc_equal(s, recv)


def main():
    DBG = "";
    use_py = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dp" )
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-d':
            DBG = "-DDEBUG"
        if o == '-p':
            use_py = True

    print(DBG, use_py)

    test_python()


if __name__ == '__main__':
    # main()
    do_test()
