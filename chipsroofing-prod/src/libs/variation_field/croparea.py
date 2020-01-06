class CropArea:
    """
        Объект, представляющий область обрезки.
        Принимает координаты в форматах:
         1) один аргумент - строка "X:Y:W:H" или итератор (X, Y, W, H)
         2) четыре аргумента: X, Y, W, H
    """
    errors = {
        'bad_coord': 'Bad CropArea coord: %s'
    }

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], str):
                coords = args[0].split(':')
            else:
                coords = tuple(args[0])
        elif len(args) == 4:
            coords = args
        else:
            raise ValueError('Invalid attribute count: %r' % (args,))

        if len(coords) != 4:
            raise ValueError('Invalid crop area: %r' % args[0])

        self._crop_coords = list(map(self._format_coord, coords))

    def __iter__(self):
        return iter(self._crop_coords)

    def __getitem__(self, item):
        return self._crop_coords[item]

    def __repr__(self):
        return 'CropArea(%s)' % ','.join(map(str, self._crop_coords))

    def __str__(self):
        return ':'.join(map(str, self._crop_coords))

    def _format_coord(self, coord):
        try:
            coord = int(coord)
        except (TypeError, ValueError):
            raise ValueError(self.errors['bad_coord'] % coord)

        if coord < 0:
            raise ValueError(self.errors['bad_coord'] % coord)

        return coord

    @property
    def x(self):
        return self._crop_coords[0]

    @x.setter
    def x(self, value):
        self._crop_coords[0] = self._format_coord(value)

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y(self):
        return self._crop_coords[1]

    @y.setter
    def y(self, value):
        self._crop_coords[1] = self._format_coord(value)

    @property
    def y2(self):
        return self.y + self.height

    @property
    def width(self):
        return self._crop_coords[2]

    @width.setter
    def width(self, value):
        self._crop_coords[2] = self._format_coord(value)

    @property
    def height(self):
        return self._crop_coords[3]

    @height.setter
    def height(self, value):
        self._crop_coords[3] = self._format_coord(value)
