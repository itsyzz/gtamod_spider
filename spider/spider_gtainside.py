import re

import urllib2

from modinfospider import Spider

import spiderutils

        

info = {}
modinfo = {}

class SpiderAtGTAinside(Spider):
    """Recognize as spider"""
    def __init__(self):
        pass

    def __del__(self):
        pass


class SpiderHomePage(SpiderAtGTAinside):
    """Get specific info at gtainside homepage, 
        such as version, type, links, etc.
    """
    def __init__(self):
        self.cont = spiderutils.openurlex("http://www.gtainside.com").read()
        self.info = {
            "homepage":"http://www.gtainside.com",
            "type_link":"/en/download.php?do=cat&main_cat="
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
            raise SpiderError(
                "Cannot specific web page, \
                please check url or review page sourcecode.")

    def set_type_info(self):
        mstiter = re.finditer(r'<B>(.*?)</B>', self.cont)
        mediter = re.finditer(r'</TABLE>', self.cont)
        if mstiter is not None and mediter is not None:
            ver_names, sts, eds = [], [], []
            for mst in mstiter:
                ver_names.append(mst.group(1))
                sts.append(mst.start())
            for med in mediter:
                eds.append(med.end())
        else:
            raise SpiderError(
                "Cannot specific web page, \
                please check url or review page sourcecode.")

        index, length = 0, len(ver_names)
        while index < length:
            i = index
            index += 1
            types = re.findall(
                r'<a href="download.php\?do=cat&id=(\d+)">(.*?)</a>'
                , self.cont[sts[i]:eds[i]])
            for type_id, type_orginame in types:
                global info
                type_name = re.sub(r' \(\d+\)', '', type_orginame)
                type_link = ("%s%s%s" %
                             (self.info["homepage"],
                              self.info["type_link"],
                              type_id))
                info[type_link] = {"ver": self.ver[ver_names[i]],
                                   "type": type_name,
                                   "id": type_id}



class SpiderTopicPage(SpiderAtGTAinside):
    """Get specific info at gtainside topicpage.
    """

    def __init__(self, link, depth = 0):
        self.link = link
        self.depth = depth
        self.info = {
            "homepage": "http://www.gtainside.com/en",
            "infopage": "/download.php?do=comments&id=",
            "dldlink": "/download.php?do=download&id=",
            "imglink": "/"}
        self.cont = spiderutils.openurlex(link).read()

    def set_maximum_depth(self):
        mat = re.search(r'<a href=download.*?start=(\d+).*?</a> <BR><BR>'
                        , self.cont)
        if mat is not None:
            self.maximum_depth = mat.group(1)
        else:
            mat = re.search(r'<B>\[1\]</B> <BR><BR>', self.cont)
            if mat is not None:
                self.maximum_depth = 1
            else:
                raise SpiderError(
                    "Cannot specific maximum page/depth, \
                    please comfirm the code")
            
    def get_info(self):
        cur_depth = 0
        fac_depth = (
            self.maximum_depth
            if (self.depth >= self.maximum_depth or self.depth == 0)
            else self.depth)
        while cur_depth < fac_depth:
            cur_link = format("%s&start=%d&orderBy=" %
                              (self.link, cur_depth * 7))
            self.cont = spiderutils.openurlex(cur_link).read()
            cur_depth += 1

            # collect info
            name_iter = re.finditer(
                r'Title:</B></TD>\s+<TD><B>(.*?)</B></TD>', self.cont)
            author_iter = re.finditer(
                r'Author:</TD>\s+<TD>(.*?)</TD>', self.cont)
            date_iter = re.finditer(
                r'Date:</TD>\s+<TD>(.*?)</TD>', self.cont)
            img_iter = re.finditer(
                r'Image:</TD>\s+<TD><img src="(.*?)"><BR><BR></TD>', self.cont)
            id_iter_forview = re.finditer(
                r'<BR><center><a href="[\D]+(.*?)"><.*?><B>DOWNLOAD</B>'
                , self.cont)
            id_iter_fordld = re.finditer(
                r'<BR><center><a href="[\D]+(.*?)"><.*?><B>DOWNLOAD</B>'
                , self.cont)
            mod_name = (name.group(1) for name in name_iter)
            mod_author = (author.group(1) for author in author_iter)
            mod_date = (date.group(1) for date in date_iter)
            mod_img = (
                ("%s%s%s" % (
                    self.info["homepage"],
                    self.info["imglink"],
                    imglink))
                for imglink in (imglink.group(1) for imglink in img_iter))
            mod_infopage = (
                ("%s%s%d" % (
                    self.info["homepage"],
                    self.info["infopage"],
                    int(index))
                for index in (index.group(1) for index in id_iter_forview)))
            mod_dldlink = (
                ("%s%s%d" % (
                    self.info["homepage"],
                    self.info["dldlink"],
                    int(index))
                 for index in (index.group(1) for index in id_iter_fordld)))

            # store info
            global modinfo
            for mod_infopage in mod_infopage:
                modinfo[mod_infopage] = {}
                xup = lambda k, v: modinfo[mod_infopage].update({k: v})
                xup("link", mod_infopage)
                xup("name", mod_name.next())
                xup("author", mod_author.next())
                xup("date", mod_date.next())
                xup("img", mod_img.next())
                xup("dldlink", mod_dldlink.next())
                try:
                    xup("ver", get_ver_fromlink(self.link))
                    xup("type", get_type_fromlink(self.link))
                except TypeError:
                    print "Cannot get ver, type"
                
            
        for k, v in modinfo.items():
            print '\t', k
            print '\t\t', v
  
def get_type_fromlink(link):
    return info[link]["type"]

def get_ver_fromlink(link):
    return info[link]["ver"]


class SpiderError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return '<spider error at http://www.gtainisde.com>'



if __name__ == '__main__':
    homepage = SpiderHomePage()
    homepage.narrow_collect_range()
    homepage.set_type_info()

    topicpage_links = info.keys()
    #for topicpage_link in topicpage_links:
    #    topicpage = SpiderTopicPage(topicpage_link)
    #    topicpage.set_maximum_depth()
    #    topicpage.get_info()
    #debug:
    topicpage = SpiderTopicPage(topicpage_links[10], 2)
    topicpage.set_maximum_depth()
    topicpage.get_info()







