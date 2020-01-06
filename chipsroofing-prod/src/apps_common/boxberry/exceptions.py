class BoxberryAPIError(Exception):
    @property
    def message(self):
        return self.args[0]
