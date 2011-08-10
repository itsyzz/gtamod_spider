import re

from time import strftime

import urllib2

import modinfo

from modinfospider import Spider

import spiderutils

from spiderutils import pause



class SpiderAtGTAGarage(Spider):
    pass


class SpiderLinkPage(SpiderAtGTAGarage):
    """collect info from www.gtagarage.com"""
    
    def __init__(self, link):
        self.data = {"link":link}
        self.content = spiderutils.openurlex(link).read()
        self.kwd = {"authorlink":"www.gtagarage.com/users/profile.php?M=",
                    "dldlink":"www.gtagarage.com/mods/download.php?f=",
                    "imglink":"http://media.gtanet.com/gtagarage/files/image_%s.jpg"}
        #Unconcident tag:
        #This mod has been removed
        #The mod you requested could not be found

    def __del__(self):
        pass

    def get_mod_dldlink(self):
        mst = re.search(r'<td align="center"><a href="../mods/download.php\?f=', self.content)
        med = re.search(r'<td align="center"><a href="../mods/download.php\?f=\d+', self.content)
        if mst is not None and med is not None:
            self.data["dldlink"] = format("%s%s" % (self.kwd["dldlink"], self.content[mst.end():med.end()]))
            return self.data["dldlink"]
        else:
            return "No download link found."

    def get_mod_author(self):
        mst = re.search(r'<td><a href="../users/profile.php\?M=\d+">', self.content)
        med = re.search(r'<td><a href="../users/profile.php\?M=\d+">\w+', self.content)
        if mst is not None and med is not None:
            self.data["author"] = self.content[mst.end():med.end()]
            return self.data["author"]
        else:
            return "No author found."

    def get_mod_authorlink(self):
        mst = re.search(r'<td><a href="../users/profile.php\?M=', self.content)
        med = re.search(r'<td><a href="../users/profile.php\?M=\d+', self.content)
        if mst is not None and med is not None:
            self.data["authorlink"] = format("%s%s" % (self.kwd["authorlink"], self.content[mst.end():med.end()]))
            return self.data["authorlink"]
        else:
            return "No authorlink found."

    def get_mod_name(self):
        mst = re.search(r'</div><span id="newstitle">', self.content)
        med = re.search(r'</div><span id="newstitle">[ a-zA-Z0-9_]+', self.content)
        if mst is not None and med is not None:
            self.data["mod_name"] = self.content[mst.end():med.end()]
            return self.data["mod_name"]
        else:
            return "No mod name found."

    def get_mod_type(self):
        lst = re.findall(r'<a href="http://www.gtagarage.com/mods/browse.php\?C=\d+">[^<]+</a>', self.content)
        if lst:
            st = lst[0].find('">') + len('">')
            ed = lst[0].find('</a>')
            self.data["mod_type"] = lst[0][st:ed]
            return self.data["mod_type"]
        else:
            return "No mod type found"

    def get_mod_subtype(self):
        lst = re.findall(r'<a href="http://www.gtagarage.com/mods/browse.php\?C=\d+">[^<]+</a>', self.content)
        if lst:
            st = lst[1].find('">') + len('">')
            ed = lst[1].find('</a>')
            self.data["mod_subtype"] = lst[1][st:ed]
            return self.data["mod_subtype"]
        else:
            return "No mod subtype found"
            
    def get_mod_gtaver(self):
        mst = re.search(r'<td><img src="http://media.gtanet.com/gtagarage/images/icons/\d+.png" alt="', self.content)
        med = re.search(r'<td><img src="http://media.gtanet.com/gtagarage/images/icons/\d+.png" alt="[ a-zA-Z0-9_]+', self.content)
        if mst is not None and med is not None:
            self.data["mod_gtaver"] = self.content[mst.end():med.end()]
            return self.data["mod_gtaver"]
        else:
            return "No mod gta version found"

    def get_mod_status(self):
        mst = re.search(r'<td><b>Status:</b></td>\s+<td>', self.content)
        med = re.search(r'<td><b>Status:</b></td>\s+<td>[ a-zA-Z0-9_]+', self.content)
        if mst is not None and med is not None:
            self.data["mod_status"] = self.content[mst.end():med.end()]
            return self.data["mod_status"]
        else:
            return "No mod status found"        

    def get_mod_lastupdated(self):
        mst = re.search(r'<td><b>Last Updated:</b></td>\s+<td>', self.content)
        med = re.search(r'<td><b>Last Updated:</b></td>\s+<td>[ a-zA-Z0-9_]+', self.content)
        if mst is not None and med is not None:
            self.data["mod_lastupdated"] = self.content[mst.end():med.end()]
            return self.data["mod_lastupdated"]
        else:
            return "No mod last updated date found" 

    def get_mod_imglink(self):
        mitered = re.finditer(r'<img src="http://media.gtanet.com/gtagarage/files/thumb_\d+.jpg" class="thumbnail" />', self.content)
        self.data["mod_images"] = []
        for med in mitered:
            imglink = format(self.kwd["imglink"] % self.content[(med.start() + len('<img src="http://media.gtanet.com/gtagarage/files/thumb_')):(med.end() - len('.jpg" class="thumbnail" />'))])
            self.data["mod_images"].append(imglink)
        if self.data["mod_images"]:
            return self.data["mod_images"]
        else:
            return "No mod images foud"

