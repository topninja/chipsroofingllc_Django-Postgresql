import json
from urllib import parse
from django.shortcuts import resolve_url
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils.translation import get_language
from social_networks.models import SocialConfig
from suit_ckeditor.widgets import CKEditorWidget as DefaultWidget
from .models import PagePhoto


class CKEditorWidget(DefaultWidget):
    class Media:
        extend = True
        css = {
            'all': (
                'ckeditor/admin/css/widget.css',
            )
        }
        js = (
            'ckeditor/admin/js/widget.js',
        )

    def render(self, name, value, attrs=None):
        self.editor_options.setdefault('language', get_language())

        attrs = attrs or {}
        attrs.setdefault('class', '')
        attrs['class'] += ' ckeditor-field'
        output = super(DefaultWidget, self).render(name, value, attrs)

        output += mark_safe('''
            <script type="text/javascript">
                window._ckeditor_confs = window._ckeditor_confs || {};
                window._ckeditor_confs["%s"] = %s;
            </script>
        ''' % (name, json.dumps(self.editor_options)))

        return output


class CKEditorUploadWidget(CKEditorWidget):
    """ Виджет редактора, добавляющий данные для определения модели при загрузке файлов """

    model = None

    class Media:
        extend = True
        js = (
            'common/js/plupload/plupload.full.min.js',
            'common/js/plupload/jquery.ui.plupload.js',
            'common/js/plupload/i18n/%s.js' % (get_language(), ),
        )

    def value_from_datadict(self, data, files, name):
        text = data.get(name, None)
        page_photos = data.get(name + '-page-photos', '')
        page_files = data.get(name + '-page-files', '')
        simple_photos = data.get(name + '-simple-photos', '')
        return [text, page_photos, page_files, simple_photos]

    def _build_url(self, base_url, **kwargs):
        """ Добавление к базовому адресу GET-параметров """
        urlparts = list(parse.urlparse(base_url))
        query = dict(parse.parse_qsl(urlparts[4]))
        query.update(kwargs)
        urlparts[4] = parse.urlencode(query)
        return parse.urlunparse(urlparts)

    def render(self, name, value, attrs=None):
        # URL загрузки фоток
        self.editor_options['PAGEPHOTOS_UPLOAD_URL'] = self._build_url(
            resolve_url('admin_ckeditor:upload_pagephoto'),
            app_label=self.model._meta.app_label,
            model_name=self.model._meta.model_name,
            field_name=name,
        )

        # URL поворота фоток
        self.editor_options['PAGEPHOTOS_ROTATE_URL'] = self._build_url(
            resolve_url('admin_ckeditor:rotate_pagephoto'),
            app_label=self.model._meta.app_label,
            model_name=self.model._meta.model_name,
        )

        # Crop фоток
        field = PagePhoto._meta.get_field('photo')
        self.editor_options['PAGEPHOTOS_MIN_DIMENSIONS'] = field.min_dimensions
        self.editor_options['PAGEPHOTOS_MAX_DIMENSIONS'] = field.max_dimensions
        self.editor_options['PAGEPHOTOS_ASPECTS'] = field.aspects
        self.editor_options['PAGEPHOTOS_CROP_URL'] = self._build_url(
            resolve_url('admin_ckeditor:crop_pagephoto'),
            app_label=self.model._meta.app_label,
            model_name=self.model._meta.model_name,
        )

        # URL загрузки файлов
        self.editor_options['PAGEFILES_UPLOAD_URL'] = self._build_url(
            resolve_url('admin_ckeditor:upload_pagefile'),
            app_label=self.model._meta.app_label,
            model_name=self.model._meta.model_name,
            field_name=name,
        )

        # URL загрузки простых фоток
        self.editor_options['SIMPLEPHOTOS_UPLOAD_URL'] = self._build_url(
            resolve_url('admin_ckeditor:upload_simplephoto'),
            app_label=self.model._meta.app_label,
            model_name=self.model._meta.model_name,
            field_name=name,
        )

        # Размер фото на странице
        self.editor_options['PAGEPHOTOS_THUMB_SIZE'] = (192, 108)

        # Максимальный размер файла
        self.editor_options['PAGEPHOTOS_MAX_FILE_SIZE'] = '10mb'
        self.editor_options['PAGEFILES_MAX_FILE_SIZE'] = '40mb'
        self.editor_options['SIMPLEPHOTOS_MAX_FILE_SIZE'] = '10mb'

        # Moxie
        self.editor_options['MOXIE_SWF'] = static('common/js/plupload/Moxie.swf')
        self.editor_options['MOXIE_XAP'] = static('common/js/plupload/Moxie.xap')

        # CSS приходится грузить JS-ом из-за переопределения стилей
        self.editor_options['PLUPLOADER_CSS'] = (
            static('admin/css/jquery-ui/jquery-ui.min.css'),
            static('common/js/plupload/css/jquery.ui.plupload.css'),
            static('ckeditor/admin/css/ckupload_fix.css'),
        )

        # Youtube APIKEY
        social = SocialConfig.get_solo()
        self.editor_options['YOUTUBE_APIKEY'] = social.google_apikey

        page_photos = []
        page_files = []
        simple_photos = []
        if isinstance(value, (tuple, list)):
            page_photos = value[1].split(',')
            page_files = value[1].split(',')
            simple_photos = value[2].split(',')
            value = value[0]

        output = mark_safe(
            '<input type="hidden" name="{0}-page-photos" value="{1}">'.format(name, ','.join(page_photos))
        )
        output += mark_safe(
            '<input type="hidden" name="{0}-page-files" value="{1}">'.format(name, ','.join(page_files))
        )
        output += mark_safe(
            '<input type="hidden" name="{0}-simple-photos" value="{1}">'.format(name, ','.join(simple_photos))
        )
        output += super().render(name, value, attrs)
        return output
