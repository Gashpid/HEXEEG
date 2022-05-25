import random

class Create():
    def __init__(self,name,*args):
        dic,lic = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890!"#$%&/()=-_|°?¿',''
        for i in range(8): lic += random.choice(dic)
        name = name.encode('utf-32')
        lic = lic.encode('utf-32')
        f = open('lic.bin','wb')
        f.write(lic); f.close()
        self.Name(name)

    def Name(self,name,*args):
        f = open('usr.bin','wb')
        f.write(name); f.close()
        
        
Create('H3XEEG')