def spider_crawl():
    while True:
        print 'Crawling at gtagarage'
        print 'Please input crawling range/index(Recommendation: 0 - 20000)'
        r = raw_input('Please input: [min], [max] - to ensure range/index\n->')

        if r.count(',') is not 1:
            print 'Please input with specific format: [min], [max]'
            pause
            continue
        
        st, ed = r.split(',')
        st, ed = st.strip(), ed.strip()
        
        if not (st.isdigit() is True and ed.isdigit() is True and st < ed):
            print 'Please input with specific format: [min], [max]'
            pause
            continue

        links = ['http://www.gtagarage.com/mods/show.php?id=%d'
                 % i for i in range(int(st), int(ed))]
        for link in links:
            spider = SpiderLinkPage(link)
            mod = modinfo.ModInfo(link)
            mod.updatekey('site', 'http://www.gtagarage.com')
            mod.updatekey('link', link)
            mod.updatekey('authorlink', spider.get_mod_authorlink())
            mod.updatekey('dldlink', spider.get_mod_dldlink())
            mod.updatekey('imglink', spider.get_mod_imglink())
            mod.updatekey('name', spider.get_mod_name())
            mod.updatekey('type', spider.get_mod_type())
            mod.updatekey('subtype', spider.get_mod_subtype())
            mod.updatekey('ver', spider.get_mod_gtaver())
            mod.updatekey('author', spider.get_mod_author())
            mod.updatekey('status', spider.get_mod_status())
            mod.updatekey('date', spider.get_mod_lastupdated())
            mod.updatekey('collecttime', strftime('%Y%m%d%H%M%S'))
            print 'Collected: %s' % link
            #mod.show()
        #modinfo.show()
        filename = 'gtagarage_%s.pkl' % strftime('%Y%m%d%H%M%S')
        modinfo.dump(filename)
        modinfo.clear()
        print 'Collect action at gtagarage finished.'
        print 'Data store at file:', filename
        pause
        break

            
def _test():
    # Please change range
    links = [ 'http://www.gtagarage.com/mods/show.php?id=%d'
              % index for index in range(0)]
    for link in links:
        spider = SpiderLinkPage(link)
        mod_authorlink = spider.get_mod_authorlink()
        mod_author = spider.get_mod_author()
        mod_dldlink = spider.get_mod_dldlink()
        mod_name = spider.get_mod_name()
        mod_gtaver = spider.get_mod_gtaver()
        mod_status = spider.get_mod_status()
        mod_lastupdated = spider.get_mod_lastupdated()
        mod_imglink = spider.get_mod_imglink()
        mod_type = spider.get_mod_type()
        mod_subtype = spider.get_mod_subtype()
        print "\tMod Name:%s - suitVersion:%s at:%s/%s\r\n\t\tAuthor:%s(%s)\r\n\t\tstatus:%s\r\n\t\tlastupdated:%s\r\n\t\tdldlink:%s\r\n\t\timg:%r"\
              % (mod_name, mod_gtaver,mod_type, mod_subtype,
                 mod_author, mod_authorlink, mod_status, mod_lastupdated,
                 mod_dldlink, mod_imglink)    

if __name__ == "__main__":
    _test()

