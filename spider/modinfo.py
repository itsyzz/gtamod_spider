class CustomMod(object):
    """elements which mods must have"""
    
    def __init__(self, gta_ver, mod_type, mod_subtype):
        self.gta_ver = gta_ver
        self.mod_type = mod_type
        self.mod_subtype = mod_subtype
    
    def __del__(self):
        pass

    def set_gta_ver(self, gta_ver):
        self.gta_ver = gta_ver

    def set_mod_type(self, mod_type):
        self.mod_type = mod_type

    def set_mod_subtype(self, mod_subtype):
        self.mod_subtype = mod_subtype


class FromWebMod(CustomMod):
    """elements which mods from web/internet"""

    def __init__(self, orgi_link, dnld_link, img_link, author_link, author):
        self.orgi_link = orgi_link
        self.dnld_link = dnld_link
        self.img_link = img_link
        self.author_link = author_link
        self.author = author

    def __del__(self):
        pass

        
