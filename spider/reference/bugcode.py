############################################################
            #it has a bug that use too much recursion
            infoparttern = re.compile(
                r"""
                Title:</B></TD>\s+                  # get title parttern
                <TD><B>(.*?)</B></TD>               # get title/name.
                [^^]+?                           # skip to
                Author:</TD>\s+                     # get author parttern
                <TD>(.*?)</TD>                      # get author
                [^^]+?                           # skip to
                Date:</TD>\s+                       # get date parttern
                <TD>(.*?)</TD>                      # get date
                [^^]+?                           # skip to
                Image:</TD>\s+                      # get image link parttern
                <TD><im3g\ src="(.*?)"><BR><BR></TD> #
                """, re.VERBOSE|re.DOTALL)
                #Image:</TD>\s+                      # get image link parttern
                #<TD><img\ src="(.*?)"<BR><BR></TD>  # get image link



###############################################################
            #get search index which do not at the search range
    def set_type_info(self):
        length = len(self.cont)
        index = 0
        test = 0
        while test <= 2:
            test += 1
        #while index <= length:
            #print "index:", index, self.cont[index:index + 100], "len", length
            #curtype = ""
            #st, ed = 0, 0
            #todo : bugs here
            index = index + 1
            med = re.search(r'</TABLE>', self.cont[index:])
            mst = re.search(r'<B>([^<]+)</B>', self.cont[index:])
            print self.cont[med.start():med.end()], "e|e", med.end()
            print self.cont[med.start():med.end()] in self.cont[index:]
            print self.cont[index:]
            #if do set index as previous value
            if mst is not None and med is not None:
                curtypename = mst.group(1)
                st, ed = mst.start(), med.end()
                #print "a",index
                index = med.end()
                #print "b",index
                #print self.cont[index:index+100]
            else:
                raise SpiderError(0)
            

            mlist = re.findall(\
                r'<a href="download.php\?do=cat&id=(\d+)">([^<]+)</a>'\
                , self.cont[st:ed])
            for id, subtype in mlist:
                subtypename = re.sub(r' \(\d+\)', '', subtype)
                subtypelink = format("%s%s%s" % \
                       (self.info["homepage"], self.info["subtypelink"], id))
                self.info[subtypelink] = {"type":self.ver[curtypename],
                                          "name":subtypename,
                                          "id":id}
            #print "c",index
            
            #print "d",index
            
        #print self.info








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
            raise SpiderError("Cannot specific web page, please check url or review page sourcecode.")



        i, length = 0, len(ver_names)
        while i < length:
            types = re.findall(
                r'<a href="download.php\?do=cat&id=(\d+)">(.*?)</a>'
                , self.cont[sts[i]:eds[i]])
            for type_id, type_orginame in types:
                type_name = re.sub(r' \(\d+\)', '', type_orginame)
                type_link = format("%s%s%s" %
                                   (self.info["homepage"],
                                    self.info["type_link"],
                                    type_id))
                self.info[type_link] = {"ver":self.ver[ver_names[i]],
                                        "type":type_name,
                                        "id":type_id}
            i += 1
