#encoding=utf-8

#由于自己平常看看新闻，又懒的开IE，所以准备用PYTHON开发个采集新闻的程序。发下PYTHON做采集非常好，天生就是作采集的。。以后再写些小的东西来玩下。。。
#用到了twisted ,beautifulsoup, httplib urllib 等。。
   



#####################导入基本模块##############
from twisted.web import client
from twisted.internet import reactor
import sys
from sgmllib import SGMLParser
import re
import urllib
from BeautifulSoup import BeautifulSoup
seturl = 'http://news.baidu.com'
newsinfo = {}
##################导入基本模块结束#########################

###############HTML采集处理###################
class SongParser(SGMLParser):
    '''一级栏目采集'''
    def reset(self):
        SGMLParser.reset(self)
        self.firstlink = []
        self.q_check = 0;


    def start_ul(self, tag):
       
        if tag:
            if tag[0]:
                if tag[0][1] == 'list2':
                    self.q_check = 1

    def handle_data(self, text):
        pass

    def start_a(self,tag):
        if tag:
            if tag[0][1] and self.q_check == 1:
#                bt = '^\/n.+'
                linkcontent = urllib.unquote(tag[0][1])
#                m = re.match(bt,linkcontent)
#                infolink = seturl+m.group()
                infolink = seturl+linkcontent
                self.firstlink.append(infolink)
                
    def end_ul(self):
        self.q_check = 0


class SecParser(SGMLParser):
    '''具体内容采集'''
    def reset(self):
         SGMLParser.reset(self)
         self.info = []
         self.c_check = 0;
        
    def start_div(self,tag):
        if tag:
            if tag[0][1] == 'longabs':
                self.c_check = 1
    
    def handle_data(self, text):
        txt = text.strip()
        if txt and self.c_check:
            self.info.append(txt)
                
            if txt == '':
                return    
            
    def end_div(self):
        self.c_check = 0
        
    def start_td(self,tag):
        if tag:
            if tag[0][1] == 'brief':
                self.c_check = 1
        
    def end_td(self):
        self.c_check = 0
        
            
def printPage(data):
    content = unicode(data,"gbk").encode("utf-8")
    parser = SongParser()
    parser.feed(content)
    
    for link in parser.firstlink:
        f = urllib.urlopen(link)
        data = f.read()
        utf8data = unicode(data,'gbk').encode('utf-8')        
        secparser = SecParser()
        secparser.feed(utf8data)
#        num = 0
        soup = BeautifulSoup(''.join(utf8data))
        title = soup.html.head.title.renderContents()
        content = ",".join(secparser.info)
        print title
        print content
        print link
#        getSites(title,content,link).addCallback(printResult).addErrback(getError)
    reactor.stop()
    
def printError(failure):
    print >>sys.stderr,"Error:",failure.getErrorMessage()
    reactor.stop()


#from twisted.internet import reactor
#from twisted.enterprise import adbapi
#import pyPgSQL.PgSQL as PgSQL
#
#
#def getSites(title,content,link):
#
#    return dbpool.runOperation("insert into newcontent(title,ncontent,link)values('"+title+"','"+content+"','"+link+"')")
##    return dbpool.runQuery("select * from newcontent")
#    
#def printResult(content):
#    print 'success'
#
#def getError(failure):
#    print >>sys.stderr,"Error:",failure.getErrorMessage()
#    reactor.stop()
#        
#        
#dbpool = adbapi.ConnectionPool("pyPgSQL.PgSQL",user="pgsql",\
#    password="" ,host="localhost",database="caiji" ,port="5432")

if len(sys.argv) == 2:
    url = sys.argv[1]
    client.getPage(url).addCallback(printPage).addErrback(printError)
    reactor.run()
    
else:
    print 'url is not empty'
    
#######################HTML采集内容处理结束##################################
