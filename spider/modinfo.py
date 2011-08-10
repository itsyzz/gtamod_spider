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

_modinfo = {}

__all__ = ["ModInfo", "show", "dump", "load"]


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

def dump():
    """
    Dump data to current dictionary in collection.pkl
    """
    output = open('collection.pkl', 'wb')
    with output:
        cPickle.dump(_modinfo, output , cPickle.HIGHEST_PROTOCOL)


def load():
    """
    Load data from collection.pkl
    """
    inload = open('collection.pkl', 'rb')
    with inload:
        collection_data = cPickle.load(inload)
    return collection_data


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
    x.remove()
    del x


if __name__ == '__main__':
    _showhelp()
    _test() 
    
    
    
    
    
