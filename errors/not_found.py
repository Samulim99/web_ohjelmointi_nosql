class NotFound(Exception):
    def __init__(self, message='Not Found'):
        self.args = (message,)