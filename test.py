import getopt, sys
import glob
import time
import string
import subprocess

def usage():
    s = "Options: \n"
    s += "-d : compile in Debug mode"
    s += "\n-p : test python"
    print(s)

def colorCode(q):
    return [ "\033[41m%s\033[0m", "\033[31m%s\033[0m", "%s", "\033[32m%s\033[0m" ][q+2] 
 
def colorTestResult(r):
    q = {'+': 1, '?':0, False: -1, True: 1}
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
        #  print(_t, type(received))
        received = _t(received)
        #  print(_t)
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
 
def do_test(exc_str):
    in_files = sorted(glob.glob("input*"))
    out_files = sorted(glob.glob("output*"))
    print(in_files, out_files)
    
    retlist = []
    for inf, outf in zip(in_files, out_files):
        print("")
        print("="*10)
        print("="*10)
        print(inf, outf)
        with open(inf) as f:
            input_content = f.read()
            f.seek(0)
            p = subprocess.Popen(exc_str, stdout=subprocess.PIPE, stdin=f, shell=True)
            recv =  p.stdout.read()

        with open(outf) as of:
            correct_answer = of.read()
            print("Input")
            print(prettyStr(input_content.rstrip()))
            print("Expected:")
            print(prettyStr(correct_answer.rstrip()))
            print("-"*10)
            print("Received:")
            print(prettyStr(recv.rstrip()))
            ret_comp = tc_equal(correct_answer, recv)

            print("Success: " + colorTestResult(ret_comp))
            retlist.append(colorTestResult( "+" if ret_comp else "-"))

    print("\n\n" + "="*20 + "\nSummary: ")
    print(" ".join(retlist))



            #  print("Successful? " + colorTestResult(tc_equal(correct_answer, recv)))

def compile_cpp(DBG):
    exc_str = 'g++ -std=c++11 ' + DBG + ' -Wall A.cc -o A.exe'
    print(exc_str)
    subprocess.call(exc_str, shell=True)

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
    if(not use_py):
        compile_cpp(DBG)
        exc_str = './A.exe'
    else:
        exc_str = "python A.py"    

    do_test(exc_str)


if __name__ == '__main__':
    main()
    #  do_test()
