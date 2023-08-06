class VjaError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __repr__(self):
        return f'VjaError("{self.msg}")'

    def __str__(self):
        return self.msg
