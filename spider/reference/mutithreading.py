#-*- encoding: gb2312 -*-
import string, threading, time

def test():
    print "a"

def thread_main(a):
    global count, mutex
    # 获得线程名
    threadname = threading.currentThread().getName()
    b =None
    for x in xrange(0, int(a)):
        # 取得锁
        a = mutex.acquire()
        count += 1
        # 释放锁
        b = mutex.release()
        
        
        #print "t:%r\n" % count
        #print "threadname:%r\nx:%r\ncount:%r|\n" % (threadname, x, count)
        time.sleep(0.3)
    
def main(num):
    global count, mutex
    threads = []
    threading.settrace(test()) 
    count = 1
    # 创建一个锁
    mutex = threading.Lock()
    # 先创建线程对象
    for x in xrange(0, num):
        threads.append(threading.Thread(target=thread_main, args=(5,), name = 'omg%d' % x))
    #print threads
    # 启动所有线程
    for t in threads:
        #print t
        t.start()
        print t.isAlive()
    
    # 主线程中等待所有子线程退出
    for t in threads:
        print t.isAlive()
        t.join(0.01)
        print t.isAlive()
    
    
if __name__ == '__main__':
    # 创建4个线程
    main(5)
    print "over"

