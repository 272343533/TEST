import time
 
def test(a,b):
    print(a)
    sys.stdout.flush()
    time.sleep(1000)
    print(b)
    time.sleep(1000)
    print('���Խ���')
 
if __name__=='__main__':
    test(1,2)