import re

import urllib2

from modinfospider import Spider

import spiderutils


class SpiderAtGTAinside(Spider):
    """Recognize as spider"""
    def __init__(self):
        pass


class SpiderTopicPage(SpiderAtGTAinside):
    """
    """
    #<B>GTA IV</B> - for gta iv
    #<B>GTA:SanAndreas</B> - for gta sa
    #<B>GTA:ViceCity</B> - for gta vc
    #<B>GTA III</B> - for gta III
    #<B>GTA:LCS</B - for gta lcs
    #<a href="download.php?do=cat&id=399">Airplanes (9)</a></TD>
    def __init__(self, link):
        self.link = link
        self.cont = spiderutils.openurlex(link).read()
        self.info = {
            "homepage":"http://www.gtainside.com",
            "subtypelink":"/download.php?do=cat&id="
            }
        self.ver = {
            "GTA IV": "IV",
            "GTA:SanAndreas": "SA",
            "GTA:ViceCity": "VC",
            "GTA III": "III",
            "GTA:LCS": "LCS",
            "GTA:VCS": "VCS",
            "IV": "GTA IV",
            "SA": "GTA:SanAndreas",
            "VC": "GTA:ViceCity",
            "III": "GTA III",
            "LCS": "GTA:LCS",
            "VCS": "GTA:VCS"
            }

    def __del__(self):
        pass

    def narrow_collect_range(self):
        mst = re.search(r'<img src="gfx/menu_left_downloads.jpg" alt="0">'
                        , self.cont)
        med = re.search(r'<img src="gfx/menu_left_games.jpg" alt="0">'
                        , self.cont)
        if mst is not None and med is not None:
            self.cont = self.cont[mst.start():med.end()]
        else:
            raise SpiderError(0)

    def set_type_info(self):
        length = len(self.cont)
        index = 0
        cont = self.cont[:]
        while index <= length:
            print index, index <= length, length
            med = re.search(r'</TABLE>', cont[index:])
            mst = re.search(r'<B>([^<]+)</B>', cont[index:])

            if mst is not None and med is not None:
                curtypename = mst.group(1)
                st, ed = mst.start(), med.end()
                
            #else:
            #    raise SpiderError(0)
                print cont
            

                mlist = re.findall(\
                    r'<a href="download.php\?do=cat&id=(\d+)">([^<]+)</a>'\
                    , cont[st:ed])
                for id, subtype in mlist:
                    subtypename = re.sub(r' \(\d+\)', '', subtype)
                    subtypelink = format("%s%s%s" % \
                           (self.info["homepage"], self.info["subtypelink"], id))
                    self.info[subtypelink] = {"type":self.ver[curtypename],
                                              "name":subtypename,
                                              "id":id}
                index = med.end()
                cont = cont[index:]
                length = len(cont)
            index = index + 1
            
        print self.info
                



class SpiderError(Exception):
    def __init__(self, errcode):
        self.errcode = errcode
        self.reason = [
            "Cannot specific web page, please check url or review \
page sourcecode."
            ]

    def __str__(self):
        return '<spider error at http://www.gtainisde.com: %s>' % \
               self.reason[self.errcode]



if __name__ == '__main__':
    obj = SpiderTopicPage("http://www.gtainside.com")
    obj.narrow_collect_range()
    obj.set_type_info()








        
        
