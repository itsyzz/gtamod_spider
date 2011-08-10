# -*- coding: gb2312 -*-
import re

from time import strftime

import urllib2

import modinfo

from modinfospider import Spider

import spiderutils

from spiderutils import pause
        
class SpiderAtGTABBS(Spider):
    """Recognize as Spider"""
    pass


class SpiderTopicPage(SpiderAtGTABBS):
    """
        Get specific topic links
        Collect info from www.gtabbs.com
    """
    
    def __init__(self, link):
        self.link = link
        self.content = spiderutils.openurlex(link).read() 
        #default encode at GTABBS.com is utf-8, re-encode in gb2312
        self.content = self.content.decode('utf-8').encode('gb2312', 'replace')
        self.info = {"link" : "http://www.gtabbs.com/"}
        
    def __del__(self):
        pass

    def get_topics(self):
        Lmst = re.findall(r'<a href="gta-\S+.html" name="readlink"', self.content)
        rList = []
        for i in range(len(Lmst)):
            nLink = Lmst[i].replace('<a href="', self.info["link"])
            nLink = nLink.replace('" name="readlink"',"")
            rList.append(nLink)
        if rList:
            return rList
        else:
            return "No link found."

    
class SpiderTopicContent(SpiderAtGTABBS):
    """Get specific info from certain link"""
    
    def __init__(self, link):
        self.link = link
        self.content = spiderutils.openurlex(link).read() 
        #default encode at GTABBS.com is utf-8, re-encode in gb2312
        self.content = self.content.decode('utf-8').encode('gb2312', 'replace')
        
        self.kwd = {"attachment":'href="job.php?action=download&aid'}
        
        mst = re.search(r'<div class="readContent">', self.content)
        med = re.search(r'<div id="mark_tpc"', self.content)
        if mst is not None and med is not None:
            self.main_topic_content = self.content[mst.start() : med.end()]
        else:
            pass

    def __del__(self):
        pass

    def detect_attachment(self):
        if self.kwd["attachment"] in self.main_topic_content:
            return True
        else:
            return False

    def get_name(self):
        mat = re.search('<td><h1 id="subject_tpc" class="read_h1">[^<]+</h1></td>', self.content)
        if mat is not None:
            return self.content[mat.start() + len('<td><h1 id="subject_tpc" class="read_h1">') : mat.end() - len('</h1></td>')]
        else:
            return "No name found."

    def get_publisher(self):
        mst = re.search('<a href="u/\d+">', self.content)
        med = re.search('<a href="u/\d+">[^<]+</a>', self.content)
        if mst is not None and mst is not None:
            return self.content[mst.end() : med.end() - len('</a>')]
        else:
            return "No publisher found."

    def get_img(self):
        Lmat = re.findall(r'<img src="http://s10.opengta.org/attachments/\S+" border="0"', self.main_topic_content)
        Limgs = []
        for i in range(len(Lmat)):
            nLink = Lmat[i].replace('<img src="', "")
            nLink = nLink.replace('" border="0"',"")
            Limgs.append(nLink)
        if Limgs:
            return Limgs
        else:
            return "No img link found."

    def get_dld(self):
        #todo
        pass

    def get_subsc_date(self):
        #todo
        pass

    def get_gtaver(self):
        return "GTA:SA"

def spider_crawl():
    while True:
        print 'Crawling at gtabbs'
        print 'Please input crawling range/pages(Recommendation: 1 - 300)'
        r = raw_input('Please input: [min], [max] - to ensure range/pages\n->')

        if r.count(',') is not 1:
            print 'Please input with specific format: [min], [max]'
            pause()
            continue
        
        st, ed = r.split(',')
        st, ed = st.strip(), ed.strip()
        
        if not (st.isdigit() is True and ed.isdigit() is True and st < ed):
            print 'Please input with specific format: [min], [max]'
            pause()
            continue

        link_pages = ['http://www.gtabbs.com/bbs-141-%d'
                      % i for i in range(int(st), int(ed))]
        for link_page in link_pages:
            link_topics = SpiderTopicPage(link_page).get_topics()
            for link_topic in link_topics:
                spider = SpiderTopicContent(link_topic)
                mod = modinfo.ModInfo(link_topic)
                mod.updatekey('site', 'http://www.gtabbs.com')
                mod.updatekey('link', link_topic)
                mod.updatekey('has_att', spider.detect_attachment())
                mod.updatekey('name', spider.get_name())
                mod.updatekey('type', '')
                mod.updatekey('subtype', '')
                mod.updatekey('ver', spider.get_gtaver())
                mod.updatekey('imglink', spider.get_img())
                mod.updatekey('publisher', spider.get_publisher())
                mod.updatekey('date', strftime('%Y%m%d%H%M%S'))
                mod.updatekey('collecttime', strftime('%Y%m%d%H%M%S'))
                print 'Collected: %s' % link_topic
                #mod.show()
                #break
                
        #modinfo.show()
        filename = 'gtabbs_%s.pkl' % strftime('%Y%m%d%H%M%S')
        modinfo.dump(filename)
        print 'Collect action at gtagarage finished.'
        print 'Data store at file:', filename
        pause()
        break
        

def _test():
    # Please change range
    link_pages = ["http://www.gtabbs.com/bbs-141-%d" % i for i in range(1, 1)]
    for link_page in link_pages:
        link_topics = SpiderTopicPage(link_page).get_topics()
        for link_topic in link_topics:
            checkcont = SpiderTopicContent(link_topic)
            has_attachment = checkcont.detect_attachment()
            name = checkcont.get_name()
            img = checkcont.get_img()
            ver = checkcont.get_gtaver()
            print "%s\n\
                    link:%s\n\
                    has_attachment:%r\n\
                    imgs:%r\n\
                    ver:%s\n" % \
                    (name, link_topic, has_attachment, img, gtaver)
if __name__ == "__main__":
    _test()
