import random
import tempfile
import requests
from datetime import time
from decimal import Decimal
from requests.exceptions import Timeout
from django.apps import apps
from django.core.files import File
from django.db.models import fields
from django.core.management import BaseCommand
from django.utils.text import Truncator, slugify
from django.utils.timezone import now, timedelta
from django.db.models.fields.files import FileField, ImageField
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from gallery.fields import GalleryField
from ckeditor.fields import CKEditorField, CKEditorUploadField
from libs.stdimage.fields import StdImageField
from ._filldb_private import (
    get_field_choices,
    generate_random_string, generate_lorem_ipsum,
    get_spans, fetch_span
)


def set_boolean(instance, field):
    """ BooleanField """
    possibles = [True, False]
    possibles.extend(get_field_choices(field))
    setattr(instance, field.name, random.choice(possibles))


def set_chars(instance, field, max_length=255):
    """ CharField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    max_length = min(max_length, field.max_length or 16 * 1024)
    for validator in field.validators:
        if isinstance(validator, MaxLengthValidator):
            max_length = min(max_length, validator.limit_value)

    value = generate_lorem_ipsum(1, min_len=1, max_len=max(5, max_length // 8), html=False)
    value = Truncator(value).chars(max_length, html=False)
    setattr(instance, field.name, value)


def set_text(instance, field, paragraphs=1, html=False):
    """ TextField """
    max_len = field.max_length or 16 * 1024
    for validator in field.validators:
        if isinstance(validator, MaxLengthValidator):
            max_len = min(max_len, validator.limit_value)

    value = generate_lorem_ipsum(paragraphs, html=html)
    value = Truncator(value).chars(max_len, html=html)
    setattr(instance, field.name, value)


def set_slug(instance, field):
    """ SlugField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    value = slugify(generate_lorem_ipsum(1, min_len=1, max_len=6))
    value = Truncator(value).chars(field.max_length, html=False)
    setattr(instance, field.name, value)


def set_integer(instance, field, min_value=-2**31, max_value=2**31 - 1):
    """ IntegerField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    for validator in field.validators:
        if isinstance(validator, MinValueValidator):
            min_value = max(min_value, validator.limit_value)
        if isinstance(validator, MaxValueValidator):
            max_value = min(max_value, validator.limit_value)

    value = random.randint(min_value, max_value)
    setattr(instance, field.name, value)


def set_date(instance, field):
    """ DateField """
    start = -60 * 24 * 3600
    end = 60 * 24 * 3600
    value = now() + timedelta(seconds=random.randint(start, end))
    setattr(instance, field.name, value)


def set_time(instance, field):
    """ TimeField """
    value = time(random.randint(0, 23), random.choice([0, 15, 30, 45]))
    setattr(instance, field.name, value)


def set_decimal(instance, field, max_digits=10):
    """ DecimalField """
    max_digits = min(max_digits, field.max_digits)
    min_value = -10 ** max_digits
    max_value = 10 ** max_digits
    for validator in field.validators:
        if isinstance(validator, MinValueValidator):
            min_value = max(min_value, validator.limit_value)
        if isinstance(validator, MaxValueValidator):
            max_value = min(max_value, validator.limit_value)

    value = random.randint(min_value, max_value)
    value = Decimal(value) / 10 ** field.decimal_places

    setattr(instance, field.name, value)


def set_email(instance, field):
    """ EmailField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    value = generate_random_string(min_len=2, max_len=20)
    setattr(instance, field.name, '%s@gmail.com' % value)


