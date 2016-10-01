import requests
import sys

if len(sys.argv) <= 1:
    print 'Usage: python test.py $FILE_NAME'
    exit(1)

url = 'http://localhost:' + sys.argv[2] + '/' if len(sys.argv) == 3 else 'http://localhost:8986/'
fname = sys.argv[1]

def read_file(fname):
    f = open(fname, 'r')
    result = f.read()
    f.close()
    return result

if __name__ == '__main__':
    data = read_file(fname)
    
    print 'data:'
    print data

    req = requests.post(url, data=data)

    print 'Response:'
    print req.text
