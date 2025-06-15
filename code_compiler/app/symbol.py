class Symbol:
    def __init__(self, address, type, size=1, values=None):
        self.address = address
        self.type = type
        self.size = size
        self.values = values if values else []