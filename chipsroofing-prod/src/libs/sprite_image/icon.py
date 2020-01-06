class Icon:
    def __init__(self, url='', name='', position=(), size=()):
        self.url = url
        self._name = name
        self._position = position
        self._size = size

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    def __getitem__(self, item):
        return self._position[item]

    def __bool__(self):
        return bool(self._name and self._position)

    def __str__(self):
        return self._name
