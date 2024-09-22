

class DefaultDict(dict):
    def __init__(self, default=None, initial_dict={}):
        super().__init__()
        self.update(initial_dict)
        self.default = default

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.default
    
    def get(self, key, default=None):
        if default is None:
            default = self.default
        return super().get(key, default)
