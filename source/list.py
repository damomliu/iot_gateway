from collections import Counter
from collections import Counter

class MirrorSourceList(list):
    def __init__(self, *args, mirror):
        super().__init__()
        self.mirror = mirror
        # for arg in args:
        #     self.append(arg)
    
    def append(self, new_src):
        if self.mirror._Validate(new_src) is not -1:
            super().append(new_src)

            for src in self:
                if src.client == new_src.client:
                    new_src.client = src.client
                    break
            

    @property
    def counter(self): return Counter(src.__class__.__name__ for src in self)
