class V2rayException(Exception):

    def __init__(self, msg=None):
        super(V2rayException, self).__init__(msg)
        self.msg = msg