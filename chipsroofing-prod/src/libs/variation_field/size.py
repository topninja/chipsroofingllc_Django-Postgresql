class Size:
    """
        Класс, помогающий рассчитать размеры картинки
        при её пропорциональном ресайзе
    """
    def __init__(self, width, height):
        self._width = self.source_width = int(width)
        self._height = self.source_height = int(height)

        if self._width <= 0:
            raise ValueError('width should be positive')
        if self._height <= 0:
            raise ValueError('height should be positive')

        self.aspect = self.source_width / self.source_height

    def _height_by_width(self, width):
        return int(width / self.aspect)

    def _width_by_height(self, height):
        return int(height * self.aspect)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        value = int(value)
        if self._width <= 0:
            raise ValueError('width should be positive')

        self._width = value
        self._height = self._height_by_width(value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._width = self._width_by_height(value)

    def max_width(self, value):
        """ Установка ограничения по ширине """
        if self._width > value:
            self.width = value

    def max_height(self, value):
        """ Установка ограничения по высоте """
        if self._height > value:
            self.height = value

    def __repr__(self):
        return 'Size(%s, %s)' % (self._width, self._height)