def set_float(instance, field):
    """ FloatField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    min_value = -2 ** 8
    max_value = 2 ** 8 - 1
    for validator in field.validators:
        if isinstance(validator, MinValueValidator):
            min_value = max(min_value, validator.limit_value)
        if isinstance(validator, MaxValueValidator):
            max_value = min(max_value, validator.limit_value)

    value = random.uniform(min_value, max_value)
    setattr(instance, field.name, value)


def set_url(instance, field):
    """ URLField """
    possibles = []
    possibles.extend(get_field_choices(field))
    if possibles:
        setattr(instance, field.name, random.choice(possibles))
        return

    max_len = field.max_length
    for validator in field.validators:
        if isinstance(validator, MaxLengthValidator):
            max_len = min(max_len, validator.limit_value)

    value = 'http://google.com/%s/' % generate_random_string(5, 10)
    setattr(instance, field.name, value)


def set_fk(instance, field):
    """ ForeignKey / OneToOneField """
    if field.unique:
        return

    related = field.rel.to.objects.all()
    if not related:
        raise ValueError('no instances for field "%s"' % field.name)

    min_index = 0 if field.null else 1
    max_index = related.count()

    index = random.randint(min_index, max_index)
    if index is 0:
        value = None
    else:
        value = related[index-1]

    setattr(instance, field.name, value)


def set_m2m(instance, field, max_count=8):
    """ ManyToManyField """
    related = field.rel.to.objects.all()
    if not related:
        raise ValueError('no instances for field "%s"' % field.name)

    min_count = 0 if field.blank else 2
    max_count = min(max_count, related.count())

    manager = getattr(instance, field.name)
    for item in related.order_by('?')[:random.randint(min_count, max_count)]:
        manager.add(item)


def set_image(instance, field, width=1920, height=1440):
    """ FileField / ImageField """
    manager = getattr(instance, field.name)

    try:
        image_type = random.choice(['people', 'places', 'things'])
        response = requests.get(
            'https://placem.at/%s?w=%d&h=%d&random=1&txt=' % (image_type, width, height),
            timeout=5,
            stream=True
        )
    except (ConnectionError, Timeout):
        response = requests.get('http://baconmockup.com/%d/%d/' % (width, height), stream=True)

    tfp = tempfile.NamedTemporaryFile(delete=False)
    with tfp:
        for chunk in response.iter_content(1024 * 1024):
            tfp.write(chunk)
        tfp.seek(0)

        manager.save('image.jpg', File(tfp), save=False)


def set_stdimage(instance, field):
    """ StdImageField """
    wspan, hspan = get_spans(field.min_dimensions, field.max_dimensions, field.variations)
    width, height = fetch_span(wspan, hspan)
    set_image(instance, field, width=width, height=height)


def set_gallery(instance, field, photo_count=3):
    """ GalleryField """
    gallery = field.rel.to.objects.create()
    setattr(instance, field.name, gallery)

    ImageModel = gallery.IMAGE_MODEL
    min_dimensions = getattr(ImageModel, 'MIN_DIMENSIONS', (0, 0))
    max_dimensions = getattr(ImageModel, 'MAX_DIMENSIONS', (0, 0))
    variations = getattr(ImageModel, 'VARIATIONS', {})
    wspan, hspan = get_spans(min_dimensions, max_dimensions, variations)

    for _ in range(photo_count):
        gallery_item = gallery.IMAGE_MODEL(
            gallery=gallery,
        )

        set_chars(gallery_item, ImageModel._meta.get_field('description'))

        width, height = fetch_span(wspan, hspan)
        set_image(gallery_item, ImageModel._meta.get_field('image'), width=width, height=height)

        gallery_item.save()


class Command(BaseCommand):
    """
        Заполнение БД рандомными данными
    """
    help = 'Fill database with random data'

    def add_arguments(self, parser):
        parser.add_argument(
            action='store',
            dest='model',
            help='Object model (e.g. "news.post")'
        )
        parser.add_argument('-c', '--count',
            action='store',
            dest='count',
            type=int,
            default=1,
            help='Number of objects to create'
        )

    def handle(self, *args, **options):
        try:
            app, model = options['model'].split('.')
        except (ValueError, AttributeError):
            raise ValueError('invalid "model" value')

        Model = apps.get_model(app, model)

        count = options['count']
        if count <= 0:
            raise ValueError('"count" must be greather than 0')

        for _ in range(count):
            print('Creating object %d of %d...' % (_ + 1, count))

            instance = Model()
            for field in Model._meta.get_fields():
                if field.auto_created:
                    continue

                if field.is_relation:
                    if field.many_to_many:
                        continue
                    elif isinstance(field, GalleryField):
                        set_gallery(instance, field, photo_count=random.randint(2, 4))
                    else:
                        set_fk(instance, field)
                elif isinstance(field, fields.BooleanField):
                    set_boolean(instance, field)
                elif isinstance(field, fields.EmailField):
                    set_email(instance, field)
                elif isinstance(field, fields.SlugField):
                    set_slug(instance, field)
                elif isinstance(field, fields.URLField):
                    set_url(instance, field)
                elif isinstance(field, fields.PositiveSmallIntegerField):
                    set_integer(instance, field, min_value=0, max_value=32767)
                elif isinstance(field, fields.PositiveIntegerField):
                    set_integer(instance, field, min_value=0)
                elif isinstance(field, fields.SmallIntegerField):
                    set_integer(instance, field, min_value=-32768, max_value=32767)
                elif isinstance(field, fields.IntegerField):
                    set_integer(instance, field)
                elif isinstance(field, fields.FloatField):
                    set_float(instance, field)
                elif isinstance(field, fields.CharField):
                    set_chars(instance, field)
                elif isinstance(field, (CKEditorField, CKEditorUploadField)):
                    set_text(instance, field, paragraphs=random.randint(3, 10), html=True)
                elif isinstance(field, fields.TextField):
                    set_text(instance, field, paragraphs=random.randint(1, 3))
                elif isinstance(field, fields.DateField):
                    set_date(instance, field)
                elif isinstance(field, fields.TimeField):
                    set_time(instance, field)
                elif isinstance(field, fields.DecimalField):
                    set_decimal(instance, field, max_digits=6)
                elif isinstance(field, StdImageField):
                    set_stdimage(instance, field)
                elif isinstance(field, ImageField):
                    set_image(instance, field, width=1920, height=1440)
                elif isinstance(field, FileField):
                    set_image(instance, field, width=800, height=600)
                else:
                    print('WARNING: unknown type of field "%s": %s' % (field.name, type(field)))
                    continue

            instance.full_clean()
            instance.save()

            for field, model in Model._meta.get_m2m_with_model():
                set_m2m(instance, field)

        print('Done')
