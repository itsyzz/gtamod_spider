class _spiderAtGTAGarage(spider):
    """collect info from www.gtagarage.com"""
    #Unfortunately, most work can be done by expression, not this stupid ugly code
    
    
    def __init__(self):
        self.garage_url = "http://www.gtagarage.com/"
        self.url_subtype_head = "http://www.gtagarage.com/mods/browse.php?C="
        self.url_subtype_tail = "&State=0&Type=0&Game=0&Order=&Dir=&Thumbs=0&st="
        self.garage_mainpage = ""
        self.Dgarage_info = {"default" : "default"}
        self.link = {"mod" : "http://www.gtagarage.com/mods/show.php?id=",
                     "author" : "http://www.gtagarage.com/users/profile.php?M="}
        self.status = {"wip" : 'http://media.gtanet.com/gtagarage/images/icons/wip.gif',
                       "comp" : 'http://media.gtanet.com/gtagarage/images/icons/comp.gif'}
        self.gtaver = {"I" : "http://media.gtanet.com/gtagarage/images/icons/1.png",
                       "II" : "http://media.gtanet.com/gtagarage/images/icons/2.png",
                       "III" : "http://media.gtanet.com/gtagarage/images/icons/3.png",
                       "VC" : "http://media.gtanet.com/gtagarage/images/icons/4.png",
                       "SA" : "http://media.gtanet.com/gtagarage/images/icons/5.png",
                       "IV" : "http://media.gtanet.com/gtagarage/images/icons/6.png"}
        self.kwd = {"mod_link_head" : '../mods/show.php?id=',
                    "mod_link_tail" : '">',
                    "mod_name_head" : '"><b>',
                    "mod_name_tail" : '</b></a><br />',
                    "mod_authorlink_head" : '../users/profile.php?M=',
                    "mod_authorlink_tail" : '">',
                    "mod_author_head" : '">',
                    "mod_author_tail" : '</a></td>'}
        #<td align="center"><a href="../users/profile.php?M=142898">Chong McBong</a></td>
        
    def __del__(self):
        pass

    def start_at_mainpage(self):
        self.garage_mainpage = urllib2.urlopen(self.garage_url).read()

    def get_type_data(self):
        startat_keywords, endwith_keywords = '<span class="submenu">Mods', '</ul>'
        startat, endwith = 0, 0

        #get specific info part
        Lcontent = self.garage_mainpage.splitlines()
        for curpos in range(len(Lcontent)):
            if startat_keywords in Lcontent[curpos]:
                startat = curpos
                continue
            if startat != 0 and endwith_keywords in Lcontent[curpos]:
                endwith = curpos
                break

        #get specific info, can simply done by expression.
        type_keywords = {"head" : '<li><a href="../mods/browse.php?C=',
                         "tail" : '</a></li>',
                         "start" : '">'}
        
        subtype_keywords = {"head" : '<li class="submenu"><a href="../mods/browse.php?C=',
                            "tail" : '</a>',
                            "start" : '">'}
        
        for content in Lcontent[startat:endwith]:
            type_findpos = content.find(type_keywords["head"])
            if type_findpos != -1:
                type_startpos = content.find(type_keywords["start"], type_findpos + len(type_keywords["head"])) + 2
                type_endpos = content.rfind(type_keywords["tail"])
                type_name, type_ID = content[type_startpos:type_endpos], content[type_findpos + len(type_keywords["head"]):type_startpos - 2]
                self.Dgarage_info[type_name], self.Dgarage_info[type_ID] = type_ID, type_name
                print "\t%s - %smods/browse.php?C=%s" % (type_name, self.garage_url, type_ID)
            subtype_findpos = content.find(subtype_keywords["head"])
            if subtype_findpos != -1:
                subtype_startpos = content.find(subtype_keywords["start"], subtype_findpos + len(subtype_keywords["head"])) + 2
                subtype_endpos = content.rfind(subtype_keywords["tail"])
                subtype_name, subtype_ID = content[subtype_startpos:subtype_endpos], content[subtype_findpos + len(subtype_keywords["head"]):subtype_startpos - 2]
                self.Dgarage_info[subtype_name], self.Dgarage_info[subtype_ID] = subtype_ID, subtype_name
                print "\t\t%s - %smods/browse.php?C=%s" % (subtype_name, self.garage_url, subtype_ID)

        #print self.Dgarage_info.items()

    def subtype_type(self, subtype_name):
        ID = int(self.Dgarage_info[subtype_name])
        return self.Dgarage_info[str(ID - (ID % 10))]
    
    def subtype_mod_amount(self, subtype_name):
        countpage_keywords = '</tr></table><br /><p><a href="javascript:pagejump'
        kwd_start, kwd_end = '&st=', '">'
        subtype_url = format("%s%s%s0" % ( self.url_subtype_head, self.Dgarage_info[subtype_name], self.url_subtype_tail))
        Lcontent = urllib2.urlopen(subtype_url).read().splitlines()
        for content in Lcontent:
            if countpage_keywords in content:
                startat, endwith = content.rfind(kwd_start) + 4, content.rfind(kwd_end)
                return int(content[startat:endwith])
                
    def cat_baseinfo(self, subtype_name, startat, endwith):
        st_kwd, ed_kwd = '<tr class="modrow">', '</tr>'
        curpos = 0
        url = format("%s%s%s%d" % ( self.url_subtype_head, self.Dgarage_info[subtype_name], self.url_subtype_tail, startat))
        Lcont = urllib2.urlopen(url).read().splitlines()

        while curpos < len(Lcont):
            st, ed = 0, 0
            #get specific info part
            for pos in range(curpos, len(Lcont)):
                if st_kwd in Lcont[pos]:
                    st = pos
                    continue
                if st != 0 and ed_kwd in Lcont[pos]:
                    ed = pos
                    curpos = ed
                    break
            if st != 0 and ed != 0:
                status = _spiderAtGTAGarage().get_mod_status(Lcont[st:ed])
                gtaver = _spiderAtGTAGarage().get_mod_gtaver(Lcont[st:ed])
                name = _spiderAtGTAGarage().get_mod_name(Lcont[st:ed])
                link = _spiderAtGTAGarage().get_mod_link(Lcont[st:ed])
                author = _spiderAtGTAGarage().get_mod_author(Lcont[st:ed])
                authorlink = _spiderAtGTAGarage().get_mod_authorlink(Lcont[st:ed])
                print "status:%s\ngtaver:%s\nname:%s\nlink:%s\nauthor:%s\nauthorlink:%s\n" % (status, gtaver, name, link, author, authorlink)
            curpos += 1

    def get_mod_author(self, Lcont):
        for cont in Lcont:
            if self.kwd["mod_authorlink_head"] in cont:
                fpos = cont.rfind(self.kwd["mod_author_head"])
                st = fpos + len(self.kwd["mod_author_head"])
                ed = cont.rfind(self.kwd["mod_author_tail"])
                return cont[st:ed]

    def get_mod_authorlink(self, Lcont):
        for cont in Lcont:
            fpos = cont.find(self.kwd["mod_authorlink_head"])
            if fpos != -1:
                st = fpos + len(self.kwd["mod_authorlink_head"])
                ed = cont.find(self.kwd["mod_authorlink_tail"], st)
                return format("%s%s" % (self.link["author"], cont[st:ed]))

    def get_mod_link(self, Lcont):
        for cont in Lcont:
            fpos = cont.find(self.kwd["mod_link_head"])
            if fpos != -1:
                st = fpos + len(self.kwd["mod_link_head"])
                ed = cont.find(self.kwd["mod_link_tail"], fpos)
                return format("%s%s" % (self.link["mod"], cont[st:ed]))

    def get_mod_name(self, Lcont):
        for cont in Lcont:
            fpos = cont.find(self.kwd["mod_name_head"])
            if fpos != -1:
                st = fpos + len(self.kwd["mod_name_head"])
                ed = cont.find(self.kwd["mod_name_tail"], fpos)
                return cont[st:ed]

    def get_mod_status(self, Lcont):
        for cont in Lcont:
            if self.status["wip"] in cont:
                return "wip"
            elif self.status["comp"] in cont:
                return "comp"
        return "unknown"

    def get_mod_gtaver(self, Lcont):
        #k for k, v in params.items()]                
        for cont in Lcont:
            if self.gtaver["I"] in cont:
                return "I"
            elif self.gtaver["II"] in cont:
                return "II"
            elif self.gtaver["III"] in cont:
                return "III"
            elif self.gtaver["VC"] in cont:
                return "VC"
            elif self.gtaver["SA"] in cont:
                return "SA"
            elif self.gtaver["IV"] in cont:
                return "IV"
        return "Unknown"
        

    def get_mod_type(self, startat, endwith):
        pass

    def get_mod_subtype(self, startat, endwith):
        pass


    #links = [ 'http://www.verycd.com/topics/%d/'%i for i in range(5420,5430)
    #test = spiderAtGTAGarage()
    #test.start_at_mainpage()
    #test.get_type_data()
    #car_amount = test.subtype_mod_amount("Cars")
    #print "There're about %d - %d cars in gtagarage.com, which belong to type %s" % (car_amount, car_amount + 25, test.subtype_type("Cars"))
    #test.cat_baseinfo("Cars", 1, 30)
