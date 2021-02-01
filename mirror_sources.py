class MirrorSourceList(list):
    def __init__(self, *args, mirror):
        super().__init__()
        self.mirror = mirror
        # for arg in args:
        #     self.append(arg)
    
    def append(self, new_src):
        if self.mirror._Validate(new_src) is not -1:
            return super().append(new_src)
