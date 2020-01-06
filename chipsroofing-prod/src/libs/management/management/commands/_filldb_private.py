import string
from operator import sub
from random import choice, randrange, randint
from django.utils.html import escape


#: list of lorem ipsum words used by the lipsum() helper function
LOREM_IPSUM_WORDS = '''\
    a ac accumsan ad adipiscing aenean aliquam aliquet amet ante aptent arcu at
    auctor augue bibendum blandit class commodo condimentum congue consectetuer
    consequat conubia convallis cras cubilia cum curabitur curae cursus dapibus
    diam dictum dictumst dignissim dis dolor donec dui duis egestas eget eleifend
    elementum elit enim erat eros est et etiam eu euismod facilisi facilisis fames
    faucibus felis fermentum feugiat fringilla fusce gravida habitant habitasse hac
    hendrerit hymenaeos iaculis id imperdiet in inceptos integer interdum ipsum
    justo lacinia lacus laoreet lectus leo libero ligula litora lobortis lorem
    luctus maecenas magna magnis malesuada massa mattis mauris metus mi molestie
    mollis montes morbi mus nam nascetur natoque nec neque netus nibh nisi nisl non
    nonummy nostra nulla nullam nunc odio orci ornare parturient pede pellentesque
    penatibus per pharetra phasellus placerat platea porta porttitor posuere
    potenti praesent pretium primis proin pulvinar purus quam quis quisque rhoncus
    ridiculus risus rutrum sagittis sapien scelerisque sed sem semper senectus sit
    sociis sociosqu sodales sollicitudin suscipit suspendisse taciti tellus tempor
    tempus tincidunt torquent tortor tristique turpis ullamcorper ultrices
    ultricies urna ut varius vehicula vel velit venenatis vestibulum vitae vivamus
    viverra volutpat vulputate'''


def get_field_choices(field):
    """ Получение возможных значений поля """
    possibles = []

    if field.null:
        possibles.append(None)

    if field._choices:
        for option_key, option_value in field.choices:
            if isinstance(option_value, (list, tuple)):
                for optgroup_key, optgroup_value in option_value:
                    possibles.append(optgroup_key)
            else:
                possibles.append(option_key)

    return possibles


def generate_lorem_ipsum(n=5, html=False, min_len=20, max_len=100):
    """Generate some lorem ipsum for the template."""
    words = LOREM_IPSUM_WORDS.split()
    result = []

    for _ in range(n):
        next_capitalized = True
        last_comma = last_fullstop = 0
        last = None
        p = []

        # each paragraph contains out of 20 to 100 words.
        for idx in range(randrange(min_len, max_len)):
            while True:
                word = choice(words)
                if word != last:
                    last = word
                    break
            if next_capitalized:
                word = word.capitalize()
                next_capitalized = False
            # add commas
            if idx - randrange(3, 8) > last_comma:
                last_comma = idx
                last_fullstop += 2
                word += ','
            # add end of sentences
            if idx - randrange(10, 20) > last_fullstop:
                last_comma = last_fullstop = idx
                word += '.'
                next_capitalized = True
            p.append(word)

        # ensure that the paragraph ends with a dot.
        p = ' '.join(p)
        if p.endswith(','):
            p = p[:-1] + '.'
        elif not p.endswith('.'):
            p += '.'
        result.append(p)

    if not html:
        return '\n\n'.join(result)
    return '\n\n'.join('<p>%s</p>' % escape(x) for x in result)


def generate_random_string(min_len=5, max_len=32):
    allowed_chars = string.ascii_letters + string.digits + '-'
    return ''.join(choice(allowed_chars) for _ in range(randrange(min_len, max_len)))


def get_spans(min_dimensions, max_dimensions, variations):
    """ Возвращает допустимые диапазоны ширины и высоты для картинки """
    min_width, min_height = min_dimensions or (0, 0)
    max_width, max_height = max_dimensions or (0, 0)

    variation_width = max(variation['size'][0] for variation in variations.values())
    variation_height = max(variation['size'][1] for variation in variations.values())

    # если не указан min_dimensions - берем самую большую вариацию
    min_width = max(min_width, variation_width)
    min_height = max(min_height, variation_height)

    # если не указан max_dimensions - берем 1920х1440
    max_width = min(1920, max_width or 1920)
    max_height = min(1440, max_height or 1440)

    return (min_width, max_width), (min_height, max_height)


def fetch_span(width_span, height_span, step=100):
    width_diff = sub(*reversed(width_span))
    step_count = width_diff // step
    if step_count <= 1:
        width = min(*width_span)
    else:
        width = width_span[0] + randint(0, step_count) * step

    height_diff = sub(*reversed(height_span))
    step_count = height_diff // step
    if step_count <= 1:
        height = min(*height_span)
    else:
        height = height_span[0] + randint(0, step_count) * step

    return width, height
