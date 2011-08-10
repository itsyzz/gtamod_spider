"""Mod info collected from web handling.

Mod info collected from web are store in this module.
Actually, data store in a depth-2 dictionary.

Classes:

    ModInfo

Functions:

    show()
    dump()
    load()

Misc variables:

    _modinfo - where mod info be stored at.
    
"""

import cPickle

import os

import os.path


_modinfo = {}

__all__ = ["ModInfo", "show", "dump", "load", "clear"]


class ModInfo(object):
    """Series of mod info operation methods provide here.
    """
    
    global _modinfo

    def __init__(self, link):
        """Auto add link data in collection
        """
        self.link = link
        if _modinfo.has_key(link) is False:
            _modinfo.update({link: {}})

    def remove(self):
        """Remove current mod info from collection
        """
        if _modinfo.has_key(self.link) is True:
            del _modinfo[self.link]       

    def show(self):
        """Display collected info from current class
        """
        print '{%r: %r}' % (self.link, _modinfo[self.link])

    def updatekey(self, key, value):
        """Update specific key in current mod info
        """
        _modinfo[self.link].update({key: value})

    def removekey(self, key):
        """Remove specific key from current mod info
        """
        if _modinfo[self.link].has_key(key) is True:
            del _modinfo[self.link][key]




def show():
    """
    Display all collected info.
    """
    print _modinfo

def dump(fielname):
    """
    Dump data to %curdir\data\%fielname
    """
    if os.path.exists('data') is not True:
        os.mkdir('data')

    try:
        output = open('data\%s' % fielname, 'wb')
    except IOError as errinfo:
        print 'Dump failed: %s' % errinfo
        return
    
    with output:
        cPickle.dump(_modinfo, output , cPickle.HIGHEST_PROTOCOL)


def load(fielname):
    """
    Load data from %curdir\data\%fielname
    """
    if os.path.exists('data') is not True:
        os.mkdir('data')

    try:
        inload = open('data\%s' % fielname, 'rb')
    except IOError as errinfo:
        print 'Load data failed: %s' % errinfo
        return ''
        
    with inload:
        collection_data = cPickle.load(inload)
    return collection_data

def clear():
    """
    Clear stored data, used after dumping data.
    """
    _modinfo = {}


def _showhelp():
    import modinfo
    help(modinfo)
    del modinfo
    
def _test():
    x = ModInfo('http://www.test.com')
    x.updatekey('1', '2')
    x.updatekey('1', None)
    x.updatekey('name', 'test')
    x.removekey('1')
    x.removekey('unexist')
    x.removekey('name')
    x.show()
    show()
    x.remove()
    del x
    show()
    clear()
    


if __name__ == '__main__':
    _showhelp()
    #_test()

    
    
    
    
