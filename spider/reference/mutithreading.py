#-*- encoding: gb2312 -*-
import string, threading, time

def test():
    print "a"

def thread_main(a):
    global count, mutex
    # ����߳���
    threadname = threading.currentThread().getName()
    b =None
    for x in xrange(0, int(a)):
        # ȡ����
        a = mutex.acquire()
        count += 1
        # �ͷ���
        b = mutex.release()
        
        
        #print "t:%r\n" % count
        #print "threadname:%r\nx:%r\ncount:%r|\n" % (threadname, x, count)
        time.sleep(0.3)
    
def main(num):
    global count, mutex
    threads = []
    threading.settrace(test()) 
    count = 1
    # ����һ����
    mutex = threading.Lock()
    # �ȴ����̶߳���
    for x in xrange(0, num):
        threads.append(threading.Thread(target=thread_main, args=(5,), name = 'omg%d' % x))
    #print threads
    # ���������߳�
    for t in threads:
        #print t
        t.start()
        print t.isAlive()
    
    # ���߳��еȴ��������߳��˳�
    for t in threads:
        print t.isAlive()
        t.join(0.01)
        print t.isAlive()
    
    
if __name__ == '__main__':
    # ����4���߳�
    main(5)
    print "over"

